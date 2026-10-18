from typing import Optional, Dict, Any
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from src.image_transforms import val_test_transforms


class GradCAMService:
    """
    Grad-CAM service for explainable AI disease lesion localization
    using EfficientNet-V2.
    """

    def __init__(self, predictor):
        self.predictor = predictor
        self.model = predictor.model
        self.device = predictor.device
        self.classes = predictor.classes

        self.activations = None
        self.gradients = None

        # Final convolutional feature layer of EfficientNet-V2
        if hasattr(self.model, "features"):
            self.target_layer = self.model.features[-1]
        else:
            self.target_layer = list(self.model.children())[-2]

    def _forward_hook(self, module, input, output):
        self.activations = output

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def analyze(
        self,
        image: Image.Image,
        crop: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Computes Grad-CAM activation heatmap for the top predicted disease class.
        """
        image = image.convert("RGB")

        # Register forward and backward hooks
        forward_handle = self.target_layer.register_forward_hook(self._forward_hook)
        backward_handle = self.target_layer.register_full_backward_hook(self._backward_hook)

        try:
            input_tensor = val_test_transforms(image).unsqueeze(0).to(self.device)

            self.model.zero_grad()
            outputs = self.model(input_tensor)

            probabilities = torch.softmax(outputs, dim=1)

            # Crop selection changes the probability space shown to the grower.
            # Keep the displayed confidence and top predictions in that same space;
            # previously we selected a crop-specific class but reported its much
            # smaller global probability across every model class.
            target_class_idx = None
            top_confidences = None
            top_class_indices = None
            if crop and crop.strip().lower() not in ["all", "any", "auto", ""]:
                target_crop = crop.strip().lower()
                matching = [
                    idx for idx, c in enumerate(self.classes)
                    if c.lower().startswith(target_crop) or target_crop in c.lower().split("___")[0]
                ]
                if matching:
                    sub_logits = outputs[0, matching]
                    sub_probs = torch.softmax(sub_logits, dim=0)
                    k = min(3, len(matching))
                    top_confidences, top_positions = sub_probs.topk(k)
                    top_class_indices = [
                        matching[position.item()]
                        for position in top_positions
                    ]
                    target_class_idx = top_class_indices[0]

            if target_class_idx is None:
                k = min(3, len(self.classes))
                top_confidences, top_indices = probabilities.topk(k, dim=1)
                top_confidences = top_confidences[0]
                top_class_indices = [
                    index.item()
                    for index in top_indices[0]
                ]
                target_class_idx = top_class_indices[0]

            predicted_class = self.classes[target_class_idx]
            confidence = top_confidences[0].item()

            # Backward pass for Grad-CAM
            target_score = outputs[0, target_class_idx]
            target_score.backward()

            if self.activations is None or self.gradients is None:
                raise RuntimeError("Failed to capture feature activations or gradients for Grad-CAM.")

            activation = self.activations[0]
            gradient = self.gradients[0]

            # Channel-wise pooling weights
            weights = gradient.mean(dim=(1, 2))

            # Weighted linear combination
            cam = torch.zeros(activation.shape[1:], device=self.device)
            for ch in range(activation.shape[0]):
                cam += weights[ch] * activation[ch]

            # Rectified Linear Unit (ReLU)
            cam = F.relu(cam)

            # Normalization to [0, 1]
            cam_min = cam.min()
            cam_max = cam.max()
            if cam_max > cam_min:
                cam = (cam - cam_min) / (cam_max - cam_min)
            else:
                cam = torch.zeros_like(cam)

            heatmap = cam.detach().cpu().numpy()

            # Resize heatmap to match image dimensions
            width, height = image.size
            heatmap_img = Image.fromarray(np.uint8(heatmap * 255))
            heatmap_img = heatmap_img.resize((width, height), Image.Resampling.BILINEAR)
            heatmap_full = np.array(heatmap_img) / 255.0

            # The candidates mirror the probability space used for the displayed score.
            top_3 = []
            for rank, idx in enumerate(top_class_indices):
                top_3.append({
                    "class": self.classes[idx],
                    "confidence": top_confidences[rank].item(),
                })

            return {
                "class": predicted_class,
                "confidence": confidence,
                "top_3": top_3,
                "heatmap": heatmap_full,
            }

        finally:
            forward_handle.remove()
            backward_handle.remove()

    def generate(self, image: Image.Image, crop: Optional[str] = None) -> Dict[str, Any]:
        """Alias for analyze() to ensure backward compatibility."""
        return self.analyze(image, crop=crop)
