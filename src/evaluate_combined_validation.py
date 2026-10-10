
import csv
import json
from pathlib import Path
from collections import Counter

import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)

from image_transforms import val_test_transforms
from plant_model import create_model


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

COMBINED_DIR = PROJECT_ROOT / "data" / "splits" / "combined"
MODELS_DIR = PROJECT_ROOT / "models"

CHECKPOINT_PATH = (
    MODELS_DIR / "efficientnet_b0_combined_55class.pth"
)

VAL_CSV = COMBINED_DIR / "combined_val.csv"

CLASS_MAPPING_FILE = (
    COMBINED_DIR / "combined_class_to_idx.json"
)

REPORT_FILE = MODELS_DIR / "combined_val_classification_report.csv"

CONFUSION_FILE = MODELS_DIR / "combined_val_confusion_matrix.csv"

BATCH_SIZE = 8
NUM_WORKERS = 2


# =========================================
# Validation dataset
# =========================================

class ValidationDataset(Dataset):

    def __init__(self, csv_path, class_to_idx, transform):

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
            raise ValueError("Validation dataset is empty.")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):

        row = self.rows[index]

        with Image.open(row["path"]) as source:
            image = source.convert("RGB")

        image = self.transform(image)

        return image, row["label"]


# =========================================
# Main
# =========================================

def main():

    print("=" * 65)
    print("COMBINED MODEL VALIDATION ANALYSIS")
    print("=" * 65)

    for path in [
        CHECKPOINT_PATH,
        VAL_CSV,
        CLASS_MAPPING_FILE,
    ]:
        if not path.is_file():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

    # -------------------------------------
    # Device and classes
    # -------------------------------------

    device = torch.device(
        "cuda" if torch.cuda.is_available() else "cpu"
    )

    use_amp = device.type == "cuda"

    print("\nDevice:", device)

    if use_amp:
        print("GPU:", torch.cuda.get_device_name(0))

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

    class_names = [
        name for name, _ in sorted(
            class_to_idx.items(),
            key=lambda item: item[1],
        )
    ]

    # -------------------------------------
    # Validation loader
    # -------------------------------------

    dataset = ValidationDataset(
        VAL_CSV,
        class_to_idx,
        val_test_transforms,
    )

    loader = DataLoader(
        dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=use_amp,
        persistent_workers=NUM_WORKERS > 0,
    )

    print("Validation images:", f"{len(dataset):,}")
    print("Classes:", len(class_names))

    # -------------------------------------
    # Load checkpoint
    # -------------------------------------

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
        weights_only=False,
    )

    saved_mapping = {
        name: int(index)
        for name, index in checkpoint["class_to_idx"].items()
    }

    if saved_mapping != class_to_idx:
        raise ValueError(
            "Checkpoint and class mapping do not match."
        )

    model = create_model(
        num_classes=len(class_names),
        freeze_backbone=False,
    )

    model.load_state_dict(
        checkpoint["model_state_dict"],
        strict=True,
    )

    model = model.to(device)
    model.eval()

    # -------------------------------------
    # Run validation inference
    # -------------------------------------

    actual = []
    predicted = []

    print("\nRunning validation inference...")

    with torch.inference_mode():

        for batch_index, (images, labels) in enumerate(
            loader,
            start=1,
        ):

            images = images.to(
                device,
                non_blocking=True,
            )

            with torch.autocast(
                device_type="cuda",
                dtype=torch.float16,
                enabled=use_amp,
            ):
                outputs = model(images)

            predictions = outputs.argmax(dim=1)

            actual.extend(labels.tolist())
            predicted.extend(predictions.cpu().tolist())

            if batch_index % 100 == 0:
                print(
                    f"Processed {len(actual):,}/"
                    f"{len(dataset):,} images"
                )

    # -------------------------------------
    # Compute metrics
    # -------------------------------------

    accuracy = accuracy_score(actual, predicted)

    report = classification_report(
        actual,
        predicted,
        labels=list(range(len(class_names))),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    matrix = confusion_matrix(
        actual,
        predicted,
        labels=list(range(len(class_names))),
    )

    print("\n" + "=" * 65)
    print("VALIDATION RESULTS")
    print("=" * 65)

    print(f"Validation accuracy: {accuracy * 100:.2f}%")
    print(f"Macro F1: {report['macro avg']['f1-score'] * 100:.2f}%")
    print(
        f"Weighted F1: "
        f"{report['weighted avg']['f1-score'] * 100:.2f}%"
    )

    # -------------------------------------
    # Lowest F1 classes
    # -------------------------------------

    per_class = [
        {
            "class_name": name,
            "precision": report[name]["precision"],
            "recall": report[name]["recall"],
            "f1_score": report[name]["f1-score"],
            "support": int(report[name]["support"]),
        }
        for name in class_names
    ]

    weakest = sorted(
        per_class,
        key=lambda item: (item["f1_score"], item["support"]),
    )[:10]

    print("\n10 LOWEST-F1 VALIDATION CLASSES")

    for item in weakest:

        print(
            f"{item['class_name']:<55} "
            f"F1: {item['f1_score'] * 100:6.2f}% "
            f"Recall: {item['recall'] * 100:6.2f}% "
            f"Support: {item['support']:4d}"
        )

    # -------------------------------------
    # Most frequent confusions
    # -------------------------------------

    confusions = []

    for actual_index, actual_name in enumerate(class_names):

        for predicted_index, predicted_name in enumerate(class_names):

            if actual_index == predicted_index:
                continue

            count = int(matrix[actual_index, predicted_index])

            if count:
                confusions.append((
                    count,
                    actual_name,
                    predicted_name,
                ))

    confusions.sort(reverse=True)

    print("\n15 MOST FREQUENT VALIDATION CONFUSIONS")

    for count, actual_name, predicted_name in confusions[:15]:

        print(
            f"Actual: {actual_name}\n"
            f"  Predicted: {predicted_name}"
            f" | Incorrect: {count}"
        )

    # -------------------------------------
    # Save per-class report
    # -------------------------------------

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        REPORT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        fields = [
            "class_name",
            "precision",
            "recall",
            "f1_score",
            "support",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(per_class)

    # -------------------------------------
    # Save confusion matrix
    # -------------------------------------

    with open(
        CONFUSION_FILE,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "actual_vs_predicted",
            *class_names,
        ])

        for class_name, row in zip(class_names, matrix):

            writer.writerow([
                class_name,
                *row.tolist(),
            ])

    print("\nReports saved:")
    print(REPORT_FILE)
    print(CONFUSION_FILE)

    print("\nValidation analysis complete.")
    print("The model checkpoint was not modified.")
    print("The test set was not loaded or evaluated.")


if __name__ == "__main__":
    main()
