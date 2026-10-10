from pathlib import Path

import torch
from torch.utils.data import DataLoader
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
import matplotlib.pyplot as plt

from plant_dataset import PlantDiseaseDataset
from image_transforms import val_test_transforms
from plant_model import create_model


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_ROOT = PROJECT_ROOT / "PlantVillage-Dataset"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
MODEL_DIR = PROJECT_ROOT / "models"

TEST_FILE = SPLITS_DIR / "color_test.txt"
MODEL_FILE = MODEL_DIR / "efficientnet_b0_finetuned.pth"

REPORT_FILE = PROJECT_ROOT / "data" / "test_classification_report.txt"
CONFUSION_FILE = PROJECT_ROOT / "data" / "confusion_matrix.png"


# =========================================
# Settings
# =========================================

BATCH_SIZE = 16
NUM_CLASSES = 38


# =========================================
# Device
# =========================================

device = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("Device:", device)

if device.type == "cuda":
    print("GPU:", torch.cuda.get_device_name(0))


# =========================================
# Load checkpoint
# =========================================

print()
print("Loading best model...")

checkpoint = torch.load(
    MODEL_FILE,
    map_location=device
)

class_to_idx = checkpoint["class_to_idx"]

classes = [
    class_name
    for class_name, _ in sorted(
        class_to_idx.items(),
        key=lambda item: item[1]
    )
]

print(
    "Best validation accuracy:",
    f"{checkpoint['val_accuracy']:.2f}%"
)

print(
    "Saved from epoch:",
    checkpoint["epoch"]
)


# =========================================
# Create test dataset
# =========================================

test_dataset = PlantDiseaseDataset(
    split_file=TEST_FILE,
    dataset_root=DATASET_ROOT,
    class_to_idx=class_to_idx,
    transform=val_test_transforms,
)


print()
print("Test images:", len(test_dataset))
print("Classes:", len(test_dataset.classes))


# =========================================
# Create DataLoader
# =========================================

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0,
    pin_memory=True,
)


# =========================================
# Create model
# =========================================

model = create_model(
    num_classes=NUM_CLASSES,
    freeze_backbone=True,
)

model.load_state_dict(
    checkpoint["model_state_dict"]
)

model = model.to(device)
model.eval()


# =========================================
# Evaluation
# =========================================

all_predictions = []
all_labels = []


print()
print("Starting test evaluation...")

with torch.inference_mode():

    for batch_index, (images, labels) in enumerate(
        test_loader
    ):

        images = images.to(
            device,
            non_blocking=True
        )

        outputs = model(images)

        predictions = outputs.argmax(dim=1)

        all_predictions.extend(
            predictions.cpu().tolist()
        )

        all_labels.extend(
            labels.tolist()
        )

        if (batch_index + 1) % 100 == 0:

            print(
                f"Processed "
                f"{(batch_index + 1) * BATCH_SIZE} "
                f"/ {len(test_dataset)} images"
            )


# =========================================
# Accuracy
# =========================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)


# =========================================
# Classification report
# =========================================

report = classification_report(
    all_labels,
    all_predictions,
    target_names=classes,
    digits=4,
    zero_division=0,
)


# =========================================
# Print results
# =========================================

print()
print("=" * 70)
print("TEST RESULTS")
print("=" * 70)

print(
    f"Test Accuracy: {accuracy * 100:.2f}%"
)

print()
print(report)


# =========================================
# Save classification report
# =========================================

REPORT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with open(
    REPORT_FILE,
    "w",
    encoding="utf-8"
) as f:

    f.write(
        f"Test Accuracy: "
        f"{accuracy * 100:.2f}%\n\n"
    )

    f.write(report)


# =========================================
# Confusion matrix
# =========================================

cm = confusion_matrix(
    all_labels,
    all_predictions
)


fig, ax = plt.subplots(
    figsize=(18, 16)
)

ax.imshow(cm)

ax.set_title(
    "Plant Disease Classification - Confusion Matrix"
)

ax.set_xlabel(
    "Predicted Class"
)

ax.set_ylabel(
    "Actual Class"
)

ax.set_xticks(
    range(len(classes))
)

ax.set_yticks(
    range(len(classes))
)

ax.set_xticklabels(
    classes,
    rotation=90,
    fontsize=7
)

ax.set_yticklabels(
    classes,
    fontsize=7
)

plt.tight_layout()

plt.savefig(
    CONFUSION_FILE,
    dpi=200,
    bbox_inches="tight"
)

plt.close()


# =========================================
# Finish
# =========================================

print()
print("Saved classification report:")
print(REPORT_FILE)

print()
print("Saved confusion matrix:")
print(CONFUSION_FILE)

print()
print("✅ Test evaluation completed!")