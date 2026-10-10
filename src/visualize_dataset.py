from pathlib import Path

import matplotlib.pyplot as plt
import torch
from torch.utils.data import DataLoader
from torchvision import transforms
from torchvision.utils import make_grid

from plant_dataset import PlantDiseaseDataset


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

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "sample_batch.png"
)


# ---------------------------------
# Image transformations
# ---------------------------------
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
])


# ---------------------------------
# Create dataset
# ---------------------------------
dataset = PlantDiseaseDataset(
    split_file=TRAIN_FILE,
    dataset_root=DATASET_ROOT,
    transform=transform,
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
# Get one batch
# ---------------------------------
images, labels = next(iter(loader))


print("Batch loaded successfully!")
print()
print("Image batch shape:", images.shape)
print("Label batch shape:", labels.shape)
print("Labels:", labels.tolist())

print()
print("Expected image shape:")
print("[batch_size, channels, height, width]")
print("[8, 3, 224, 224]")


# ---------------------------------
# Create image grid
# ---------------------------------
grid = make_grid(
    images,
    nrow=4,
    padding=2,
)


# Convert tensor → NumPy
grid_image = grid.permute(1, 2, 0).numpy()


# ---------------------------------
# Display
# ---------------------------------
plt.figure(figsize=(10, 7))

plt.imshow(grid_image)
plt.axis("off")
plt.title("PlantVillage Training Batch")

plt.tight_layout()

# Save image
OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True,
)

plt.savefig(
    OUTPUT_FILE,
    dpi=150,
    bbox_inches="tight",
)

print()
print(f"Saved visualization to:")
print(OUTPUT_FILE)

plt.show()