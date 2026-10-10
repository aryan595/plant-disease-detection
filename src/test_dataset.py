from pathlib import Path

from plant_dataset import PlantDiseaseDataset


# ---------------------------------
# Project paths
# ---------------------------------
PROJECT_ROOT = Path(__file__).resolve().parent.parent

TRAIN_FILE = (
    PROJECT_ROOT
    / "data"
    / "splits"
    / "color_train_final.txt"
)

DATASET_ROOT = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
)


# ---------------------------------
# Create dataset
# ---------------------------------
dataset = PlantDiseaseDataset(
    split_file=TRAIN_FILE,
    dataset_root=DATASET_ROOT
)


# ---------------------------------
# Print basic information
# ---------------------------------
print("Dataset loaded successfully!")
print()

print("Number of images:", len(dataset))
print("Number of classes:", len(dataset.classes))

print()
print("First 10 classes:")

for index, class_name in enumerate(dataset.classes[:10]):
    print(f"{index}: {class_name}")


# ---------------------------------
# Load one image
# ---------------------------------
image, label = dataset[0]

print()
print("First sample:")
print("Image type:", type(image))
print("Label:", label)
print("Class:", dataset.classes[label])
print("Image size:", image.size)