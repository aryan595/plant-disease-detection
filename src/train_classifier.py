from pathlib import Path
from collections import Counter

import torch
import torch.nn as nn
from torch.utils.data import DataLoader

from plant_dataset import PlantDiseaseDataset
from image_transforms import (
    train_transforms,
    val_test_transforms,
)
from plant_model import create_model


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
DATASET_ROOT = PROJECT_ROOT / "PlantVillage-Dataset"
MODEL_DIR = PROJECT_ROOT / "models"

TRAIN_FILE = SPLITS_DIR / "color_train_final.txt"
VAL_FILE = SPLITS_DIR / "color_val.txt"


# =========================================
# Settings
# =========================================

NUM_CLASSES = 38

BATCH_SIZE = 16
NUM_EPOCHS = 5

LEARNING_RATE = 0.001

NUM_WORKERS = 2

MODEL_NAME = "efficientnet_b0_classifier_fast.pth"


# =========================================
# Main
# =========================================

def main():

    # =====================================
    # Device
    # =====================================

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    print("Device:", device)

    if device.type == "cuda":
        print(
            "GPU:",
            torch.cuda.get_device_name(0)
        )


    # =====================================
    # Dataset
    # =====================================

    train_dataset = PlantDiseaseDataset(
        split_file=TRAIN_FILE,
        dataset_root=DATASET_ROOT,
        transform=train_transforms,
    )

    val_dataset = PlantDiseaseDataset(
        split_file=VAL_FILE,
        dataset_root=DATASET_ROOT,
        class_to_idx=train_dataset.class_to_idx,
        transform=val_test_transforms,
    )


    print()
    print(
        "Training images  :",
        len(train_dataset)
    )

    print(
        "Validation images:",
        len(val_dataset)
    )

    print(
        "Classes          :",
        len(train_dataset.classes)
    )


    # =====================================
    # DataLoaders
    # =====================================

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        persistent_workers=True,
    )

    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=True,
        persistent_workers=True,
    )


    # =====================================
    # Class weights
    # =====================================

    class_counts = Counter(
        train_dataset.labels
    )

    counts = torch.tensor(
        [
            class_counts[index]
            for index in range(NUM_CLASSES)
        ],
        dtype=torch.float32,
    )

    class_weights = 1.0 / counts

    class_weights = (
        class_weights
        / class_weights.mean()
    )

    class_weights = class_weights.to(device)


    print()
    print("Class weights calculated.")


    # =====================================
    # Model
    # =====================================

    model = create_model(
        num_classes=NUM_CLASSES,
        freeze_backbone=True,
    )

    model = model.to(device)


    # =====================================
    # Loss
    # =====================================

    criterion = nn.CrossEntropyLoss(
        weight=class_weights
    )


    # =====================================
    # Optimizer
    # =====================================

    optimizer = torch.optim.Adam(
        model.classifier.parameters(),
        lr=LEARNING_RATE,
    )


    # =====================================
    # AMP
    # =====================================

    use_amp = device.type == "cuda"

    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=use_amp,
    )


    # =====================================
    # Best model
    # =====================================

    best_val_accuracy = 0.0


    # =====================================
    # Training
    # =====================================

    for epoch in range(NUM_EPOCHS):

        print()
        print("=" * 70)

        print(
            f"Epoch {epoch + 1}/{NUM_EPOCHS}"
        )

        print("=" * 70)


        # ---------------------------------
        # TRAIN
        # ---------------------------------

        model.train()

        running_loss = 0.0

        correct = 0
        total = 0

        total_batches = len(train_loader)


        for batch_index, (images, labels) in enumerate(
            train_loader,
            start=1
        ):

            images = images.to(
                device,
                non_blocking=True
            )

            labels = labels.to(
                device,
                non_blocking=True
            )


            optimizer.zero_grad(
                set_to_none=True
            )


            # -----------------------------
            # Mixed precision forward pass
            # -----------------------------

            with torch.autocast(
                device_type="cuda",
                dtype=torch.float16,
                enabled=use_amp,
            ):

                outputs = model(images)

                loss = criterion(
                    outputs,
                    labels
                )


            # -----------------------------
            # Backward + optimizer
            # -----------------------------

            scaler.scale(
                loss
            ).backward()

            scaler.step(
                optimizer
            )

            scaler.update()


            # -----------------------------
            # Statistics
            # -----------------------------

            running_loss += loss.item()

            predictions = outputs.argmax(
                dim=1
            )

            correct += (
                predictions == labels
            ).sum().item()

            total += labels.size(0)


            # -----------------------------
            # Progress
            # -----------------------------

            if batch_index % 100 == 0:

                current_loss = (
                    running_loss
                    / batch_index
                )

                current_accuracy = (
                    correct
                    / total
                ) * 100

                print(
                    f"Batch "
                    f"{batch_index:4d}/{total_batches} "
                    f"| Loss: "
                    f"{current_loss:.4f} "
                    f"| Acc: "
                    f"{current_accuracy:.2f}%"
                )


        train_loss = (
            running_loss
            / total_batches
        )

        train_accuracy = (
            correct
            / total
        ) * 100


        # ---------------------------------
        # VALIDATION
        # ---------------------------------

        model.eval()

        val_loss_total = 0.0

        val_correct = 0
        val_total = 0


        with torch.inference_mode():

            for images, labels in val_loader:

                images = images.to(
                    device,
                    non_blocking=True
                )

                labels = labels.to(
                    device,
                    non_blocking=True
                )


                with torch.autocast(
                    device_type="cuda",
                    dtype=torch.float16,
                    enabled=use_amp,
                ):

                    outputs = model(images)

                    loss = criterion(
                        outputs,
                        labels
                    )


                val_loss_total += (
                    loss.item()
                )

                predictions = outputs.argmax(
                    dim=1
                )

                val_correct += (
                    predictions == labels
                ).sum().item()

                val_total += labels.size(0)


        val_loss = (
            val_loss_total
            / len(val_loader)
        )

        val_accuracy = (
            val_correct
            / val_total
        ) * 100


        # ---------------------------------
        # Results
        # ---------------------------------

        print()

        print(
            f"Train Loss:     {train_loss:.4f}"
        )

        print(
            f"Train Accuracy: {train_accuracy:.2f}%"
        )

        print(
            f"Val Loss:       {val_loss:.4f}"
        )

        print(
            f"Val Accuracy:   {val_accuracy:.2f}%"
        )


        # ---------------------------------
        # Save best model
        # ---------------------------------

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            MODEL_DIR.mkdir(
                parents=True,
                exist_ok=True
            )

            model_path = (
                MODEL_DIR
                / MODEL_NAME
            )

            torch.save(
                {
                    "model_state_dict":
                        model.state_dict(),

                    "class_to_idx":
                        train_dataset.class_to_idx,

                    "val_accuracy":
                        val_accuracy,

                    "epoch":
                        epoch + 1,
                },
                model_path,
            )

            print()
            print("✅ Best model saved!")

            print(
                "Path:",
                model_path
            )


    # =====================================
    # Finish
    # =====================================

    print()
    print("=" * 70)

    print("Training completed!")

    print("=" * 70)

    print(
        f"Best validation accuracy: "
        f"{best_val_accuracy:.2f}%"
    )


if __name__ == "__main__":
    main()