
import csv
import json
import copy
from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
from torch.utils.data import (
    Dataset,
    DataLoader,
    WeightedRandomSampler,
)
from PIL import Image
from sklearn.metrics import f1_score

from image_transforms import (
    train_transforms,
    val_test_transforms,
)
from plant_model import create_model


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMBINED_DIR = PROJECT_ROOT / "data" / "splits" / "combined"
MODELS_DIR = PROJECT_ROOT / "models"

SOURCE_CHECKPOINT = (
    MODELS_DIR / "efficientnet_b0_combined_55class.pth"
)

CLASS_MAPPING_FILE = (
    COMBINED_DIR / "combined_class_to_idx.json"
)

TRAIN_CSV = COMBINED_DIR / "combined_train.csv"
VAL_CSV = COMBINED_DIR / "combined_val.csv"

BEST_MODEL_PATH = (
    MODELS_DIR / "efficientnet_b0_combined_balanced_best.pth"
)

LATEST_MODEL_PATH = (
    MODELS_DIR / "efficientnet_b0_combined_balanced_last.pth"
)


# =========================================
# Configuration
# =========================================

BATCH_SIZE = 8
NUM_EPOCHS = 3
NUM_WORKERS = 2

BACKBONE_LR = 5e-6
CLASSIFIER_LR = 2e-5
WEIGHT_DECAY = 1e-4

LOG_EVERY = 200
SEED = 42


# =========================================
# Dataset
# =========================================

class CombinedPlantDataset(Dataset):

    def __init__(self, csv_path, class_to_idx, transform=None):

        self.rows = []
        self.transform = transform

        with open(
            csv_path,
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            reader = csv.DictReader(file)

            for row in reader:

                class_name = row["class_name"]
                label = int(row["class_idx"])
                image_path = Path(row["image_path"])

                if class_name not in class_to_idx:
                    raise ValueError(
                        f"Unknown class: {class_name}"
                    )

                if class_to_idx[class_name] != label:
                    raise ValueError(
                        f"Incorrect label index: {class_name}"
                    )

                if not image_path.is_file():
                    raise FileNotFoundError(
                        f"Image not found: {image_path}"
                    )

                self.rows.append({
                    "path": image_path,
                    "class_name": class_name,
                    "label": label,
                })

        if not self.rows:
            raise ValueError(
                f"No images found in {csv_path}"
            )

        self.labels = [
            row["label"] for row in self.rows
        ]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):

        row = self.rows[index]

        with Image.open(row["path"]) as source:
            image = source.convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        return image, row["label"]


# =========================================
# Save checkpoint
# =========================================

def save_checkpoint(
    path,
    model,
    class_to_idx,
    epoch,
    val_accuracy,
    val_macro_f1,
    val_loss,
):

    path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "class_to_idx": class_to_idx,
            "classes": [
                name
                for name, _ in sorted(
                    class_to_idx.items(),
                    key=lambda item: item[1],
                )
            ],
            "num_classes": len(class_to_idx),
            "epoch": epoch,
            "val_accuracy": val_accuracy,
            "val_macro_f1": val_macro_f1,
            "val_loss": val_loss,
            "source_checkpoint": str(SOURCE_CHECKPOINT),
            "sampling_strategy": "inverse_sqrt_class_frequency",
        },
        path,
    )


# =========================================
# Main
# =========================================

def main():

    print("=" * 65)
    print("BALANCED FINE-TUNING — 55 CLASSES")
    print("=" * 65)

    # -------------------------------------
    # Reproducibility
    # -------------------------------------

    torch.manual_seed(SEED)

    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(SEED)

    # -------------------------------------
    # Device
    # -------------------------------------

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    use_amp = device.type == "cuda"

    print("\nDevice:", device)

    if use_amp:
        print("GPU:", torch.cuda.get_device_name(0))

    # -------------------------------------
    # Check required files
    # -------------------------------------

    for path in [
        SOURCE_CHECKPOINT,
        CLASS_MAPPING_FILE,
        TRAIN_CSV,
        VAL_CSV,
    ]:

        if not path.is_file():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

    # -------------------------------------
    # Load mapping
    # -------------------------------------

    with open(
        CLASS_MAPPING_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        class_to_idx = json.load(file)

    class_to_idx = {
        name: int(index)
        for name, index in class_to_idx.items()
    }

    number_of_classes = len(class_to_idx)

    if sorted(class_to_idx.values()) != list(
        range(number_of_classes)
    ):
        raise ValueError(
            "Class indices are not contiguous."
        )

    print("Classes:", number_of_classes)

    # -------------------------------------
    # Load datasets
    # -------------------------------------

    print("\nLoading datasets...")

    train_dataset = CombinedPlantDataset(
        TRAIN_CSV,
        class_to_idx,
        transform=train_transforms,
    )

    val_dataset = CombinedPlantDataset(
        VAL_CSV,
        class_to_idx,
        transform=val_test_transforms,
    )

    train_paths = {
        str(row["path"].resolve())
        for row in train_dataset.rows
    }

    val_paths = {
        str(row["path"].resolve())
        for row in val_dataset.rows
    }

    if train_paths & val_paths:
        raise ValueError(
            "Training and validation share image paths."
        )

    print("Training images:", f"{len(train_dataset):,}")
    print("Validation images:", f"{len(val_dataset):,}")

    # -------------------------------------
    # Compute smoothed sampling weights
    # -------------------------------------

    class_counts = Counter(
        train_dataset.labels
    )

    for class_index in range(number_of_classes):

        if class_counts[class_index] == 0:
            raise ValueError(
                f"Class {class_index} has no training images."
            )

    # A sample from a rare class gets a larger weight.
    # Inverse square root is less aggressive than full inverse
    # frequency balancing and helps limit extreme oversampling.
    sample_weights = [
        1.0 / (class_counts[label] ** 0.5)
        for label in train_dataset.labels
    ]

    generator = torch.Generator()
    generator.manual_seed(SEED)

    sampler = WeightedRandomSampler(
        weights=torch.as_tensor(
            sample_weights,
            dtype=torch.double,
        ),
        num_samples=len(train_dataset),
        replacement=True,
        generator=generator,
    )

    print("\nBalanced sampler ready.")

    print("Sampling uses inverse square-root class frequency.")
    print("Training draws per epoch:", f"{len(train_dataset):,}")
    print(
        "Some images may be sampled more than once per epoch."
    )

    # -------------------------------------
    # DataLoaders
    # -------------------------------------

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        sampler=sampler,
        num_workers=NUM_WORKERS,
        pin_memory=use_amp,
        persistent_workers=NUM_WORKERS > 0,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=use_amp,
        persistent_workers=NUM_WORKERS > 0,
    )

    # -------------------------------------
    # Load current 55-class checkpoint
    # -------------------------------------

    print("\nLoading current 55-class model...")

    checkpoint = torch.load(
        SOURCE_CHECKPOINT,
        map_location="cpu",
        weights_only=False,
    )

    checkpoint_mapping = {
        name: int(index)
        for name, index
        in checkpoint["class_to_idx"].items()
    }

    if checkpoint_mapping != class_to_idx:
        raise ValueError(
            "Checkpoint and dataset class mappings differ."
        )

    model = create_model(
        num_classes=number_of_classes,
        freeze_backbone=False,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True,
    )

    # -------------------------------------
    # Trainable layers
    # -------------------------------------

    for parameter in model.parameters():
        parameter.requires_grad = False

    for parameter in model.features[6:].parameters():
        parameter.requires_grad = True

    for parameter in model.classifier.parameters():
        parameter.requires_grad = True

    model = model.to(device)

    print("Loaded checkpoint epoch:", checkpoint["epoch"])
    print("Existing validation accuracy:", checkpoint["val_accuracy"])
    print("Starting fine-tuning from the current 55-class model.")

    # -------------------------------------
    # Loss and optimizer
    # -------------------------------------

    # The sampler already adjusts class exposure.
    # Use ordinary cross-entropy here to avoid multiplying
    # the imbalance correction twice.
    criterion = nn.CrossEntropyLoss()

    optimizer = torch.optim.AdamW(
        [
            {
                "params": model.features[6:].parameters(),
                "lr": BACKBONE_LR,
            },
            {
                "params": model.classifier.parameters(),
                "lr": CLASSIFIER_LR,
            },
        ],
        weight_decay=WEIGHT_DECAY,
    )

    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=use_amp,
    )

    # Select the best checkpoint using validation macro F1.
    best_val_macro_f1 = -1.0

    # =====================================
    # Training epochs
    # =====================================

    for epoch in range(NUM_EPOCHS):

        print("\n" + "=" * 65)
        print(f"EPOCH {epoch + 1}/{NUM_EPOCHS}")
        print("=" * 65)

        # ---------------------------------
        # Training
        # ---------------------------------

        model.train()

        # Keep frozen early feature blocks in evaluation mode.
        for layer in model.features[:6]:
            layer.eval()

        running_loss = 0.0
        train_correct = 0
        train_total = 0

        for batch_index, (images, labels) in enumerate(
            train_loader,
            start=1,
        ):

            images = images.to(
                device,
                non_blocking=True,
            )

            labels = labels.to(
                device,
                non_blocking=True,
            )

            optimizer.zero_grad(set_to_none=True)

            with torch.autocast(
                device_type="cuda",
                dtype=torch.float16,
                enabled=use_amp,
            ):

                outputs = model(images)

                loss = criterion(
                    outputs,
                    labels,
                )

            scaler.scale(loss).backward()
            scaler.step(optimizer)
            scaler.update()

            running_loss += loss.item()

            predictions = outputs.argmax(dim=1)

            train_correct += (
                predictions == labels
            ).sum().item()

            train_total += labels.size(0)

            if batch_index % LOG_EVERY == 0:

                print(
                    f"Batch {batch_index:4d}/{len(train_loader)}"
                    f" | Loss: {running_loss / batch_index:.4f}"
                    f" | Accuracy: "
                    f"{100 * train_correct / train_total:.2f}%"
                )

        train_loss = (
            running_loss / len(train_loader)
        )

        train_accuracy = (
            100 * train_correct / train_total
        )

        # ---------------------------------
        # Validation
        # ---------------------------------

        model.eval()

        val_loss_total = 0.0
        val_correct = 0
        val_total = 0

        true_labels = []
        predicted_labels = []

        with torch.inference_mode():

            for images, labels in val_loader:

                images = images.to(
                    device,
                    non_blocking=True,
                )

                labels_device = labels.to(
                    device,
                    non_blocking=True,
                )

                with torch.autocast(
                    device_type="cuda",
                    dtype=torch.float16,
                    enabled=use_amp,
                ):

                    outputs = model(images)

                    loss = criterion(
                        outputs,
                        labels_device,
                    )

                val_loss_total += loss.item()

                predictions = outputs.argmax(dim=1)

                val_correct += (
                    predictions == labels_device
                ).sum().item()

                val_total += labels_device.size(0)

                true_labels.extend(
                    labels.tolist()
                )

                predicted_labels.extend(
                    predictions.cpu().tolist()
                )

        val_loss = (
            val_loss_total / len(val_loader)
        )

        val_accuracy = (
            100 * val_correct / val_total
        )

        val_macro_f1 = f1_score(
            true_labels,
            predicted_labels,
            labels=list(range(number_of_classes)),
            average="macro",
            zero_division=0,
        )

        # ---------------------------------
        # Print metrics
        # ---------------------------------

        print("\nEpoch results:")

        print(f"Train loss:       {train_loss:.4f}")
        print(f"Train accuracy:   {train_accuracy:.2f}%")
        print(f"Validation loss:  {val_loss:.4f}")
        print(f"Validation accuracy: {val_accuracy:.2f}%")
        print(f"Validation macro F1: {val_macro_f1 * 100:.2f}%")

        # ---------------------------------
        # Save latest checkpoint
        # ---------------------------------

        save_checkpoint(
            LATEST_MODEL_PATH,
            model,
            class_to_idx,
            epoch + 1,
            val_accuracy,
            val_macro_f1,
            val_loss,
        )

        # ---------------------------------
        # Save best macro-F1 checkpoint
        # ---------------------------------

        if val_macro_f1 > best_val_macro_f1:

            best_val_macro_f1 = val_macro_f1

            save_checkpoint(
                BEST_MODEL_PATH,
                model,
                class_to_idx,
                epoch + 1,
                val_accuracy,
                val_macro_f1,
                val_loss,
            )

            print("\nBest balanced model saved:")
            print(BEST_MODEL_PATH)

        print("\nOriginal combined checkpoint remains untouched.")

    # =====================================
    # Complete
    # =====================================

    print("\n" + "=" * 65)
    print("BALANCED FINE-TUNING COMPLETE")
    print("=" * 65)

    print(
        "Best validation macro F1:",
        f"{best_val_macro_f1 * 100:.2f}%",
    )

    print("\nBest model:")
    print(BEST_MODEL_PATH)

    print("\nLatest model:")
    print(LATEST_MODEL_PATH)

    print(
        "\nNo test images were used during this training run."
    )


if __name__ == "__main__":
    main()
