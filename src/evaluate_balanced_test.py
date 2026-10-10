
import csv
import json
from pathlib import Path

import torch
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
)
from torch.utils.data import DataLoader

from image_transforms import val_test_transforms
from plant_model import create_model

from evaluate_combined_model import (
    CombinedTestDataset,
    TEST_CSV,
    CLASS_MAPPING_FILE,
    REPORT_DIR,
)


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

BALANCED_CHECKPOINT = (
    MODELS_DIR / "efficientnet_b0_combined_balanced_best.pth"
)

BASELINE_JSON = MODELS_DIR / "combined_test_report.json"
BASELINE_CLASS_REPORT = (
    MODELS_DIR / "combined_test_classification_report.csv"
)

OUTPUT_JSON = MODELS_DIR / "combined_balanced_test_report.json"
OUTPUT_CSV = (
    MODELS_DIR / "combined_balanced_test_classification_report.csv"
)
OUTPUT_CONFUSION = (
    MODELS_DIR / "combined_balanced_test_confusion_matrix.csv"
)

BATCH_SIZE = 8
NUM_WORKERS = 2


# =========================================
# Main
# =========================================

def main():

    print("=" * 70)
    print("BALANCED MODEL — TEST COMPARISON")
    print("=" * 70)

    # -------------------------------------
    # Verify input files
    # -------------------------------------

    required_files = [
        BALANCED_CHECKPOINT,
        TEST_CSV,
        CLASS_MAPPING_FILE,
        BASELINE_JSON,
        BASELINE_CLASS_REPORT,
    ]

    for path in required_files:
        if not path.is_file():
            raise FileNotFoundError(
                f"Required file not found: {path}"
            )

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
    # Load class mapping
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

    class_names = [
        name
        for name, _ in sorted(
            class_to_idx.items(),
            key=lambda item: item[1],
        )
    ]

    # -------------------------------------
    # Load test data
    # -------------------------------------

    test_dataset = CombinedTestDataset(
        TEST_CSV,
        class_to_idx,
        transform=val_test_transforms,
    )

    test_loader = DataLoader(
        test_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=NUM_WORKERS,
        pin_memory=use_amp,
        persistent_workers=NUM_WORKERS > 0,
    )

    print("Test images:", f"{len(test_dataset):,}")
    print("Classes:", len(class_names))

    # -------------------------------------
    # Load balanced checkpoint
    # -------------------------------------

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

    print("Balanced checkpoint epoch:", checkpoint["epoch"])

    # -------------------------------------
    # Evaluate
    # -------------------------------------

    actual = []
    predicted = []
    top3_correct = 0

    print("\nRunning inference...")

    with torch.inference_mode():

        for batch_index, (images, labels) in enumerate(
            test_loader,
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

            probabilities = torch.softmax(
                outputs.float(),
                dim=1,
            )

            predictions = probabilities.argmax(dim=1)

            top3_indices = probabilities.topk(
                k=3,
                dim=1,
            ).indices

            actual.extend(labels.tolist())
            predicted.extend(predictions.cpu().tolist())

            top3_correct += (
                top3_indices.cpu()
                == labels.unsqueeze(1)
            ).any(dim=1).sum().item()

            if batch_index % 200 == 0:
                print(
                    f"Processed "
                    f"{len(actual):,}/{len(test_dataset):,}"
                )

    # -------------------------------------
    # Metrics
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

    top3_accuracy = top3_correct / len(actual)

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
    print("BALANCED MODEL TEST RESULTS")
    print("=" * 70)

    print(f"Accuracy:       {accuracy * 100:.2f}%")
    print(f"Macro F1:       {macro_f1 * 100:.2f}%")
    print(f"Weighted F1:    {weighted_f1 * 100:.2f}%")
    print(f"Top-3 accuracy: {top3_accuracy * 100:.2f}%")

    # -------------------------------------
    # Compare with previous checkpoint
    # -------------------------------------

    with open(
        BASELINE_JSON,
        "r",
        encoding="utf-8",
    ) as file:
        baseline = json.load(file)

    print("\n" + "=" * 70)
    print("PREVIOUS MODEL VS BALANCED MODEL")
    print("=" * 70)

    metric_pairs = [
        ("accuracy", "Accuracy"),
        ("macro_f1", "Macro F1"),
        ("weighted_f1", "Weighted F1"),
        ("top3_accuracy", "Top-3 accuracy"),
    ]

    for key, label in metric_pairs:

        old_value = baseline[key]
        new_value = {
            "accuracy": accuracy,
            "macro_f1": macro_f1,
            "weighted_f1": weighted_f1,
            "top3_accuracy": top3_accuracy,
        }[key]

        delta_pp = (new_value - old_value) * 100

        print(
            f"{label:18s} "
            f"Previous: {old_value * 100:6.2f}% | "
            f"Balanced: {new_value * 100:6.2f}% | "
            f"Change: {delta_pp:+.2f} pp"
        )

    # -------------------------------------
    # Compare key crop classes
    # -------------------------------------

    print("\nTARGETED CLASS COMPARISON")

    with open(
        BASELINE_CLASS_REPORT,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        baseline_f1 = {
            row["class_name"]: float(row["f1_score"])
            for row in reader
        }

    target_classes = [
        "Sugarcane___Mosaic",
        "Sugarcane___healthy",
        "Sugarcane___Red_rot",
        "Sugarcane___Rust",
        "Sugarcane___Yellow_disease",
        "Cotton___Bacterial_blight",
        "Soybean___Bacterial_blight",
        "Grape___Bacterial_leaf_spot",
    ]

    for name in target_classes:

        old_f1 = baseline_f1.get(name)
        new_f1 = report[name]["f1-score"]

        if old_f1 is None:
            continue

        change = (new_f1 - old_f1) * 100

        print(
            f"{name}: "
            f"Previous {old_f1 * 100:.2f}% | "
            f"Balanced {new_f1 * 100:.2f}% | "
            f"Change {change:+.2f} pp"
        )

    # -------------------------------------
    # Save separate report
    # -------------------------------------

    MODELS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with open(
        OUTPUT_JSON,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            {
                "checkpoint": str(BALANCED_CHECKPOINT),
                "epoch": checkpoint["epoch"],
                "test_samples": len(actual),
                "accuracy": accuracy,
                "macro_f1": macro_f1,
                "weighted_f1": weighted_f1,
                "top3_accuracy": top3_accuracy,
                "classification_report": report,
            },
            file,
            indent=2,
        )

    with open(
        OUTPUT_CSV,
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

        for name in class_names:
            metrics = report[name]

            writer.writerow({
                "class_name": name,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1-score"],
                "support": int(metrics["support"]),
            })

    with open(
        OUTPUT_CONFUSION,
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
            writer.writerow([name, *row.tolist()])

    print("\nSeparate reports saved:")
    print(OUTPUT_JSON)
    print(OUTPUT_CSV)
    print(OUTPUT_CONFUSION)

    print("\nComparison complete.")
    print("Neither checkpoint was modified.")


if __name__ == "__main__":
    main()
