import numpy as np
import torch
import torch.nn.functional as F
from PIL import Image

from src.image_transforms import val_test_transforms


class GradCAMService:

    def __init__(self, predictor):

        self.predictor = predictor

        self.model = predictor.model
        self.device = predictor.device
        self.classes = predictor.classes

        self.activations = None
        self.gradients = None

        # Final convolutional feature layer
        self.target_layer = self.model.features[-1]

    # =====================================
    # Forward hook
    # =====================================

    def _forward_hook(
        self,
        module,
        input,
        output,
    ):
        self.activations = output

    # =====================================
    # Backward hook
    # =====================================

    def _backward_hook(
        self,
        module,
        grad_input,
        grad_output,
    ):
        self.gradients = grad_output[0]

    # =====================================
    # Analyze image
    # =====================================

    def analyze(self, image: Image.Image):

        image = image.convert("RGB")

        # ---------------------------------
        # Register hooks
        # ---------------------------------

        forward_handle = (
            self.target_layer.register_forward_hook(
                self._forward_hook
            )
        )

        backward_handle = (
            self.target_layer.register_full_backward_hook(
                self._backward_hook
            )
        )

        try:

            # -----------------------------
            # Transform image
            # -----------------------------

            input_tensor = val_test_transforms(
                image
            )

            input_tensor = (
                input_tensor
                .unsqueeze(0)
                .to(self.device)
            )

            # -----------------------------
            # ONE forward pass
            # -----------------------------

            self.model.zero_grad()

            outputs = self.model(
                input_tensor
            )

            # -----------------------------
            # Probabilities
            # -----------------------------

            probabilities = torch.softmax(
                outputs,
                dim=1
            )

            # -----------------------------
            # Top 3
            # -----------------------------

            top_probabilities, top_indices = (
                probabilities.topk(
                    3,
                    dim=1
                )
            )

            # -----------------------------
            # Predicted class
            # -----------------------------

            predicted_index = (
                top_indices[0][0].item()
            )

            predicted_class = (
                self.classes[predicted_index]
            )

            confidence = (
                top_probabilities[0][0].item()
            )

            # -----------------------------
            # Backward pass for Grad-CAM
            # -----------------------------

            target_score = outputs[
                0,
                predicted_index
            ]

            target_score.backward()

            # -----------------------------
            # Activations
            # -----------------------------

            activation = self.activations[0]

            gradient = self.gradients[0]

            # -----------------------------
            # Channel weights
            # -----------------------------

            weights = gradient.mean(
                dim=(1, 2)
            )

            # -----------------------------
            # Weighted feature maps
            # -----------------------------

            cam = torch.zeros(
                activation.shape[1:],
                device=self.device
            )

            for channel in range(
                activation.shape[0]
            ):

                cam += (
                    weights[channel]
                    * activation[channel]
                )

            # -----------------------------
            # ReLU
            # -----------------------------

            cam = F.relu(cam)

            # -----------------------------
            # Normalize
            # -----------------------------

            cam -= cam.min()

            if cam.max() > 0:
                cam /= cam.max()

            # -----------------------------
            # Convert to NumPy
            # -----------------------------

            heatmap = (
                cam
                .detach()
                .cpu()
                .numpy()
            )

            # -----------------------------
            # Resize heatmap
            # -----------------------------

            width, height = image.size

            heatmap_image = Image.fromarray(
                np.uint8(
                    heatmap * 255
                )
            )

            heatmap_image = (
                heatmap_image.resize(
                    (width, height),
                    Image.Resampling.BILINEAR
                )
            )

            heatmap = (
                np.array(heatmap_image)
                / 255.0
            )

            # -----------------------------
            # Build top-3 result
            # -----------------------------

            top_3 = []

            for rank in range(3):

                index = (
                    top_indices[0][rank]
                    .item()
                )

                probability = (
                    top_probabilities[0][rank]
                    .item()
                )

                top_3.append(
                    {
                        "class": self.classes[index],
                        "confidence": probability,
                    }
                )

            # -----------------------------
            # Return everything
            # -----------------------------

            return {
                "class": predicted_class,
                "confidence": confidence,
                "top_3": top_3,
                "heatmap": heatmap,
            }

        finally:

            forward_handle.remove()
            backward_handle.remove()