import json
import random
from pathlib import Path
from collections import defaultdict

# -----------------------------
# Paths
# -----------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = PROJECT_ROOT / "data" / "splits" / "color_train.txt"
LEAF_MAP_FILE = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
    / "leaf_grouping"
    / "leaf-map.json"
)

VAL_FILE = PROJECT_ROOT / "data" / "splits" / "color_val.txt"


# -----------------------------
# Settings
# -----------------------------
VALIDATION_RATIO = 0.10
RANDOM_SEED = 42


# -----------------------------
# Load training paths
# -----------------------------
with open(TRAIN_FILE, "r", encoding="utf-8") as f:
    train_paths = [line.strip() for line in f if line.strip()]


# -----------------------------
# Load leaf mapping
# -----------------------------
with open(LEAF_MAP_FILE, "r", encoding="utf-8") as f:
    leaf_map = json.load(f)


# -----------------------------
# Convert an image filename
# into the lookup identifier
# -----------------------------
def get_image_identifier(file_name: str) -> str:
    identifier = file_name.replace("_final_masked", "")

    if "___" in identifier:
        identifier = identifier.split("___")[-1]

    identifier = identifier.split("copy")[0]

    for extension in [".jpg", ".JPG", ".png", ".PNG"]:
        identifier = identifier.replace(extension, "")

    return identifier.strip().lower()


# -----------------------------
# Group images by leaf
# -----------------------------
leaf_groups = defaultdict(list)

for image_path in train_paths:

    parts = image_path.split("/")

    # Expected:
    # raw/color/class_name/file_name
    if len(parts) < 4:
        continue

    class_name = parts[2]
    file_name = parts[3]

    image_identifier = get_image_identifier(file_name)

    # Find leaf information
    leaf_id = None

    if image_identifier in leaf_map:
        suggestions = leaf_map[image_identifier]

        if len(suggestions) == 1:
            leaf_id = suggestions[0]
        else:
            for suggestion in suggestions:
                if class_name in suggestion:
                    leaf_id = suggestion
                    break

    # Fallback if mapping isn't found
    if leaf_id is None:
        leaf_id = f"fallback_{image_identifier}"

    # Include class in the grouping key.
    # This makes the grouping extra safe.
    group_key = (class_name, leaf_id)

    leaf_groups[group_key].append(image_path)


# -----------------------------
# Select validation groups
# -----------------------------
random.seed(RANDOM_SEED)

groups_by_class = defaultdict(list)

for (class_name, leaf_id), images in leaf_groups.items():
    groups_by_class[class_name].append(images)


validation_paths = []
training_paths = []

for class_name, groups in groups_by_class.items():

    random.shuffle(groups)

    total_images = sum(len(group) for group in groups)

    target_validation = max(
        1,
        round(total_images * VALIDATION_RATIO)
    )

    current_validation = 0

    for group in groups:

        if current_validation < target_validation:
            validation_paths.extend(group)
            current_validation += len(group)
        else:
            training_paths.extend(group)


# -----------------------------
# Sort for reproducibility
# -----------------------------
validation_paths.sort()
training_paths.sort()


# -----------------------------
# Write validation split
# -----------------------------
with open(VAL_FILE, "w", encoding="utf-8") as f:
    for path in validation_paths:
        f.write(path + "\n")


# -----------------------------
# Print results
# -----------------------------
print("Validation split created!")
print()
print(f"Original training images : {len(train_paths)}")
print(f"New training images      : {len(training_paths)}")
print(f"Validation images        : {len(validation_paths)}")
print(f"Total                    : {len(training_paths) + len(validation_paths)}")
print()
print(f"Saved to: {VAL_FILE}")