import csv
import re
from collections import Counter
from pathlib import Path


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_ROOT = PROJECT_ROOT / "data" / "external"

OUTPUT_FILE = PROJECT_ROOT / "data" / "external_manifest.csv"


# =========================================
# Supported image formats
# =========================================

IMAGE_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".bmp",
    ".webp",
    ".tif",
    ".tiff",
}


# =========================================
# Standardized class mappings
#
# Folder name -> canonical model class
# =========================================

CLASS_MAPS = {

    "grape": {
        "bacterialleafspot": "Grape___Bacterial_leaf_spot",
        "downymildew": "Grape___Downy_mildew",
        "healthyleaves": "Grape___healthy",
        "powderymildew": "Grape___Powdery_mildew",
    },

    "sugarcane": {
        "healthy": "Sugarcane___healthy",
        "mosaic": "Sugarcane___Mosaic",
        "redrot": "Sugarcane___Red_rot",
        "rust": "Sugarcane___Rust",
        "yellow": "Sugarcane___Yellow_disease",
    },

    "cotton": {
        "alternarialeafspot": "Cotton___Alternaria_leaf_spot",
        "bacterialblight": "Cotton___Bacterial_blight",
        "fusariumwilt": "Cotton___Fusarium_wilt",
        "healthyleaf": "Cotton___healthy",
        "verticilliumwilt": "Cotton___Verticillium_wilt",
    },

    "soybean": {
        "bacterialblight": "Soybean___Bacterial_blight",
        "cercosporaleafblight": "Soybean___Cercospora_leaf_blight",
        "healthy": "Soybean___healthy",
        "rust": "Soybean___Rust",
        "suddendeathsyndrome": "Soybean___Sudden_death_syndrome",
    },
}


# =========================================
# Helpers
# =========================================

def normalize_folder_name(name):
    """
    Normalize folder names to match labels despite
    spaces, underscores, hyphens, and capitalization.
    """

    return re.sub(
        r"[^a-z0-9]",
        "",
        name.lower(),
    )


def is_image(path):
    return (
        path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


# =========================================
# Build manifest
# =========================================

def main():

    rows = []

    class_counts = Counter()

    dataset_counts = Counter()

    unmapped_folders = set()

    missing_datasets = []


    for dataset_name, class_map in CLASS_MAPS.items():

        dataset_path = DATASET_ROOT / dataset_name

        print(f"\nInspecting {dataset_name}...")

        if not dataset_path.is_dir():

            missing_datasets.append(
                str(dataset_path)
            )

            print(
                f"  MISSING: {dataset_path}"
            )

            continue


        image_files = sorted(
            (
                path
                for path in dataset_path.rglob("*")
                if is_image(path)
            ),
            key=lambda path: str(path).lower(),
        )


        for image_path in image_files:

            source_class = image_path.parent.name

            normalized_class = normalize_folder_name(
                source_class
            )

            canonical_class = class_map.get(
                normalized_class
            )


            # Never silently guess unknown labels

            if canonical_class is None:

                unmapped_folders.add(
                    (
                        dataset_name,
                        source_class,
                    )
                )

                continue


            rows.append({

                "dataset": dataset_name,

                "source_class": source_class,

                "canonical_class": canonical_class,

                "image_path": str(
                    image_path.resolve()
                ),

                "extension": image_path.suffix.lower(),

            })


            dataset_counts[dataset_name] += 1

            class_counts[
                (
                    dataset_name,
                    source_class,
                    canonical_class,
                )
            ] += 1


    # =====================================
    # Report problems before writing
    # =====================================

    if missing_datasets:

        print("\nERROR: Dataset folders are missing.")

        for path in missing_datasets:
            print(f"  {path}")

        print("\nNo manifest was written.")

        return


    if unmapped_folders:

        print("\nERROR: Unrecognized class folders:")

        for dataset, folder in sorted(unmapped_folders):
            print(f"  {dataset}: {folder}")

        print(
            "\nNo manifest was written. "
            "We need to inspect these labels first."
        )

        return


    # =====================================
    # Write manifest
    # =====================================

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )


    fieldnames = [
        "dataset",
        "source_class",
        "canonical_class",
        "image_path",
        "extension",
    ]


    with open(
        OUTPUT_FILE,
        "w",
        newline="",
        encoding="utf-8-sig",
    ) as csvfile:

        writer = csv.DictWriter(
            csvfile,
            fieldnames=fieldnames,
        )

        writer.writeheader()

        writer.writerows(rows)


    # =====================================
    # Summary
    # =====================================

    print("\n" + "=" * 65)

    print("EXTERNAL DATASET MANIFEST CREATED")

    print("=" * 65)


    for dataset_name in CLASS_MAPS:

        print(
            f"\n{dataset_name.upper()}: "
            f"{dataset_counts[dataset_name]:,} images"
        )


        for (
            source_dataset,
            source_class,
            canonical_class,
        ), count in sorted(class_counts.items()):

            if source_dataset != dataset_name:
                continue

            print(
                f"  {source_class} -> "
                f"{canonical_class}: {count:,}"
            )


    unique_external_classes = {
        row["canonical_class"]
        for row in rows
    }


    print("\nTotal images:", f"{len(rows):,}")

    print(
        "Unique standardized classes:",
        len(unique_external_classes),
    )

    print("\nManifest saved to:")

    print(OUTPUT_FILE)

    print(
        "\nOriginal image files were not moved or modified."
    )


if __name__ == "__main__":
    main()