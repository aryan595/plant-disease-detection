
import csv
from pathlib import Path


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
MODELS_DIR = PROJECT_ROOT / "models"

CLASS_REPORT = (
    MODELS_DIR / "combined_test_classification_report.csv"
)

CONFUSION_FILE = (
    MODELS_DIR / "combined_test_confusion_matrix.csv"
)

NUM_WEAK_CLASSES = 10
NUM_TOP_CONFUSIONS = 15


# =========================================
# Read classification report
# =========================================

def load_classification_report():

    if not CLASS_REPORT.is_file():
        raise FileNotFoundError(
            f"Classification report not found: {CLASS_REPORT}"
        )

    rows = []

    with open(
        CLASS_REPORT,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            class_name = row["class_name"]

            # Ignore aggregate rows if present.
            if class_name in {
                "accuracy",
                "macro avg",
                "weighted avg",
            }:
                continue

            rows.append({
                "class_name": class_name,
                "precision": float(row["precision"]),
                "recall": float(row["recall"]),
                "f1": float(row["f1_score"]),
                "support": int(float(row["support"])),
            })

    return rows


# =========================================
# Read confusion matrix
# =========================================

def load_confusion_matrix():

    if not CONFUSION_FILE.is_file():
        raise FileNotFoundError(
            f"Confusion matrix not found: {CONFUSION_FILE}"
        )

    with open(
        CONFUSION_FILE,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.reader(file)

        header = next(reader)

        if not header or header[0] != "actual_vs_predicted":
            raise ValueError(
                "Unexpected confusion matrix format."
            )

        class_names = header[1:]

        matrix = {}

        for row in reader:

            if not row:
                continue

            actual_class = row[0]

            values = [
                int(value)
                for value in row[1:]
            ]

            if len(values) != len(class_names):
                raise ValueError(
                    f"Incorrect matrix row length: {actual_class}"
                )

            matrix[actual_class] = dict(
                zip(class_names, values)
            )

    if set(matrix) != set(class_names):
        raise ValueError(
            "Confusion matrix row and column classes do not match."
        )

    return class_names, matrix


# =========================================
# Print lowest-performing classes
# =========================================

def show_weak_classes(report, matrix):

    weakest = sorted(
        report,
        key=lambda row: (
            row["f1"],
            row["support"],
        ),
    )[:NUM_WEAK_CLASSES]

    print("\n" + "=" * 80)
    print("10 CLASSES WITH THE LOWEST F1 SCORES")
    print("=" * 80)

    for item in weakest:

        name = item["class_name"]

        total = sum(
            matrix[name].values()
        )

        correct = matrix[name].get(name, 0)

        errors = total - correct

        print(f"\nClass: {name}")

        print(
            f"  F1: {item['f1'] * 100:.2f}%"
            f" | Precision: {item['precision'] * 100:.2f}%"
            f" | Recall: {item['recall'] * 100:.2f}%"
        )

        print(
            f"  Test images: {item['support']}"
            f" | Correct: {correct}"
            f" | Incorrect: {errors}"
        )

        mistakes = sorted(
            (
                (predicted, count)
                for predicted, count
                in matrix[name].items()
                if predicted != name and count > 0
            ),
            key=lambda pair: pair[1],
            reverse=True,
        )

        if not mistakes:

            print("  No incorrect predictions in this split.")

        else:

            print("  Most common incorrect predictions:")

            for predicted, count in mistakes[:3]:

                print(
                    f"    -> {predicted}: {count}"
                )


# =========================================
# Print most common confusions
# =========================================

def show_top_confusions(class_names, matrix):

    confusions = []

    for actual_class in class_names:

        for predicted_class in class_names:

            if actual_class == predicted_class:
                continue

            count = matrix[actual_class][predicted_class]

            if count > 0:

                confusions.append({
                    "actual": actual_class,
                    "predicted": predicted_class,
                    "count": count,
                })

    confusions.sort(
        key=lambda item: item["count"],
        reverse=True,
    )

    print("\n" + "=" * 80)
    print("MOST FREQUENT MISCLASSIFICATIONS")
    print("=" * 80)

    if not confusions:

        print("No misclassifications found.")

        return

    for rank, item in enumerate(
        confusions[:NUM_TOP_CONFUSIONS],
        start=1,
    ):

        print(
            f"{rank:2d}. Actual: {item['actual']}"
        )

        print(
            f"    Predicted: {item['predicted']}"
            f" | Incorrect images: {item['count']}"
        )


# =========================================
# New-crop class summary
# =========================================

def show_new_crop_summary(report):

    new_crops = (
        "Cotton___",
        "Grape___",
        "Sugarcane___",
        "Soybean___",
    )

    crop_groups = {}

    for item in report:

        name = item["class_name"]

        for prefix in new_crops:

            if name.startswith(prefix):

                crop_groups.setdefault(
                    prefix.removesuffix("___"),
                    [],
                ).append(item)

                break

    print("\n" + "=" * 80)
    print("AVERAGE F1 FOR EACH ADDED CROP")
    print("=" * 80)

    for crop, items in sorted(crop_groups.items()):

        macro_f1 = (
            sum(item["f1"] for item in items)
            / len(items)
        )

        total_support = sum(
            item["support"]
            for item in items
        )

        print(
            f"{crop:12s} | "
            f"Classes: {len(items):2d} | "
            f"Macro F1: {macro_f1 * 100:.2f}% | "
            f"Test images: {total_support}"
        )


# =========================================
# Main
# =========================================

def main():

    print("=" * 80)
    print("PLANT DISEASE MODEL ERROR ANALYSIS")
    print("=" * 80)

    report = load_classification_report()

    class_names, matrix = load_confusion_matrix()

    if set(class_names) != {
        item["class_name"] for item in report
    }:
        raise ValueError(
            "Classification report and confusion matrix "
            "contain different classes."
        )

    print("Classes analyzed:", len(class_names))

    show_weak_classes(report, matrix)

    show_top_confusions(class_names, matrix)

    show_new_crop_summary(report)

    print("\n" + "=" * 80)
    print("ANALYSIS COMPLETED")
    print("No files were modified.")
    print("=" * 80)


if __name__ == "__main__":
    main()
