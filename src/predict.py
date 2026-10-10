from pathlib import Path
import sys

import torch
from PIL import Image
from torchvision.transforms import Compose

from plant_model import create_model
from image_transforms import val_test_transforms


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_FILE = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_finetuned.pth"
)


# =========================================
# Device
# =========================================

device = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


# =========================================
# Check command-line argument
# =========================================

if len(sys.argv) != 2:

    print()
    print("Usage:")
    print(
        'python src/predict.py "path\\to\\image.jpg"'
    )
    print()

    sys.exit(1)


image_path = Path(sys.argv[1])


if not image_path.exists():

    print()
    print(
        f"ERROR: Image not found:\n{image_path}"
    )
    print()

    sys.exit(1)


# =========================================
# Load checkpoint
# =========================================

print("Loading model...")

checkpoint = torch.load(
    MODEL_FILE,
    map_location=device
)


# =========================================
# Class mapping
# =========================================

class_to_idx = checkpoint["class_to_idx"]

classes = [
    class_name
    for class_name, _ in sorted(
        class_to_idx.items(),
        key=lambda item: item[1]
    )
]


# =========================================
# Create model
# =========================================

model = create_model(
    num_classes=len(classes),
    freeze_backbone=False
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)

model.eval()


# =========================================
# Load image
# =========================================

print("Loading image...")

image = Image.open(
    image_path
).convert("RGB")


print(
    f"Image size: {image.size}"
)


# =========================================
# Transform image
# =========================================

image_tensor = val_test_transforms(
    image
)

image_tensor = image_tensor.unsqueeze(0)

image_tensor = image_tensor.to(device)


# =========================================
# Prediction
# =========================================

with torch.inference_mode():

    outputs = model(
        image_tensor
    )

    probabilities = torch.softmax(
        outputs,
        dim=1
    )

    top_probabilities, top_indices = (
        probabilities.topk(3, dim=1)
    )


# =========================================
# Print results
# =========================================

print()
print("=" * 60)
print("PLANT DISEASE PREDICTION")
print("=" * 60)

print()
print("Image:")
print(image_path)

print()

for rank in range(3):

    index = top_indices[0][rank].item()

    probability = (
        top_probabilities[0][rank].item()
        * 100
    )

    print(
        f"{rank + 1}. "
        f"{classes[index]} "
        f"→ {probability:.2f}%"
    )


# =========================================
# Best prediction
# =========================================

best_index = top_indices[0][0].item()

best_probability = (
    top_probabilities[0][0].item()
    * 100
)

best_class = classes[best_index]


print()
print("=" * 60)

print(
    f"Prediction: {best_class}"
)

print(
    f"Confidence: {best_probability:.2f}%"
)

print("=" * 60)