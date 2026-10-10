from pathlib import Path
from collections import Counter


# =========================================
# Project paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATASET_ROOT = PROJECT_ROOT / "data" / "external"

DATASET_NAMES = [
    "grape",
    "sugarcane",
    "cotton",
    "soybean",
]

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
# Helpers
# =========================================

def is_image_file(path):
    return (
        path.is_file()
        and path.suffix.lower() in IMAGE_EXTENSIONS
    )


def count_direct_images(folder):
    return sum(
        1
        for item in folder.iterdir()
        if is_image_file(item)
    )


def inspect_dataset(dataset_name):

    root = DATASET_ROOT / dataset_name

    print("\n" + "=" * 65)
    print(f"DATASET: {dataset_name.upper()}")
    print("=" * 65)

    if not root.exists():
        print(f"ERROR: Folder not found: {root}")
        return

    if not root.is_dir():
        print(f"ERROR: Expected a directory: {root}")
        return

    all_images = [
        path
        for path in root.rglob("*")
        if is_image_file(path)
    ]

    print(f"Dataset path: {root}")
    print(f"Total image files: {len(all_images):,}")

    if not all_images:
        print(
            "No images found. Check whether the dataset "
            "was extracted into another location."
        )
        return

    # -------------------------------------
    # File extension counts
    # -------------------------------------

    extension_counts = Counter(
        path.suffix.lower()
        for path in all_images
    )

    print("\nImage formats:")

    for extension, count in sorted(
        extension_counts.items()
    ):
        print(f"  {extension}: {count:,}")

    # -------------------------------------
    # Folders containing images directly
    # -------------------------------------

    folder_counts = Counter(
        path.parent
        for path in all_images
    )

    print("\nFolders containing images directly:")

    for folder, count in sorted(
        folder_counts.items(),
        key=lambda item: str(item[0]).lower(),
    ):

        relative_path = folder.relative_to(root)

        print(
            f"  {relative_path.as_posix()}/"
            f"  -> {count:,} images"
        )

    # -------------------------------------
    # Overview of directory structure
    # -------------------------------------

    print("\nDirectory structure (up to 3 levels):")
    print(f"  {root.name}/")

    directories = sorted(
        (
            path
            for path in root.rglob("*")
            if path.is_dir()
        ),
        key=lambda path: str(path).lower(),
    )

    for directory in directories:

        relative_path = directory.relative_to(root)

        depth = len(relative_path.parts)

        if depth > 3:
            continue

        indent = "  " * depth

        direct_count = count_direct_images(directory)

        suffix = (
            f" [{direct_count:,} images]"
            if direct_count
            else ""
        )

        print(
            f"{indent}{directory.name}/{suffix}"
        )


# =========================================
# Main
# =========================================

def main():

    print("EXTERNAL PLANT DATASET INSPECTOR")
    print(f"Project root: {PROJECT_ROOT}")

    for dataset_name in DATASET_NAMES:
        inspect_dataset(dataset_name)

    print("\n" + "=" * 65)
    print("INSPECTION COMPLETE")
    print("No dataset files were changed.")
    print("=" * 65)


if __name__ == "__main__":
    main()