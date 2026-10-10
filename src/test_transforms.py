from pathlib import Path

import torch
from torchvision import transforms

from plant_dataset import PlantDiseaseDataset
from image_transforms import (
    train_transforms,
    val_test_transforms,
)


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
# Create training dataset
# ---------------------------------
train_dataset = PlantDiseaseDataset(
    split_file=TRAIN_FILE,
    dataset_root=DATASET_ROOT,
    transform=train_transforms,
)


# ---------------------------------
# Load one image
# ---------------------------------
image, label = train_dataset[0]


print("Transform test successful!")
print()
print("Tensor type:", type(image))
print("Tensor shape:", image.shape)
print("Label:", label)
print("Tensor dtype:", image.dtype)
print("Tensor device:", image.device)


# ---------------------------------
# Check values
# ---------------------------------
print()
print("Minimum value:", image.min().item())
print("Maximum value:", image.max().item())


# ---------------------------------
# Verify tensor
# ---------------------------------
assert isinstance(image, torch.Tensor)
assert image.shape == (3, 224, 224)

print()
print("All checks passed! ✅")