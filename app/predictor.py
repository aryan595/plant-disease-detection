from pathlib import Path
import json
import os
from typing import Optional, List, Dict, Any

# Keep the production worker within the memory and CPU budget of a small web
# service. These are defaults only, so a larger host can deliberately override
# them through its environment.
for _thread_env in (
    "OMP_NUM_THREADS",
    "MKL_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
):
    os.environ.setdefault(_thread_env, "1")
os.environ.setdefault("MALLOC_ARENA_MAX", "2")

import torch
import torch.nn as nn
import torchvision.models as models
from PIL import Image

from src.image_transforms import val_test_transforms


class PlantDiseasePredictor:
    """
    High-accuracy plant disease predictor backed by the project's saved
    EfficientNet checkpoint. The checkpoint supplies the authoritative class
    mapping so weights and labels can never drift apart at runtime.
    """

    def __init__(self):
        project_root = Path(__file__).resolve().parent.parent

        self.model_file = (
            project_root
            / "models"
            / "effnetv2_s_plant_disease.pth"
        )
        self.classes_file = (
            project_root
            / "models"
            / "effnetv2_s_classes.json"
        )

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        # A single request is processed at a time by the API worker. Limiting
        # native thread pools avoids unnecessary per-thread memory on Render's
        # compact instances and is more predictable under concurrent traffic.
        try:
            torch.set_num_threads(int(os.getenv("TORCH_NUM_THREADS", "1")))
            torch.set_num_interop_threads(1)
        except RuntimeError:
            # PyTorch only allows changing inter-op threads before parallel
            # work begins. It is safe to retain its existing setting otherwise.
            pass

        print("Loading plant disease model...")
        print("Device:", self.device)

        if not self.model_file.is_file():
            # Fallback check
            alt_model = project_root / "models" / "efficientnet_b0_combined_balanced_best.pth"
            if alt_model.is_file():
                print(f"Primary checkpoint not found, falling back to {alt_model}")
                self.model_file = alt_model
            else:
                raise FileNotFoundError(f"Model checkpoint not found: {self.model_file}")

        print("Checkpoint:", self.model_file)
        checkpoint = torch.load(
            self.model_file,
            map_location="cpu",
            weights_only=False,
        )
        state_dict = (
            checkpoint["model_state_dict"]
            if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint
            else checkpoint
        )

        if not isinstance(state_dict, dict):
            raise ValueError("The model checkpoint does not contain a valid state dictionary.")

        # The persisted mapping is coupled to the classifier weights. Prefer it over
        # auxiliary JSON files, which may describe an earlier training run.
        saved_mapping = checkpoint.get("class_to_idx") if isinstance(checkpoint, dict) else None
        saved_classes = checkpoint.get("classes") if isinstance(checkpoint, dict) else None
        if isinstance(saved_mapping, dict):
            self.classes = [
                class_name
                for class_name, _ in sorted(
                    saved_mapping.items(),
                    key=lambda item: int(item[1]),
                )
            ]
        elif isinstance(saved_classes, list):
            self.classes = list(saved_classes)
        elif self.classes_file.is_file():
            with open(self.classes_file, "r", encoding="utf-8") as file:
                self.classes = json.load(file)
        else:
            raise ValueError("The checkpoint has no class mapping and no fallback classes file exists.")

        classifier_weights = state_dict.get("classifier.1.weight")
        if classifier_weights is None:
            raise ValueError("The checkpoint is missing EfficientNet classifier weights.")

        checkpoint_class_count = int(classifier_weights.shape[0])
        if len(self.classes) != checkpoint_class_count:
            raise ValueError(
                "Checkpoint class mapping does not match its classifier: "
                f"{len(self.classes)} labels for {checkpoint_class_count} output weights."
            )

        self.class_to_idx = {name: idx for idx, name in enumerate(self.classes)}
        model_name = self.model_file.name.lower()
        if "effnetv2" in model_name or "efficientnet_v2" in model_name:
            self.model = models.efficientnet_v2_s(weights=None)
            architecture = "EfficientNet-V2-S"
        else:
            self.model = models.efficientnet_b0(weights=None)
            architecture = "EfficientNet-B0"

        self.model.classifier[1] = nn.Linear(
            self.model.classifier[1].in_features,
            checkpoint_class_count,
        )
        # Never run inference on randomly initialized weights. A checkpoint mismatch
        # is a deployment error and must be visible instead of producing fake confidence.
        self.model.load_state_dict(state_dict, strict=True)
        print(f"{architecture} model ready with {checkpoint_class_count} classes.")

        self.model = self.model.to(self.device)
        self.model.eval()

    def predict(
        self,
        image: Image.Image,
        crop: Optional[str] = None,
    ) -> List[Dict[str, Any]]:
        """
        Run inference on image.
        If crop is provided (e.g. 'Tomato', 'Grape', 'Soybean', 'Potato'),
        evaluates with prior conditioning on that specific crop's classes.
        """
        image = image.convert("RGB")
        tensor = val_test_transforms(image).unsqueeze(0).to(self.device)

        with torch.inference_mode():
            logits = self.model(tensor)

            # Optional crop-conditioned inference
            if crop and crop.strip().lower() not in ["all", "any", "auto", ""]:
                target_crop = crop.strip().lower()
                matching_indices = [
                    idx for idx, c in enumerate(self.classes)
                    if c.lower().startswith(target_crop) or target_crop in c.lower().split("___")[0]
                ]
                if matching_indices:
                    sub_logits = logits[0, matching_indices]
                    sub_probs = torch.softmax(sub_logits, dim=0)
                    k = min(3, len(matching_indices))
                    top_probs, top_k = sub_probs.topk(k)
                    results = []
                    for rank in range(k):
                        orig_idx = matching_indices[top_k[rank].item()]
                        results.append({
                            "class": self.classes[orig_idx],
                            "confidence": top_probs[rank].item(),
                        })
                    return results

            # Global top 3 across all classes
            probabilities = torch.softmax(logits, dim=1)
            top_probabilities, top_indices = probabilities.topk(
                min(3, len(self.classes)),
                dim=1,
            )

        results = []
        for rank in range(top_indices.shape[1]):
            index = top_indices[0, rank].item()
            probability = top_probabilities[0, rank].item()
            results.append({
                "class": self.classes[index],
                "confidence": probability,
            })

        return results
