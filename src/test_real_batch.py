from pathlib import Path

import torch
from torch.utils.data import DataLoader

from plant_dataset import PlantDiseaseDataset
from image_transforms import train_transforms
from plant_model import create_model


# ---------------------------------
# Project paths
# ---------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "splits"
    / "color_train_final.txt"
)

DATASET_ROOT = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
)


# ---------------------------------
# Device
# ---------------------------------
device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

if device.type == "cuda":
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# ---------------------------------
# Create dataset
# ---------------------------------
dataset = PlantDiseaseDataset(
    split_file=TRAIN_FILE,
    dataset_root=DATASET_ROOT,
    transform=train_transforms,
)


# ---------------------------------
# Create DataLoader
# ---------------------------------
loader = DataLoader(
    dataset,
    batch_size=8,
    shuffle=True,
    num_workers=0,
)


# ---------------------------------
# Load one real batch
# ---------------------------------
images, labels = next(iter(loader))

print()
print("Real batch loaded!")
print("Images:", images.shape)
print("Labels:", labels.shape)


# ---------------------------------
# Move batch to GPU
# ---------------------------------
images = images.to(device)
labels = labels.to(device)

print()
print("Images device:", images.device)
print("Labels device:", labels.device)


# ---------------------------------
# Create model
# ---------------------------------
model = create_model(
    num_classes=38,
    freeze_backbone=True,
)

model = model.to(device)

model.eval()


# ---------------------------------
# Forward pass
# ---------------------------------
with torch.no_grad():
    outputs = model(images)


# ---------------------------------
# Get predictions
# ---------------------------------
predictions = outputs.argmax(dim=1)


print()
print("Forward pass successful!")
print("Outputs shape:", outputs.shape)

print()
print("Actual labels:    ", labels.tolist())
print("Predicted labels: ", predictions.tolist())


# ---------------------------------
# Show class names
# ---------------------------------
print()
print("Actual classes:")

for label in labels[:8]:
    print(
        " -",
        dataset.classes[label.item()]
    )

print()
print("Predicted classes:")

for prediction in predictions[:8]:
    print(
        " -",
        dataset.classes[prediction.item()]
    )


# ---------------------------------
# GPU memory
# ---------------------------------
if device.type == "cuda":
    memory_used = torch.cuda.memory_allocated() / (
        1024 ** 2
    )

    print()
    print(
        f"GPU memory allocated: "
        f"{memory_used:.1f} MB"
    )

print()
print("✅ Real image → model test passed!")