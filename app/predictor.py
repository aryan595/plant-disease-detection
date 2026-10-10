
from pathlib import Path

import torch
from PIL import Image

from src.plant_model import create_model
from src.image_transforms import val_test_transforms


class PlantDiseasePredictor:
    """
    Loads the expanded 55-class plant disease model
    and predicts the top three classes for an image.
    """

    def __init__(self):

        # =====================================
        # Paths
        # =====================================

        project_root = Path(__file__).resolve().parent.parent

        self.model_file = (
            project_root
            / "models"
            / "efficientnet_b0_combined_balanced_best.pth"
        )

        # =====================================
        # Device
        # =====================================

        self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        print("Loading expanded plant disease model...")
        print("Checkpoint:", self.model_file)
        print("Device:", self.device)

        if self.device.type == "cuda":
            print(
                "GPU:",
                torch.cuda.get_device_name(0),
            )

        # =====================================
        # Check checkpoint
        # =====================================

        if not self.model_file.is_file():
            raise FileNotFoundError(
                "Expanded model checkpoint not found: "
                f"{self.model_file}"
            )

        # This is a checkpoint created by our own training script.
        checkpoint = torch.load(
            self.model_file,
            map_location="cpu",
            weights_only=False,
        )

        if "model_state_dict" not in checkpoint:
            raise ValueError(
                "Checkpoint does not contain model_state_dict."
            )

        if "class_to_idx" not in checkpoint:
            raise ValueError(
                "Checkpoint does not contain class_to_idx."
            )

        # =====================================
        # Load class mapping
        # =====================================

        self.class_to_idx = {
            class_name: int(index)
            for class_name, index
            in checkpoint["class_to_idx"].items()
        }

        self.classes = [
            class_name
            for class_name, _ in sorted(
                self.class_to_idx.items(),
                key=lambda item: item[1],
            )
        ]

        if sorted(self.class_to_idx.values()) != list(
            range(len(self.classes))
        ):
            raise ValueError(
                "The checkpoint contains invalid class indices."
            )

        if (
            "num_classes" in checkpoint
            and int(checkpoint["num_classes"]) != len(self.classes)
        ):
            raise ValueError(
                "Checkpoint num_classes does not match its mapping."
            )

        expected_classes = 55

        if len(self.classes) != expected_classes:
            raise ValueError(
                f"Expected {expected_classes} classes, "
                f"but checkpoint contains {len(self.classes)}."
            )

        # =====================================
        # Create expanded model
        # =====================================

        self.model = create_model(
            num_classes=len(self.classes),
            freeze_backbone=False,
        )

        # Strict loading ensures that the model architecture
        # and checkpoint weights match exactly.
        self.model.load_state_dict(
            checkpoint["model_state_dict"],
            strict=True,
        )

        self.model = self.model.to(self.device)
        self.model.eval()

        # =====================================
        # Confirm successful loading
        # =====================================

        print("Expanded model loaded successfully.")
        print("Model: EfficientNet-B0")
        print("Number of classes:", len(self.classes))

        print(
            "Validation accuracy recorded in checkpoint:",
            f"{checkpoint.get('val_accuracy', 0):.2f}%",
        )

        print(
            "Checkpoint epoch:",
            checkpoint.get("epoch", "unknown"),
        )

        print("First five classes:")

        for class_name in self.classes[:5]:
            print("  ", class_name)

        print("PlantDiseasePredictor ready.")

    # =====================================
    # Predict
    # =====================================

    def predict(self, image: Image.Image):

        image = image.convert("RGB")

        # -------------------------------------
        # Apply inference transformations
        # -------------------------------------

        tensor = val_test_transforms(image)

        tensor = tensor.unsqueeze(0).to(self.device)

        # -------------------------------------
        # Run inference
        # -------------------------------------

        with torch.inference_mode():

            outputs = self.model(tensor)

            probabilities = torch.softmax(
                outputs,
                dim=1,
            )

            top_probabilities, top_indices = (
                probabilities.topk(
                    min(3, len(self.classes)),
                    dim=1,
                )
            )

        # -------------------------------------
        # Return top predictions
        # -------------------------------------

        results = []

        for rank in range(top_indices.shape[1]):

            index = top_indices[0, rank].item()

            probability = (
                top_probabilities[0, rank].item()
            )

            results.append({
                "class": self.classes[index],
                "confidence": probability,
            })

        return results
