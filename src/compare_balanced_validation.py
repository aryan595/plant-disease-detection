
import csv
import json
from pathlib import Path

import torch
from PIL import Image
from torch.utils.data import Dataset, DataLoader
from sklearn.metrics import (
    accuracy_score,
    f1_score,
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

BALANCED_CHECKPOINT = (
    MODELS_DIR / "efficientnet_b0_combined_balanced_best.pth"
)

CLASS_MAPPING_FILE = (
    COMBINED_DIR / "combined_class_to_idx.json"
)

VAL_CSV = COMBINED_DIR / "combined_val.csv"

# Reports from the original, unbalanced model.
BASELINE_REPORT = (
    MODELS_DIR / "combined_val_classification_report.csv"
)

# Separate output files so baseline reports aren't overwritten.
BALANCED_REPORT = (
    MODELS_DIR / "combined_balanced_val_classification_report.csv"
)

BALANCED_CONFUSION = (
    MODELS_DIR / "combined_balanced_val_confusion_matrix.csv"
)

BALANCED_SUMMARY = (
    MODELS_DIR / "combined_balanced_val_summary.json"
)

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
                        f"Incorrect index for {class_name}"
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
# Read baseline F1 report
# =========================================

def load_baseline_f1():

    if not BASELINE_REPORT.is_file():
        print(
            "\nBaseline validation report not found. "
            "The comparison will still evaluate the balanced model."
        )
        return {}

    baseline = {}

    with open(
        BASELINE_REPORT,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            name = row.get("class_name")
            score = row.get("f1_score")

            if name and score is not None:
                baseline[name] = float(score)

    return baseline


# =========================================
# Main
# =========================================

def main():

    print("=" * 70)
    print("BALANCED MODEL — VALIDATION COMPARISON")
    print("=" * 70)

    # -------------------------------------
    # Verify files
    # -------------------------------------

    for path in [
        BALANCED_CHECKPOINT,
        CLASS_MAPPING_FILE,
        VAL_CSV,
    ]:

        if not path.is_file():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

    # -------------------------------------
    # Device and class mapping
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
        name
        for name, _ in sorted(
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
    # Load balanced checkpoint
    # -------------------------------------

    print("\nLoading balanced checkpoint...")

    checkpoint = torch.load(
        BALANCED_CHECKPOINT,
        map_location="cpu",
        weights_only=False,
    )

    saved_mapping = {
        name: int(index)
        for name, index in checkpoint["class_to_idx"].items()
    }

    if saved_mapping != class_to_idx:
        raise ValueError(
            "Balanced checkpoint and class mapping differ."
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

    print("Checkpoint epoch:", checkpoint["epoch"])
    print(
        "Recorded validation macro F1:",
        f"{checkpoint['val_macro_f1'] * 100:.2f}%",
    )

    # -------------------------------------
    # Evaluate validation set
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

    macro_f1 = f1_score(
        actual,
        predicted,
        labels=list(range(len(class_names))),
        average="macro",
        zero_division=0,
    )

    weighted_f1 = f1_score(
        actual,
        predicted,
        labels=list(range(len(class_names))),
        average="weighted",
        zero_division=0,
    )

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

    print("\n" + "=" * 70)
    print("BALANCED VALIDATION RESULTS")
    print("=" * 70)

    print(f"Accuracy:   {accuracy * 100:.2f}%")
    print(f"Macro F1:   {macro_f1 * 100:.2f}%")
    print(f"Weighted F1: {weighted_f1 * 100:.2f}%")

    # -------------------------------------
    # Compare targeted classes
    # -------------------------------------

    baseline_f1 = load_baseline_f1()

    important_classes = [
        "Sugarcane___Mosaic",
        "Sugarcane___healthy",
        "Sugarcane___Red_rot",
        "Sugarcane___Rust",
        "Sugarcane___Yellow_disease",
        "Cotton___Bacterial_blight",
        "Soybean___Bacterial_blight",
        "Grape___Bacterial_leaf_spot",
        "Grape___Downy_mildew",
    ]

    print("\n" + "=" * 70)
    print("TARGETED CLASS COMPARISON")
    print("=" * 70)

    for name in important_classes:

        if name not in report:
            continue

        balanced_f1 = report[name]["f1-score"]

        print(f"\n{name}")

        if name in baseline_f1:

            old_f1 = baseline_f1[name]
            delta = (balanced_f1 - old_f1) * 100

            print(f"  Original validation F1: {old_f1 * 100:.2f}%")
            print(f"  Balanced validation F1: {balanced_f1 * 100:.2f}%")
            print(f"  Change: {delta:+.2f} percentage points")

        else:

            print(
                f"  Balanced validation F1: "
                f"{balanced_f1 * 100:.2f}%"
            )

    # -------------------------------------
    # Lowest-F1 classes
    # -------------------------------------

    weak_classes = sorted(
        (
            {
                "class_name": name,
                "precision": report[name]["precision"],
                "recall": report[name]["recall"],
                "f1_score": report[name]["f1-score"],
                "support": int(report[name]["support"]),
            }
            for name in class_names
        ),
        key=lambda item: (
            item["f1_score"],
            item["support"],
        ),
    )[:10]

    print("\n" + "=" * 70)
    print("10 LOWEST-F1 BALANCED VALIDATION CLASSES")
    print("=" * 70)

    for item in weak_classes:

        print(
            f"{item['class_name']:<55} "
            f"F1: {item['f1_score'] * 100:6.2f}% "
            f"Recall: {item['recall'] * 100:6.2f}% "
            f"Support: {item['support']:4d}"
        )

    # -------------------------------------
    # Save per-class report
    # -------------------------------------

    per_class_rows = [
        {
            "class_name": name,
            "precision": report[name]["precision"],
            "recall": report[name]["recall"],
            "f1_score": report[name]["f1-score"],
            "support": int(report[name]["support"]),
        }
        for name in class_names
    ]

    with open(
        BALANCED_REPORT,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=[
                "class_name",
                "precision",
                "recall",
                "f1_score",
                "support",
            ],
        )

        writer.writeheader()
        writer.writerows(per_class_rows)

    # -------------------------------------
    # Save confusion matrix
    # -------------------------------------

    with open(
        BALANCED_CONFUSION,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "actual_vs_predicted",
            *class_names,
        ])

        for name, row in zip(class_names, matrix):

            writer.writerow([
                name,
                *row.tolist(),
            ])

    # -------------------------------------
    # Save summary
    # -------------------------------------

    summary = {
        "checkpoint": str(BALANCED_CHECKPOINT),
        "epoch": checkpoint["epoch"],
        "validation_images": len(dataset),
        "number_of_classes": len(class_names),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "targeted_class_comparison": {
            name: {
                "original_f1": baseline_f1.get(name),
                "balanced_f1": report[name]["f1-score"],
            }
            for name in important_classes
            if name in report
        },
    }

    with open(
        BALANCED_SUMMARY,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=2,
        )

    print("\nReports saved:")
    print(BALANCED_REPORT)
    print(BALANCED_CONFUSION)
    print(BALANCED_SUMMARY)

    print("\nValidation comparison complete.")
    print("No test images were evaluated.")
    print("No model checkpoints were modified.")


if __name__ == "__main__":
    main()
