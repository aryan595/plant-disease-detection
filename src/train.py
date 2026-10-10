from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import DataLoader
from torchvision import transforms

from plant_dataset import PlantDiseaseDataset
from image_transforms import train_transforms
from plant_model import create_model


# =========================================
# Project paths
# =========================================

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


# =========================================
# Training settings
# =========================================

BATCH_SIZE = 8
LEARNING_RATE = 0.001

NUM_CLASSES = 38

# Safety test: only train 100 batches
MAX_BATCHES = 100


# =========================================
# Device
# =========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

if device.type == "cuda":
    print(
        "GPU:",
        torch.cuda.get_device_name(0)
    )


# =========================================
# Dataset
# =========================================

train_dataset = PlantDiseaseDataset(
    split_file=TRAIN_FILE,
    dataset_root=DATASET_ROOT,
    transform=train_transforms,
)


print()
print("Training images:", len(train_dataset))
print("Classes:", len(train_dataset.classes))


# =========================================
# DataLoader
# =========================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0,
    pin_memory=True,
)


# =========================================
# Model
# =========================================

model = create_model(
    num_classes=NUM_CLASSES,
    freeze_backbone=True,
)

model = model.to(device)


# =========================================
# Loss
# =========================================

criterion = nn.CrossEntropyLoss()


# =========================================
# Optimizer
# =========================================

optimizer = torch.optim.Adam(
    model.classifier.parameters(),
    lr=LEARNING_RATE,
)


# =========================================
# Training
# =========================================

model.train()

running_loss = 0.0

print()
print("Starting training test...")
print()


for batch_index, (images, labels) in enumerate(train_loader):

    # -------------------------------------
    # Stop after MAX_BATCHES
    # -------------------------------------

    if batch_index >= MAX_BATCHES:
        break


    # -------------------------------------
    # Move data to GPU
    # -------------------------------------

    images = images.to(
        device,
        non_blocking=True
    )

    labels = labels.to(
        device,
        non_blocking=True
    )


    # -------------------------------------
    # Clear previous gradients
    # -------------------------------------

    optimizer.zero_grad()


    # -------------------------------------
    # Forward pass
    # -------------------------------------

    outputs = model(images)


    # -------------------------------------
    # Calculate loss
    # -------------------------------------

    loss = criterion(
        outputs,
        labels
    )


    # -------------------------------------
    # Backpropagation
    # -------------------------------------

    loss.backward()


    # -------------------------------------
    # Update weights
    # -------------------------------------

    optimizer.step()


    # -------------------------------------
    # Track loss
    # -------------------------------------

    running_loss += loss.item()


    # -------------------------------------
    # Print progress
    # -------------------------------------

    if (batch_index + 1) % 10 == 0:

        average_loss = (
            running_loss
            / (batch_index + 1)
        )

        print(
            f"Batch "
            f"{batch_index + 1:3d}/{MAX_BATCHES} "
            f"| Loss: {average_loss:.4f}"
        )


# =========================================
# Finish
# =========================================

average_loss = (
    running_loss / MAX_BATCHES
)

print()
print("=" * 50)
print("Training test completed!")
print("=" * 50)

print(
    f"Average loss: {average_loss:.4f}"
)

if device.type == "cuda":

    memory_used = (
        torch.cuda.max_memory_allocated()
        / (1024 ** 2)
    )

    print(
        f"Peak GPU memory: "
        f"{memory_used:.1f} MB"
    )

print()
print("✅ Forward + backward + optimizer test passed!")