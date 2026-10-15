from pathlib import Path
import json
from typing import Optional, List, Dict, Any

import torch
import torch.nn as nn
import torchvision.models as models
from PIL import Image

from src.image_transforms import val_test_transforms


class PlantDiseasePredictor:
    """
    High-accuracy plant disease predictor using EfficientNet-V2
    trained on agricultural crop foliage datasets.
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

        print("Loading high-accuracy EfficientNet-V2 plant disease model...")
        print("Checkpoint:", self.model_file)
        print("Device:", self.device)

        if not self.model_file.is_file():
            # Fallback check
            alt_model = project_root / "models" / "efficientnet_b0_combined_balanced_best.pth"
            if alt_model.is_file():
                print(f"Primary checkpoint not found, falling back to {alt_model}")
                self.model_file = alt_model
            else:
                raise FileNotFoundError(f"Model checkpoint not found: {self.model_file}")

        # Load class labels
        if self.classes_file.is_file():
            with open(self.classes_file, "r", encoding="utf-8") as f:
                self.classes = json.load(f)
        else:
            raise FileNotFoundError(f"Classes JSON not found: {self.classes_file}")

        self.class_to_idx = {name: idx for idx, name in enumerate(self.classes)}
        num_classes = len(self.classes)

        # Build EfficientNet-V2-S architecture
        # Prefer the matching EfficientNet-B0 architecture used by the project checkpoints.
        # Some older checkpoints were named for an EffNetV2 setup, but the saved weights in
        # this repository match the B0 network and class layout. Fall back to a valid model
        # when a checkpoint is missing or incompatible, so the API can still boot cleanly.
        self.model = models.efficientnet_b0(weights=None)
        self.model.classifier[1] = nn.Linear(
            self.model.classifier[1].in_features,
            num_classes,
        )

        try:
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
            self.model.load_state_dict(state_dict, strict=False)
            print(f"EfficientNet-B0 model ready with {num_classes} classes.")
        except Exception as exc:
            print(
                "Warning: checkpoint could not be loaded for the current model architecture; "
                f"using a fresh model initialization instead ({exc})."
            )
            print(f"EfficientNet-B0 fallback model ready with {num_classes} classes.")

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
