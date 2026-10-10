import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

import torch


# =========================================
# Project paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_ROOT = PROJECT_ROOT / "PlantVillage-Dataset"
SPLITS_DIR = PROJECT_ROOT / "data" / "splits"
EXTERNAL_MANIFEST = (
    PROJECT_ROOT / "data" / "external_manifest.csv"
)

CHECKPOINT_PATH = (
    PROJECT_ROOT / "models" / "efficientnet_b0_finetuned.pth"
)

OUTPUT_DIR = SPLITS_DIR / "combined"

SEED = 42

IMAGE_EXTENSIONS = {
    ".jpg", ".jpeg", ".png", ".bmp",
    ".webp", ".tif", ".tiff",
}


# =========================================
# Split configuration
# =========================================

ORIGINAL_SPLITS = {
    "train": SPLITS_DIR / "color_train_final.txt",
    "val": SPLITS_DIR / "color_val.txt",
    "test": SPLITS_DIR / "color_test.txt",
}


# =========================================
# Load existing checkpoint classes
# =========================================

def load_existing_classes():

    if not CHECKPOINT_PATH.is_file():
        raise FileNotFoundError(
            f"Checkpoint not found: {CHECKPOINT_PATH}"
        )

    checkpoint = torch.load(
        CHECKPOINT_PATH,
        map_location="cpu",
        weights_only=False,
    )

    class_to_idx = checkpoint.get("class_to_idx")

    if not isinstance(class_to_idx, dict):
        raise ValueError(
            "The checkpoint has no valid class_to_idx mapping."
        )

    class_to_idx = {
        str(name): int(index)
        for name, index in class_to_idx.items()
    }

    indices = sorted(class_to_idx.values())

    if indices != list(range(len(indices))):
        raise ValueError(
            "Existing class indices are not contiguous."
        )

    print(
        f"Loaded {len(class_to_idx)} existing classes "
        "from the checkpoint."
    )

    return class_to_idx


# =========================================
# Read original PlantVillage splits
# =========================================

def read_original_split(split_name, split_file):

    if not split_file.is_file():
        raise FileNotFoundError(
            f"Split file not found: {split_file}"
        )

    rows = []

    with open(
        split_file,
        "r",
        encoding="utf-8",
    ) as file:

        for line_number, line in enumerate(file, start=1):

            relative_path = line.strip()

            if not relative_path:
                continue

            # Handle Windows and Unix path separators.
            parts = relative_path.replace("\\", "/").split("/")

            if (
                len(parts) < 4
                or parts[0] != "raw"
                or parts[1] != "color"
            ):
                raise ValueError(
                    f"Unexpected path in {split_file}, "
                    f"line {line_number}: {relative_path}"
                )

            class_name = parts[2]

            image_path = (
                DATASET_ROOT / Path(*parts)
            ).resolve()

            if not image_path.is_file():
                raise FileNotFoundError(
                    f"Image listed in split file is missing: "
                    f"{image_path}"
                )

            if image_path.suffix.lower() not in IMAGE_EXTENSIONS:
                raise ValueError(
                    f"Unsupported image extension: {image_path}"
                )

            rows.append({
                "split": split_name,
                "dataset": "plantvillage",
                "source_class": class_name,
                "class_name": class_name,
                "image_path": str(image_path),
                "extension": image_path.suffix.lower(),
            })

    print(
        f"PlantVillage {split_name}: "
        f"{len(rows):,} images"
    )

    return rows


# =========================================
# Read external manifest
# =========================================

def read_external_manifest():

    if not EXTERNAL_MANIFEST.is_file():
        raise FileNotFoundError(
            f"External manifest not found: "
            f"{EXTERNAL_MANIFEST}"
        )

    rows = []

    with open(
        EXTERNAL_MANIFEST,
        "r",
        newline="",
        encoding="utf-8-sig",
    ) as file:

        reader = csv.DictReader(file)

        required_columns = {
            "dataset",
            "source_class",
            "canonical_class",
            "image_path",
            "extension",
        }

        missing_columns = (
            required_columns - set(reader.fieldnames or [])
        )

        if missing_columns:
            raise ValueError(
                "External manifest is missing columns: "
                + ", ".join(sorted(missing_columns))
            )

        for row in reader:

            image_path = Path(row["image_path"]).resolve()

            class_name = row["canonical_class"].strip()

            if not class_name:
                raise ValueError(
                    "An external image has an empty class label."
                )

            if not image_path.is_file():
                raise FileNotFoundError(
                    f"External image is missing: {image_path}"
                )

            rows.append({
                "dataset": row["dataset"].strip(),
                "source_class": row["source_class"].strip(),
                "class_name": class_name,
                "image_path": str(image_path),
                "extension": image_path.suffix.lower(),
            })

    print(
        f"External datasets: {len(rows):,} images"
    )

    return rows


# =========================================
# Split external data by class
# =========================================

def split_external_by_class(external_rows):

    grouped_rows = defaultdict(list)

    for row in external_rows:
        grouped_rows[row["class_name"]].append(row)

    split_rows = {
        "train": [],
        "val": [],
        "test": [],
    }

    for class_name in sorted(grouped_rows):

        images = sorted(
            grouped_rows[class_name],
            key=lambda row: row["image_path"].lower(),
        )

        # A deterministic shuffle for reproducibility.
        rng = random.Random(
            f"{SEED}:{class_name}"
        )
        rng.shuffle(images)

        count = len(images)

        if count < 3:
            raise ValueError(
                f"Not enough images to split class "
                f"{class_name}: {count}"
            )

        train_count = int(count * 0.70)
        val_count = int(count * 0.15)

        # Ensure every class has at least one sample per split.
        train_count = max(1, train_count)
        val_count = max(1, val_count)

        test_count = count - train_count - val_count

        while test_count < 1:

            if train_count > 1:
                train_count -= 1
            elif val_count > 1:
                val_count -= 1
            else:
                raise ValueError(
                    f"Cannot create all three splits for "
                    f"{class_name}"
                )

            test_count = count - train_count - val_count

        assignments = [
            ("train", images[:train_count]),
            (
                "val",
                images[train_count:train_count + val_count],
            ),
            (
                "test",
                images[train_count + val_count:],
            ),
        ]

        for split_name, selected_images in assignments:

            for row in selected_images:

                split_rows[split_name].append({
                    **row,
                    "split": split_name,
                })

    return split_rows


# =========================================
# Main
# =========================================

def main():

    print("=" * 65)
    print("PREPARE COMBINED DATASET SPLITS")
    print("=" * 65)

    # -------------------------------------
    # Load the original label mapping
    # -------------------------------------

    class_to_idx = load_existing_classes()

    # -------------------------------------
    # Read original data assignments
    # -------------------------------------

    plantvillage_rows = []

    for split_name, split_file in ORIGINAL_SPLITS.items():

        plantvillage_rows.extend(
            read_original_split(
                split_name,
                split_file,
            )
        )

    # Make sure the original split files have no shared paths.
    original_paths = [
        row["image_path"]
        for row in plantvillage_rows
    ]

    if len(original_paths) != len(set(original_paths)):
        raise ValueError(
            "An image path appears more than once in the "
            "original PlantVillage splits."
        )

    original_classes = {
        row["class_name"]
        for row in plantvillage_rows
    }

    missing_original_classes = (
        set(class_to_idx) - original_classes
    )

    unknown_original_classes = (
        original_classes - set(class_to_idx)
    )

    if missing_original_classes or unknown_original_classes:
        raise ValueError(
            "PlantVillage split labels do not match "
            "the checkpoint class mapping.\n"
            f"Missing: {sorted(missing_original_classes)}\n"
            f"Unknown: {sorted(unknown_original_classes)}"
        )

    # -------------------------------------
    # Read external data
    # -------------------------------------

    external_rows = read_external_manifest()

    external_classes = {
        row["class_name"]
        for row in external_rows
    }

    # -------------------------------------
    # Identify overlapping classes
    # -------------------------------------

    shared_classes = (
        external_classes & set(class_to_idx)
    )

    new_classes = sorted(
        external_classes - set(class_to_idx)
    )

    print("\nExisting classes:", len(class_to_idx))
    print("External classes:", len(external_classes))

    print("\nShared classes:")

    for name in sorted(shared_classes):
        print(f"  {name}")

    print("\nNew classes to add:")

    for name in new_classes:
        print(f"  {name}")

    # -------------------------------------
    # Expand mapping without renumbering
    # old checkpoint classes
    # -------------------------------------

    combined_class_to_idx = dict(class_to_idx)

    next_index = max(
        combined_class_to_idx.values(),
        default=-1,
    ) + 1

    for class_name in new_classes:

        combined_class_to_idx[class_name] = next_index

        next_index += 1

    print(
        "\nExpected combined class count:",
        len(combined_class_to_idx),
    )

    # -------------------------------------
    # Verify all external labels are mapped
    # -------------------------------------

    unmapped_classes = (
        external_classes - set(combined_class_to_idx)
    )

    if unmapped_classes:
        raise ValueError(
            f"Unmapped external classes: "
            f"{sorted(unmapped_classes)}"
        )

    # -------------------------------------
    # Split external images
    # -------------------------------------

    external_splits = split_external_by_class(
        external_rows
    )

    # -------------------------------------
    # Combine existing and external data
    # -------------------------------------

    all_rows = {
        "train": [],
        "val": [],
        "test": [],
    }

    for row in plantvillage_rows:
        all_rows[row["split"]].append(row)

    for split_name in all_rows:
        all_rows[split_name].extend(
            external_splits[split_name]
        )

    # -------------------------------------
    # Assign numeric labels
    # -------------------------------------

    for split_name, rows in all_rows.items():

        for row in rows:
            row["class_idx"] = combined_class_to_idx[
                row["class_name"]
            ]

        rows.sort(
            key=lambda row: (
                row["class_idx"],
                row["image_path"].lower(),
            )
        )

    # -------------------------------------
    # Validate split coverage
    # -------------------------------------

    expected_classes = set(combined_class_to_idx)

    for split_name, rows in all_rows.items():

        if len(rows) != len({
            row["image_path"]
            for row in rows
        }):
            raise ValueError(
                f"Duplicate image paths in {split_name}."
            )

        present_classes = {
            row["class_name"]
            for row in rows
        }

        missing = expected_classes - present_classes

        if missing:
            raise ValueError(
                f"{split_name} is missing classes: "
                f"{sorted(missing)}"
            )

    # Verify the same external image is not assigned
    # to multiple splits.
    split_by_path = {}

    for split_name, rows in all_rows.items():

        for row in rows:

            path = row["image_path"]

            previous_split = split_by_path.get(path)

            if previous_split is not None:
                if previous_split != split_name:
                    raise ValueError(
                        f"Image leakage detected: {path}"
                    )

            split_by_path[path] = split_name

    # -------------------------------------
    # Write new outputs only
    # -------------------------------------

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "split",
        "dataset",
        "source_class",
        "class_name",
        "class_idx",
        "image_path",
        "extension",
    ]

    for split_name, rows in all_rows.items():

        output_file = (
            OUTPUT_DIR
            / f"combined_{split_name}.csv"
        )

        with open(
            output_file,
            "w",
            newline="",
            encoding="utf-8-sig",
        ) as file:

            writer = csv.DictWriter(
                file,
                fieldnames=fields,
            )

            writer.writeheader()
            writer.writerows(rows)

        print(
            f"\nCreated {output_file.name}: "
            f"{len(rows):,} images"
        )

    # -------------------------------------
    # Save final mapping
    # -------------------------------------

    mapping_file = (
        OUTPUT_DIR
        / "combined_class_to_idx.json"
    )

    with open(
        mapping_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            combined_class_to_idx,
            file,
            indent=4,
            ensure_ascii=False,
        )

    # -------------------------------------
    # Save summary
    # -------------------------------------

    summary = {
        "seed": SEED,
        "existing_class_count": len(class_to_idx),
        "external_class_count": len(external_classes),
        "shared_classes": sorted(shared_classes),
        "new_classes": new_classes,
        "combined_class_count": len(combined_class_to_idx),
        "plantvillage_image_count": len(plantvillage_rows),
        "external_image_count": len(external_rows),
        "split_counts": {
            name: len(rows)
            for name, rows in all_rows.items()
        },
        "class_counts_by_split": {
            name: dict(
                Counter(row["class_name"] for row in rows)
            )
            for name, rows in all_rows.items()
        },
    }

    summary_file = OUTPUT_DIR / "combined_summary.json"

    with open(
        summary_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            summary,
            file,
            indent=4,
            ensure_ascii=False,
        )

    # -------------------------------------
    # Summary
    # -------------------------------------

    print("\n" + "=" * 65)
    print("COMBINED SPLITS PREPARED")
    print("=" * 65)

    print(
        "PlantVillage images:",
        f"{len(plantvillage_rows):,}",
    )

    print(
        "External images:",
        f"{len(external_rows):,}",
    )

    print(
        "Total images:",
        f"{sum(len(rows) for rows in all_rows.values()):,}",
    )

    print(
        "Total classes:",
        len(combined_class_to_idx),
    )

    print("\nOutput directory:")
    print(OUTPUT_DIR)

    print("\nThe original split files and model checkpoint")
    print("were not modified.")


if __name__ == "__main__":
    main()