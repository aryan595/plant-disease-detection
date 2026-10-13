"""
AgriSense - Explainable AI (XAI) Grad-CAM Module
Algorithm: Gradient-weighted Class Activation Mapping (Selvaraju et al., 2017)
Provides visual interpretability to verify where the deep learning model focuses on the leaf.
"""

from typing import Dict, Tuple

import cv2
import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image


class GradCAMExplainer:
    """
    Computes and visualizes Grad-CAM heatmaps for EfficientNet-B0.
    """

    def __init__(self, model_engine):
        self.engine = model_engine
        self.model = model_engine.model
        self.device = model_engine.device
        
        # Final convolutional layer of EfficientNet-B0
        self.target_layer = self.model.features[-1]
        
        self.activations = None
        self.gradients = None

    def _forward_hook(self, module, input, output):
        self.activations = output

    def _backward_hook(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate_cam(
        self,
        image: Image.Image,
        target_class_idx: int,
        alpha: float = 0.55
    ) -> Dict:
        """
        Generate Grad-CAM heatmap and blended visualization for the target class.
        
        Args:
            image: Original PIL Leaf Image
            target_class_idx: Target output index in the model
            alpha: Blending weight between original image and heatmap
            
        Returns:
            Dictionary with heatmap array, overlay PIL image, side-by-side PIL image.
        """
        image_rgb = image.convert("RGB")
        original_np = np.array(image_rgb)
        orig_h, orig_w = original_np.shape[:2]

        # Register hooks
        handle_fwd = self.target_layer.register_forward_hook(self._forward_hook)
        handle_bwd = self.target_layer.register_full_backward_hook(self._backward_hook)

        # Preprocess image
        from agrisense.core.model import INFERENCE_TRANSFORMS
        input_tensor = INFERENCE_TRANSFORMS(image_rgb).unsqueeze(0).to(self.device)

        self.model.zero_grad()
        output = self.model(input_tensor)

        # Score for target class
        score = output[0, target_class_idx]
        score.backward()

        # Remove hooks
        handle_fwd.remove()
        handle_bwd.remove()

        # Extract activations and gradients
        activation = self.activations[0]  # shape: [C, H, W]
        gradient = self.gradients[0]      # shape: [C, H, W]

        # Neuron importance weights via Global Average Pooling
        weights = gradient.mean(dim=(1, 2))  # shape: [C]

        # Weighted combination of forward activation maps
        cam = torch.zeros(activation.shape[1:], device=self.device)
        for i, w in enumerate(weights):
            cam += w * activation[i]

        # Apply ReLU to retain only features with positive influence
        cam = F.relu(cam)

        # Normalize between 0 and 1
        cam_min = cam.min()
        cam_max = cam.max()
        if cam_max > cam_min:
            cam = (cam - cam_min) / (cam_max - cam_min)
        else:
            cam = torch.zeros_like(cam)

        heatmap_np = cam.detach().cpu().numpy()

        # Resize heatmap to match original image dimensions
        heatmap_resized = cv2.resize(heatmap_np, (orig_w, orig_h))

        # Colorize heatmap using JET colormap
        heatmap_uint8 = np.uint8(255 * np.clip(heatmap_resized, 0, 1))
        colored_heatmap_bgr = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
        colored_heatmap_rgb = cv2.cvtColor(colored_heatmap_bgr, cv2.COLOR_BGR2RGB)

        # Blend with original leaf image
        overlay_np = cv2.addWeighted(
            original_np, 1.0 - alpha,
            colored_heatmap_rgb, alpha,
            0
        )

        overlay_pil = Image.fromarray(overlay_np)
        colored_heatmap_pil = Image.fromarray(colored_heatmap_rgb)

        # Create high-impact side-by-side comparison image [Original | Heatmap | Overlay]
        gap = 10
        total_w = orig_w * 2 + gap
        side_by_side = Image.new("RGB", (total_w, orig_h), color=(240, 243, 240))
        side_by_side.paste(image_rgb, (0, 0))
        side_by_side.paste(overlay_pil, (orig_w + gap, 0))

        return {
            "raw_heatmap": heatmap_resized,
            "colored_heatmap_pil": colored_heatmap_pil,
            "overlay_pil": overlay_pil,
            "side_by_side_pil": side_by_side,
        }
