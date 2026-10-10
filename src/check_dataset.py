from pathlib import Path
from collections import Counter

# -----------------------------
# Project paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

SPLITS_DIR = PROJECT_ROOT / "data" / "splits"

TRAIN_FILE = SPLITS_DIR / "color_train_final.txt"
VAL_FILE = SPLITS_DIR / "color_val.txt"
TEST_FILE = SPLITS_DIR / "color_test.txt"


# -----------------------------
# Read split file
# -----------------------------
def read_split(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


# -----------------------------
# Extract class name
# -----------------------------
def get_class_name(image_path):
    """
    Example:

    raw/color/Tomato___Early_blight/image.JPG

    returns:

    Tomato___Early_blight
    """
    parts = image_path.replace("\\", "/").split("/")

    if len(parts) < 4:
        raise ValueError(f"Unexpected path format: {image_path}")

    return parts[2]


# -----------------------------
# Analyze a split
# -----------------------------
def analyze_split(name, file_path):
    paths = read_split(file_path)

    class_counts = Counter(
        get_class_name(path)
        for path in paths
    )

    print(f"\n{name}")
    print("-" * 50)
    print(f"Total images : {len(paths)}")
    print(f"Classes      : {len(class_counts)}")

    return paths, class_counts


# -----------------------------
# Analyze all splits
# -----------------------------
train_paths, train_counts = analyze_split(
    "TRAIN",
    TRAIN_FILE
)

val_paths, val_counts = analyze_split(
    "VALIDATION",
    VAL_FILE
)

test_paths, test_counts = analyze_split(
    "TEST",
    TEST_FILE
)


# -----------------------------
# Compare classes
# -----------------------------
all_classes = set(train_counts) | set(val_counts) | set(test_counts)

missing_from_train = all_classes - set(train_counts)
missing_from_val = all_classes - set(val_counts)
missing_from_test = all_classes - set(test_counts)


print("\n" + "=" * 50)
print("CLASS CHECK")
print("=" * 50)

print(f"Total unique classes: {len(all_classes)}")
print(f"Missing from train  : {missing_from_train}")
print(f"Missing from val    : {missing_from_val}")
print(f"Missing from test   : {missing_from_test}")


# -----------------------------
# Show class counts
# -----------------------------
print("\n" + "=" * 80)
print(f"{'CLASS':55} {'TRAIN':>8} {'VAL':>8} {'TEST':>8}")
print("=" * 80)

for class_name in sorted(all_classes):
    print(
        f"{class_name:55} "
        f"{train_counts.get(class_name, 0):8} "
        f"{val_counts.get(class_name, 0):8} "
        f"{test_counts.get(class_name, 0):8}"
    )