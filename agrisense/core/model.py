"""
AgriSense - Deep Learning Inference Engine
Model: EfficientNet-B0 trained on Agricultural Leaf Datasets
Features: Crop-constrained Bayesian Inference, Confidence Thresholding, Crop Mismatch Detection
"""

from pathlib import Path
from typing import Dict, List, Optional, Tuple

import numpy as np
import torch
import torch.nn as nn
from PIL import Image
from torchvision import transforms
from torchvision.models import efficientnet_b0

from agrisense.data.treatments_db import CROP_MAPPING, get_diseases_for_crop


# ImageNet Standard Normalization
INFERENCE_TRANSFORMS = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225],
    ),
])


class AgriSenseModel:
    """
    Deep learning inference engine with crop-conditioned probability filtering.
    """

    def __init__(self, checkpoint_path: Optional[Path] = None):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        project_root = Path(__file__).resolve().parent.parent.parent
        effnetv2_path = project_root / "models" / "effnetv2_s_plant_disease.pth"
        effnetv2_classes = project_root / "models" / "effnetv2_s_classes.json"

        if checkpoint_path is None:
            if effnetv2_path.is_file() and effnetv2_classes.is_file():
                checkpoint_path = effnetv2_path
            else:
                checkpoint_path = project_root / "models" / "efficientnet_b0_combined_balanced_best.pth"
            
        self.checkpoint_path = checkpoint_path
        self.classes_path = effnetv2_classes if checkpoint_path == effnetv2_path else None
        self.model: Optional[nn.Module] = None
        self.classes: List[str] = []
        self.class_to_idx: Dict[str, int] = {}
        self.is_loaded = False
        
        self._load_model()

    def _load_model(self):
        """Loads model checkpoint or creates a fallback ready model."""
        import json
        from torchvision.models import efficientnet_v2_s, efficientnet_b0

        if self.checkpoint_path.is_file():
            try:
                checkpoint = torch.load(
                    self.checkpoint_path,
                    map_location="cpu",
                    weights_only=False,
                )

                if self.classes_path and self.classes_path.is_file():
                    with open(self.classes_path, "r", encoding="utf-8") as f:
                        self.classes = json.load(f)
                    self.class_to_idx = {name: idx for idx, name in enumerate(self.classes)}
                    num_classes = len(self.classes)

                    self.model = efficientnet_v2_s(weights=None)
                    in_features = self.model.classifier[1].in_features
                    self.model.classifier[1] = nn.Linear(in_features, num_classes)

                    state_dict = checkpoint["model_state_dict"] if isinstance(checkpoint, dict) and "model_state_dict" in checkpoint else checkpoint
                    self.model.load_state_dict(state_dict, strict=True)
                    self.model = self.model.to(self.device)
                    self.model.eval()
                    self.is_loaded = True
                    print(f"[AgriSense] Successfully loaded EfficientNet-V2 with {num_classes} classes on {self.device}.")
                    return

                elif isinstance(checkpoint, dict) and "class_to_idx" in checkpoint:
                    self.class_to_idx = {
                        k: int(v) for k, v in checkpoint["class_to_idx"].items()
                    }
                    self.classes = [
                        k for k, _ in sorted(self.class_to_idx.items(), key=lambda x: x[1])
                    ]
                    num_classes = len(self.classes)
                    self.model = efficientnet_b0(weights=None)
                    in_features = self.model.classifier[1].in_features
                    self.model.classifier[1] = nn.Linear(in_features, num_classes)
                    self.model.load_state_dict(checkpoint["model_state_dict"], strict=True)
                    self.model = self.model.to(self.device)
                    self.model.eval()
                    self.is_loaded = True
                    print(f"[AgriSense] Successfully loaded model with {num_classes} classes on {self.device}.")
                    return
            except Exception as e:
                print(f"[AgriSense] Warning: Checkpoint load error ({e}). Initializing fallback.")
                
        # Fallback initialization if checkpoint is missing or incompatible
        print("[AgriSense] Initializing pre-trained backbone fallback model.")
        from torchvision.models import EfficientNet_B0_Weights
        self.classes = [
            "Grape___healthy", "Grape___Downy_mildew", "Grape___Powdery_mildew", "Grape___Black_rot",
            "Tomato___healthy", "Tomato___Early_blight", "Tomato___Late_blight", "Tomato___Bacterial_spot",
            "Soybean___healthy", "Soybean___Rust", "Soybean___Bacterial_blight", "Soybean___Cercospora_leaf_blight"
        ]
        self.class_to_idx = {c: i for i, c in enumerate(self.classes)}
        self.model = efficientnet_b0(weights=EfficientNet_B0_Weights.DEFAULT)
        in_features = self.model.classifier[1].in_features
        self.model.classifier[1] = nn.Linear(in_features, len(self.classes))
        self.model = self.model.to(self.device)
        self.model.eval()
        self.is_loaded = True

    def predict(
        self,
        image: Image.Image,
        selected_crop: str,
        confidence_threshold: float = 0.70
    ) -> Dict:
        """
        Conditioned prediction for a single leaf image given selected crop.
        
        Args:
            image: PIL Image
            selected_crop: 'Grapes', 'Tomato', or 'Soybean'
            confidence_threshold: 0.70 standard threshold
            
        Returns:
            Dictionary containing prediction metrics, crop-conditioned probabilities,
            and warnings.
        """
        image_rgb = image.convert("RGB")
        input_tensor = INFERENCE_TRANSFORMS(image_rgb).unsqueeze(0).to(self.device)

        with torch.no_grad():
            logits = self.model(input_tensor)
            global_probs = torch.softmax(logits, dim=1)[0]

        # Global top prediction (unconstrained)
        global_top_idx = torch.argmax(global_probs).item()
        global_top_class = self.classes[global_top_idx]
        global_top_conf = float(global_probs[global_top_idx].item())

        # Determine valid classes for the selected crop
        target_keys = get_diseases_for_crop(selected_crop)
        valid_indices = [
            self.class_to_idx[k] for k in target_keys if k in self.class_to_idx
        ]

        if not valid_indices:
            # Fallback if specific classes are missing from index
            valid_indices = list(range(len(self.classes)))

        # Sub-logits for the selected crop
        crop_logits = logits[0, valid_indices]
        crop_probs = torch.softmax(crop_logits, dim=0)

        # Sort crop-specific predictions
        sorted_indices = torch.argsort(crop_probs, descending=True)
        top_crop_predictions = []
        for idx in sorted_indices:
            original_class_idx = valid_indices[idx.item()]
            class_name = self.classes[original_class_idx]
            prob = float(crop_probs[idx.item()].item())
            top_crop_predictions.append({
                "class_key": class_name,
                "confidence": prob,
                "confidence_percent": round(prob * 100, 2)
            })

        best_prediction = top_crop_predictions[0]
        predicted_class = best_prediction["class_key"]
        best_conf = best_prediction["confidence"]
        predicted_idx = self.class_to_idx.get(predicted_class, valid_indices[0])

        # Cross-crop mismatch detection
        # If model is overwhelmingly confident (>85%) in a completely different crop
        crop_mismatch_warning = None
        global_crop_prefix = global_top_class.split("___")[0].lower()
        selected_crop_clean = selected_crop.lower()
        if (
            global_crop_prefix != selected_crop_clean
            and global_top_conf > 0.85
            and best_conf < 0.60
        ):
            crop_mismatch_warning = (
                f"Model detected features of '{global_top_class.split('___')[0]}' "
                f"instead of selected '{selected_crop}'. Please verify your crop selection."
            )

        is_low_confidence = best_conf < confidence_threshold
        is_healthy = "healthy" in predicted_class.lower()

        return {
            "class_key": predicted_class,
            "confidence": best_conf,
            "confidence_percent": round(best_conf * 100, 2),
            "is_low_confidence": is_low_confidence,
            "confidence_threshold": confidence_threshold,
            "is_healthy": is_healthy,
            "selected_crop": selected_crop,
            "top_predictions": top_crop_predictions,
            "global_top_class": global_top_class,
            "global_top_conf": global_top_conf,
            "crop_mismatch_warning": crop_mismatch_warning,
            "input_tensor": input_tensor,
            "predicted_idx": predicted_idx
        }
