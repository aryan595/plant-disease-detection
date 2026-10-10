from pathlib import Path

from PIL import Image

from app.predictor import PlantDiseasePredictor


# =========================================
# Project paths
# =========================================

PROJECT_ROOT = (
    Path(__file__).resolve().parent.parent
)


# =========================================
# Pick one test image
# =========================================

IMAGE_PATH = (
    PROJECT_ROOT
    / "PlantVillage-Dataset"
    / "raw"
    / "color"
    / "Apple___Black_rot"
)


# Find first JPG
image_files = list(
    IMAGE_PATH.glob("*.JPG")
)

if not image_files:
    image_files = list(
        IMAGE_PATH.glob("*.jpg")
    )

if not image_files:
    raise FileNotFoundError(
        "No JPG image found."
    )


image_file = image_files[0]


# =========================================
# Load image
# =========================================

image = Image.open(
    image_file
)


# =========================================
# Create predictor
# =========================================

predictor = (
    PlantDiseasePredictor()
)


# =========================================
# Predict
# =========================================

results = predictor.predict(
    image
)


# =========================================
# Print
# =========================================

print()
print("=" * 60)
print("PREDICTION TEST")
print("=" * 60)

print()
print("Image:", image_file.name)

print()

for rank, result in enumerate(
    results,
    start=1
):

    print(
        f"{rank}. "
        f"{result['class']} "
        f"→ "
        f"{result['confidence'] * 100:.2f}%"
    )

print()
print("✅ Predictor class works!")