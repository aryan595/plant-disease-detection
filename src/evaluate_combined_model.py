
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

CHECKPOINT_PATH = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_combined_55class.pth"
)

TEST_CSV = COMBINED_DIR / "combined_test.csv"
CLASS_MAPPING_FILE = (
    COMBINED_DIR / "combined_class_to_idx.json"
)

REPORT_DIR = PROJECT_ROOT / "models"

JSON_REPORT = REPORT_DIR / "combined_test_report.json"
CLASS_REPORT = REPORT_DIR / "combined_test_classification_report.csv"
CONFUSION_CSV = REPORT_DIR / "combined_test_confusion_matrix.csv"

BATCH_SIZE = 8
NUM_WORKERS = 2


# =========================================
# Test dataset
# =========================================

class CombinedTestDataset(Dataset):

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
                        f"Incorrect class index: {class_name}"
                    )

                if not image_path.is_file():
                    raise FileNotFoundError(
                        f"Image not found: {image_path}"
                    )

                self.rows.append({
                    "image_path": image_path,
                    "class_name": class_name,
                    "label": label,
                })

        if not self.rows:
            raise ValueError("The test dataset is empty.")

    def __len__(self):
        return len(self.rows)

    def __getitem__(self, index):

        row = self.rows[index]

        with Image.open(row["image_path"]) as source:
            image = source.convert("RGB")

        if self.transform is not None:
            image = self.transform(image)

        return image, row["label"]


# =========================================
# Main
# =========================================

def main():

    print("=" * 65)
    print("EXPANDED MODEL TEST EVALUATION")
    print("=" * 65)

    # -------------------------------------
    # Check files
    # -------------------------------------

    for path in [
        CHECKPOINT_PATH,
        TEST_CSV,
        CLASS_MAPPING_FILE,
    ]:

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

    class_names = [
        name
        for name, _ in sorted(
            class_to_idx.items(),
            key=lambda item: item[1],
        )
    ]

    num_classes = len(class_names)

    print("Number of classes:", num_classes)

    # -------------------------------------
    # Test data
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

    # -------------------------------------
    # Load best trained model
    # -------------------------------------

    print("\nLoading best combined checkpoint...")

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
        weights_only=False,
    )

    checkpoint_mapping = {
        name: int(index)
        for name, index in checkpoint["class_to_idx"].items()
    }

    if checkpoint_mapping != class_to_idx:
        raise ValueError(
            "Checkpoint class mapping differs from "
            "the combined mapping."
        )

    model = create_model(
        num_classes=num_classes,
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
        "Best validation accuracy:",
        f"{checkpoint['val_accuracy']:.2f}%",
    )

    # -------------------------------------
    # Test inference
    # -------------------------------------

    all_labels = []
    all_predictions = []
    all_top3 = []

    correct = 0
    total = 0

    print("\nRunning test evaluation...")

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

            predictions = outputs.argmax(dim=1)

            top3_predictions = outputs.topk(
                k=3,
                dim=1,
            ).indices

            labels_list = labels.tolist()

            predictions_list = predictions.cpu().tolist()

            top3_list = top3_predictions.cpu().tolist()

            all_labels.extend(labels_list)

            all_predictions.extend(predictions_list)

            all_top3.extend(
                [
                    label in top3
                    for label, top3 in zip(
                        labels_list,
                        top3_list,
                    )
                ]
            )

            correct += (
                predictions.cpu() == labels
            ).sum().item()

            total += labels.size(0)

            if batch_index % 200 == 0:

                print(
                    f"Processed {total:,}/"
                    f"{len(test_dataset):,} images"
                )

    # -------------------------------------
    # Overall metrics
    # -------------------------------------

    accuracy = accuracy_score(
        all_labels,
        all_predictions,
    )

    macro_f1 = f1_score(
        all_labels,
        all_predictions,
        labels=list(range(num_classes)),
        average="macro",
        zero_division=0,
    )

    weighted_f1 = f1_score(
        all_labels,
        all_predictions,
        labels=list(range(num_classes)),
        average="weighted",
        zero_division=0,
    )

    top3_accuracy = sum(all_top3) / len(all_top3)

    report = classification_report(
        all_labels,
        all_predictions,
        labels=list(range(num_classes)),
        target_names=class_names,
        output_dict=True,
        zero_division=0,
    )

    print("\n" + "=" * 65)
    print("FINAL TEST RESULTS")
    print("=" * 65)

    print(f"Test samples:       {len(all_labels):,}")
    print(f"Accuracy:           {accuracy * 100:.2f}%")
    print(f"Macro F1:           {macro_f1 * 100:.2f}%")
    print(f"Weighted F1:        {weighted_f1 * 100:.2f}%")
    print(f"Top-3 accuracy:     {top3_accuracy * 100:.2f}%")

    print("\nPer-class results:")

    for class_name in class_names:

        metrics = report[class_name]

        print(
            f"{class_name:<55} "
            f"F1: {metrics['f1-score'] * 100:6.2f}% "
            f"Support: {int(metrics['support']):5d}"
        )

    # -------------------------------------
    # Save JSON report
    # -------------------------------------

    REPORT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    report_data = {
        "checkpoint": str(CHECKPOINT_PATH),
        "checkpoint_epoch": checkpoint["epoch"],
        "best_validation_accuracy": checkpoint["val_accuracy"],
        "number_of_classes": num_classes,
        "test_samples": len(all_labels),
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "weighted_f1": weighted_f1,
        "top3_accuracy": top3_accuracy,
        "classification_report": report,
    }

    with open(
        JSON_REPORT,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            report_data,
            file,
            indent=2,
        )

    # -------------------------------------
    # Save per-class CSV report
    # -------------------------------------

    with open(
        CLASS_REPORT,
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

        for class_name in class_names:

            metrics = report[class_name]

            writer.writerow({
                "class_name": class_name,
                "precision": metrics["precision"],
                "recall": metrics["recall"],
                "f1_score": metrics["f1-score"],
                "support": int(metrics["support"]),
            })

    # -------------------------------------
    # Save confusion matrix
    # -------------------------------------

    matrix = confusion_matrix(
        all_labels,
        all_predictions,
        labels=list(range(num_classes)),
    )

    with open(
        CONFUSION_CSV,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        writer = csv.writer(file)

        writer.writerow([
            "actual_vs_predicted",
            *class_names,
        ])

        for class_name, row in zip(
            class_names,
            matrix,
        ):

            writer.writerow([
                class_name,
                *row.tolist(),
            ])

    print("\nReports saved:")

    print(JSON_REPORT)
    print(CLASS_REPORT)
    print(CONFUSION_CSV)

    print("\nEvaluation complete.")
    print("The model checkpoint was not modified.")


if __name__ == "__main__":
    main()
