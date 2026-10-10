
import csv
import json
from collections import Counter
from pathlib import Path

import torch
import torch.nn as nn
from PIL import Image
from torch.utils.data import Dataset, DataLoader

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
    MODELS_DIR / "efficientnet_b0_finetuned.pth"
)

CLASS_MAPPING_FILE = (
    COMBINED_DIR / "combined_class_to_idx.json"
)

TRAIN_CSV = COMBINED_DIR / "combined_train.csv"
VAL_CSV = COMBINED_DIR / "combined_val.csv"
TEST_CSV = COMBINED_DIR / "combined_test.csv"

BEST_MODEL_PATH = (
    MODELS_DIR / "efficientnet_b0_combined_55class.pth"
)

LATEST_MODEL_PATH = (
    MODELS_DIR / "efficientnet_b0_combined_55class_last.pth"
)


# =========================================
# Configuration
# =========================================

BATCH_SIZE = 8
NUM_EPOCHS = 3
NUM_WORKERS = 2

BACKBONE_LEARNING_RATE = 1e-5
CLASSIFIER_LEARNING_RATE = 1e-4
WEIGHT_DECAY = 1e-4

LOG_EVERY = 200


# =========================================
# Dataset
# =========================================

class CombinedPlantDataset(Dataset):

    def __init__(self, csv_path, class_to_idx, transform=None):

        self.csv_path = Path(csv_path)
        self.transform = transform
        self.rows = []

        with open(
            self.csv_path,
            "r",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            reader = csv.DictReader(file)

            required_columns = {
                "image_path",
                "class_name",
                "class_idx",
            }

            missing = required_columns - set(
                reader.fieldnames or []
            )

            if missing:
                raise ValueError(
                    f"Missing CSV columns in {self.csv_path}: "
                    f"{sorted(missing)}"
                )

            for row in reader:

                class_name = row["class_name"]
                class_idx = int(row["class_idx"])
                image_path = Path(row["image_path"])

                if class_name not in class_to_idx:
                    raise ValueError(
                        f"Unknown class: {class_name}"
                    )

                if class_to_idx[class_name] != class_idx:
                    raise ValueError(
                        f"Class index mismatch for {class_name}"
                    )

                if not image_path.is_file():
                    raise FileNotFoundError(
                        f"Image not found: {image_path}"
                    )

                self.rows.append({
                    "image_path": image_path,
                    "class_name": class_name,
                    "label": class_idx,
                })

        if not self.rows:
            raise ValueError(
                f"No images found in {self.csv_path}"
            )

        self.labels = [
            row["label"] for row in self.rows
        ]

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):

        row = self.rows[index]

        try:
            with Image.open(row["image_path"]) as opened:
                image = opened.convert("RGB")

        except Exception as exc:
            raise RuntimeError(
                f"Could not read image: {row['image_path']}"
            ) from exc

        if self.transform is not None:
            image = self.transform(image)

        return image, row["label"]


# =========================================
# Validate splits
# =========================================

def validate_splits(
    train_dataset,
    val_dataset,
    test_dataset,
    class_to_idx,
):

    paths = {}

    for split_name, dataset in [
        ("training", train_dataset),
        ("validation", val_dataset),
        ("test", test_dataset),
    ]:

        paths[split_name] = {
            str(row["image_path"].resolve())
            for row in dataset.rows
        }

        present_classes = {
            row["class_name"]
            for row in dataset.rows
        }

        missing_classes = (
            set(class_to_idx) - present_classes
        )

        if missing_classes:
            raise ValueError(
                f"{split_name} split is missing classes: "
                f"{sorted(missing_classes)}"
            )

    if paths["training"] & paths["validation"]:
        raise ValueError(
            "Training and validation share image paths."
        )

    if paths["training"] & paths["test"]:
        raise ValueError(
            "Training and test share image paths."
        )

    if paths["validation"] & paths["test"]:
        raise ValueError(
            "Validation and test share image paths."
        )

    print("Split validation passed.")
    print("No exact image paths are shared between splits.")
    print(
        "Test images:",
        f"{len(test_dataset):,}",
        "(reserved for final evaluation)",
    )


# =========================================
# Initialize expanded model
# =========================================

def initialize_expanded_model(class_to_idx, device):

    print("\nLoading existing fine-tuned checkpoint...")

    checkpoint = torch.load(
        SOURCE_CHECKPOINT,
        map_location="cpu",
        weights_only=False,
    )

    old_state = checkpoint["model_state_dict"]

    old_class_to_idx = {
        name: int(index)
        for name, index in checkpoint["class_to_idx"].items()
    }

    # Verify that every original class retains its index.
    for class_name, old_index in old_class_to_idx.items():

        if class_name not in class_to_idx:
            raise ValueError(
                f"Original class missing: {class_name}"
            )

        if class_to_idx[class_name] != old_index:
            raise ValueError(
                f"Original class index changed: {class_name}"
            )

    number_of_classes = len(class_to_idx)

    print("Existing classes:", len(old_class_to_idx))
    print("Expanded classes:", number_of_classes)

    # Create the new model with 55 output classes.
    model = create_model(
        num_classes=number_of_classes,
        freeze_backbone=False,
    )

    new_state = model.state_dict()

    # These two tensors have different shapes in the old
    # and new models, so we transfer them separately below.
    classifier_keys = {
        "classifier.1.weight",
        "classifier.1.bias",
    }

    # Copy every compatible backbone parameter.
    compatible_state = {
        name: tensor
        for name, tensor in old_state.items()
        if (
            name in new_state
            and name not in classifier_keys
            and tensor.shape == new_state[name].shape
        )
    }

    # IMPORTANT FIX:
    # load_state_dict returns ONE result object.
    load_result = model.load_state_dict(
        compatible_state,
        strict=False,
    )

    if set(load_result.missing_keys) != classifier_keys:
        raise RuntimeError(
            "Unexpected missing model parameters: "
            f"{load_result.missing_keys}"
        )

    if load_result.unexpected_keys:
        raise RuntimeError(
            "Unexpected parameters: "
            f"{load_result.unexpected_keys}"
        )

    # Transfer the original 38 classifier rows to their
    # corresponding class indices in the expanded model.
    with torch.no_grad():

        for class_name, old_index in old_class_to_idx.items():

            new_index = class_to_idx[class_name]

            model.classifier[1].weight[new_index].copy_(
                old_state["classifier.1.weight"][old_index]
            )

            model.classifier[1].bias[new_index].copy_(
                old_state["classifier.1.bias"][old_index]
            )

    print(
        "Transferred existing class weights:",
        len(old_class_to_idx),
    )

    print(
        "New output classes:",
        number_of_classes - len(old_class_to_idx),
    )

    # Freeze the early feature extractor.
    for parameter in model.parameters():
        parameter.requires_grad = False

    # Fine-tune later features and the classifier.
    for parameter in model.features[6:].parameters():
        parameter.requires_grad = True

    for parameter in model.classifier.parameters():
        parameter.requires_grad = True

    return model.to(device)


# =========================================
# Save checkpoint
# =========================================

def save_checkpoint(
    path,
    model,
    class_to_idx,
    epoch,
    val_accuracy,
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
            "val_loss": val_loss,
            "source_checkpoint": str(SOURCE_CHECKPOINT),
        },
        path,
    )


# =========================================
# Main
# =========================================

def main():

    print("=" * 65)
    print("EXPANDED PLANT DISEASE MODEL TRAINING")
    print("=" * 65)

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
    # Required files
    # -------------------------------------

    required_files = [
        SOURCE_CHECKPOINT,
        CLASS_MAPPING_FILE,
        TRAIN_CSV,
        VAL_CSV,
        TEST_CSV,
    ]

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

    # -------------------------------------
    # Class mapping
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

    expected_indices = list(range(len(class_to_idx)))

    if sorted(class_to_idx.values()) != expected_indices:
        raise ValueError(
            "Class indices must be contiguous, starting at zero."
        )

    print("\nNumber of classes:", len(class_to_idx))

    # -------------------------------------
    # Load all split manifests
    # -------------------------------------

    print("\nLoading dataset manifests...")

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

    test_dataset = CombinedPlantDataset(
        TEST_CSV,
        class_to_idx,
        transform=None,
    )

    validate_splits(
        train_dataset,
        val_dataset,
        test_dataset,
        class_to_idx,
    )

    print("\nTraining images:", f"{len(train_dataset):,}")
    print("Validation images:", f"{len(val_dataset):,}")
    print("Number of classes:", len(class_to_idx))

    # -------------------------------------
    # Class weights
    # -------------------------------------

    class_counts = Counter(train_dataset.labels)

    counts = torch.tensor(
        [
            class_counts[index]
            for index in range(len(class_to_idx))
        ],
        dtype=torch.float32,
    )

    if torch.any(counts == 0):
        raise ValueError(
            "At least one class has no training images."
        )

    class_weights = counts.rsqrt()
    class_weights /= class_weights.mean()
    class_weights = class_weights.to(device)

    print("Class weights calculated.")

    # -------------------------------------
    # DataLoaders
    # -------------------------------------

    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
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
    # Model
    # -------------------------------------

    model = initialize_expanded_model(
        class_to_idx,
        device,
    )

    # -------------------------------------
    # Loss
    # -------------------------------------

    criterion = nn.CrossEntropyLoss(
        weight=class_weights,
    )

    # -------------------------------------
    # Optimizer
    # -------------------------------------

    optimizer = torch.optim.AdamW(
        [
            {
                "params": model.features[6:].parameters(),
                "lr": BACKBONE_LEARNING_RATE,
            },
            {
                "params": model.classifier.parameters(),
                "lr": CLASSIFIER_LEARNING_RATE,
            },
        ],
        weight_decay=WEIGHT_DECAY,
    )

    scaler = torch.amp.GradScaler(
        "cuda",
        enabled=use_amp,
    )

    best_val_accuracy = -1.0

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

        # Keep the frozen early layers in evaluation mode.
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

        train_loss = running_loss / len(train_loader)

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

        with torch.inference_mode():

            for images, labels in val_loader:

                images = images.to(
                    device,
                    non_blocking=True,
                )

                labels = labels.to(
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
                        labels,
                    )

                val_loss_total += loss.item()

                predictions = outputs.argmax(dim=1)

                val_correct += (
                    predictions == labels
                ).sum().item()

                val_total += labels.size(0)

        val_loss = val_loss_total / len(val_loader)

        val_accuracy = 100 * val_correct / val_total

        # ---------------------------------
        # Metrics
        # ---------------------------------

        print("\nEpoch results:")

        print(f"Train loss:     {train_loss:.4f}")
        print(f"Train accuracy: {train_accuracy:.2f}%")
        print(f"Val loss:       {val_loss:.4f}")
        print(f"Val accuracy:   {val_accuracy:.2f}%")

        # ---------------------------------
        # Save most recent epoch
        # ---------------------------------

        save_checkpoint(
            LATEST_MODEL_PATH,
            model,
            class_to_idx,
            epoch + 1,
            val_accuracy,
            val_loss,
        )

        # ---------------------------------
        # Save best validation model
        # ---------------------------------

        if val_accuracy > best_val_accuracy:

            best_val_accuracy = val_accuracy

            save_checkpoint(
                BEST_MODEL_PATH,
                model,
                class_to_idx,
                epoch + 1,
                val_accuracy,
                val_loss,
            )

            print("\nBest combined model saved:")
            print(BEST_MODEL_PATH)

        print("\nOriginal checkpoint remains untouched.")

    # =====================================
    # Finished
    # =====================================

    print("\n" + "=" * 65)
    print("COMBINED TRAINING COMPLETED")
    print("=" * 65)

    print(
        f"Best validation accuracy: "
        f"{best_val_accuracy:.2f}%"
    )

    print("\nBest checkpoint:")
    print(BEST_MODEL_PATH)

    print("\nLatest checkpoint:")
    print(LATEST_MODEL_PATH)

    print(
        "\nThe test set was not used for training "
        "or checkpoint selection."
    )


if __name__ == "__main__":
    main()
