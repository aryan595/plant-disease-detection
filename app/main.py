import base64
import json
from io import BytesIO
from pathlib import Path

import cv2
import numpy as np

from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from PIL import Image

from app.predictor import PlantDiseasePredictor
from app.gradcam_service import GradCAMService
from app.chat_routes import router as chat_router


# =========================================
# Paths and configuration
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DISEASE_INFO_FILE = (
    PROJECT_ROOT / "app" / "disease_info.json"
)

MAX_FILE_SIZE = 10 * 1024 * 1024

MAX_IMAGE_WIDTH = 6000
MAX_IMAGE_HEIGHT = 6000

LOW_CONFIDENCE_THRESHOLD = 0.70

ALLOWED_CONTENT_TYPES = {
    "image/jpeg",
    "image/png",
    "image/webp",
}


# =========================================
# Load disease information
# =========================================

with open(DISEASE_INFO_FILE, "r", encoding="utf-8") as f:
    disease_info = json.load(f)

print(
    f"Loaded disease information for "
    f"{len(disease_info)} classes."
)


# =========================================
# FastAPI
# =========================================

app = FastAPI(
    title="Plant Disease Detection API",
    description="Plant disease detection using EfficientNet-B0",
    version="1.1.0",
)
app.include_router(chat_router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================
# Load models
# =========================================

predictor = PlantDiseasePredictor()
gradcam_service = GradCAMService(predictor)


# =========================================
# Parse model class names
# =========================================

def parse_class_name(class_name):
    parts = class_name.split("___", 1)

    if len(parts) == 2:
        plant = parts[0].replace("_", " ").strip()
        disease = parts[1].replace("_", " ").strip()
    else:
        plant = class_name.replace("_", " ").strip()
        disease = "Unknown"

    return plant, disease


# =========================================
# Step 35: Image quality assessment
# =========================================

def assess_image_quality(image):
    """
    Run basic image-quality checks.

    These checks identify some potentially unsuitable images.
    They do not determine whether an image actually contains
    a plant leaf.
    """

    warnings = []

    image_array = np.asarray(
        image.convert("RGB")
    )

    height, width = image_array.shape[:2]

    # -------------------------------------
    # Image resolution
    # -------------------------------------

    if min(width, height) < 160:
        warnings.append(
            "The image resolution is low."
        )

    # -------------------------------------
    # Convert to grayscale for quality tests
    # -------------------------------------

    gray = cv2.cvtColor(
        image_array,
        cv2.COLOR_RGB2GRAY,
    )

    # -------------------------------------
    # Blur detection
    # -------------------------------------

    blur_score = cv2.Laplacian(
        gray,
        cv2.CV_64F,
    ).var()

    if blur_score < 10:
        warnings.append(
            "The image may be blurry or out of focus."
        )

    # -------------------------------------
    # Brightness detection
    # -------------------------------------

    brightness = float(
        np.mean(gray)
    )

    if brightness < 25:
        warnings.append(
            "The image appears very dark."
        )

    elif brightness > 235:
        warnings.append(
            "The image appears excessively bright."
        )

    # -------------------------------------
    # Contrast detection
    # -------------------------------------

    contrast = float(
        np.std(gray)
    )

    if contrast < 12:
        warnings.append(
            "The image has very low contrast."
        )

    return warnings


# =========================================
# Validate uploaded images
# =========================================

async def validate_image(file: UploadFile):

    # -------------------------------------
    # Check file type
    # -------------------------------------

    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(
            status_code=400,
            detail=(
                "Invalid file type. Upload a JPG, "
                "PNG, or WEBP image."
            ),
        )

    # -------------------------------------
    # Read contents
    # -------------------------------------

    contents = await file.read()

    if len(contents) == 0:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is empty.",
        )

    # -------------------------------------
    # Check file size
    # -------------------------------------

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=413,
            detail="Image is too large. Maximum size is 10 MB.",
        )

    # -------------------------------------
    # Verify image
    # -------------------------------------

    try:
        with Image.open(BytesIO(contents)) as check_image:
            check_image.verify()

        with Image.open(BytesIO(contents)) as opened_image:
            image = opened_image.convert("RGB")

    except Exception:
        raise HTTPException(
            status_code=400,
            detail="The uploaded file is not a valid image.",
        )

    # -------------------------------------
    # Check dimensions
    # -------------------------------------

    width, height = image.size

    if width > MAX_IMAGE_WIDTH or height > MAX_IMAGE_HEIGHT:
        raise HTTPException(
            status_code=400,
            detail=(
                "Image dimensions are too large. "
                "Maximum allowed dimensions are 6000 × 6000."
            ),
        )

    return image


# =========================================
# Generate Grad-CAM overlay
# =========================================

def create_gradcam_image(original_image, heatmap):

    original = np.asarray(
        original_image.convert("RGB")
    )

    heatmap_uint8 = (
        np.clip(heatmap, 0, 1) * 255
    ).astype(np.uint8)

    colored_heatmap = cv2.applyColorMap(
        heatmap_uint8,
        cv2.COLORMAP_JET,
    )

    colored_heatmap = cv2.cvtColor(
        colored_heatmap,
        cv2.COLOR_BGR2RGB,
    )

    overlay = cv2.addWeighted(
        original,
        0.5,
        colored_heatmap,
        0.5,
        0,
    )

    buffer = BytesIO()

    Image.fromarray(overlay).save(
        buffer,
        format="PNG",
    )

    encoded = base64.b64encode(
        buffer.getvalue()
    ).decode("utf-8")

    return f"data:image/png;base64,{encoded}"


# =========================================
# Get friendly class information
# =========================================

def get_display_information(class_name):

    plant, disease = parse_class_name(class_name)

    info = disease_info.get(
        class_name,
        {},
    )

    plant = info.get("plant", plant)
    disease = info.get("disease", disease)

    return plant, disease, info


# =========================================
# Root endpoint
# =========================================

@app.get("/")
def root():

    return {
        "message": "Plant Disease Detection API is running!",
        "model": "EfficientNet-B0",
        "classes": len(predictor.classes),
        "device": str(predictor.device),
        "disease_info_classes": len(disease_info),
    }


# =========================================
# Prediction endpoint
# =========================================

@app.post("/predict")
async def predict(file: UploadFile = File(...)):

    image = await validate_image(file)

    results = predictor.predict(image)

    best = results[0]

    plant, disease, info = get_display_information(
        best["class"]
    )

    top_predictions = []

    for prediction in results:

        result_plant, result_disease, _ = (
            get_display_information(
                prediction["class"]
            )
        )

        top_predictions.append({
            "plant": result_plant,
            "disease": result_disease,
            "confidence": round(
                prediction["confidence"] * 100,
                2,
            ),
        })

    image_quality_warnings = assess_image_quality(image)

    return {
        "filename": file.filename,
        "plant": plant,
        "disease": disease,
        "is_healthy": disease.strip().lower() == "healthy",
        "confidence": round(
            best["confidence"] * 100,
            2,
        ),
        "description": info.get(
            "description",
            "No additional information is available.",
        ),
        "symptoms": info.get("symptoms", []),
        "management": info.get("management", []),
        "prevention": info.get("prevention", []),
        "top_3": top_predictions[:3],
        "image_quality_warnings": image_quality_warnings,
    }


# =========================================
# Grad-CAM endpoint
# =========================================

@app.post("/gradcam")
async def gradcam(file: UploadFile = File(...)):

    image = await validate_image(file)

    result = gradcam_service.generate(image)

    plant, disease, _ = get_display_information(
        result["class"]
    )

    gradcam_image = create_gradcam_image(
        image,
        result["heatmap"],
    )

    return {
        "filename": file.filename,
        "plant": plant,
        "disease": disease,
        "confidence": round(
            result["confidence"] * 100,
            2,
        ),
        "gradcam_image": gradcam_image,
        "image_quality_warnings": assess_image_quality(image),
    }


# =========================================
# Combined analysis endpoint
# =========================================

@app.post("/analyze")
async def analyze(file: UploadFile = File(...)):

    # -------------------------------------
    # Step 1: Validate uploaded image
    # -------------------------------------

    image = await validate_image(file)

    # -------------------------------------
    # Step 2: Assess basic image quality
    # -------------------------------------

    quality_warnings = assess_image_quality(image)

    # -------------------------------------
    # Step 3: Run prediction + Grad-CAM
    # -------------------------------------

    result = gradcam_service.analyze(image)

    best_class = result["class"]

    plant, disease, info = get_display_information(
        best_class
    )

    confidence_score = float(
        result["confidence"]
    )

    confidence_percent = round(
        confidence_score * 100,
        2,
    )

    is_healthy = (
        disease.strip().lower() == "healthy"
    )

    # -------------------------------------
    # Step 4: Build top-3 predictions
    # -------------------------------------

    top_predictions = []

    for prediction in result["top_3"]:

        result_plant, result_disease, _ = (
            get_display_information(
                prediction["class"]
            )
        )

        top_predictions.append({
            "plant": result_plant,
            "disease": result_disease,
            "confidence": round(
                prediction["confidence"] * 100,
                2,
            ),
        })

    # -------------------------------------
    # Step 5: Construct warnings
    # -------------------------------------

    warnings = []

    if confidence_score < LOW_CONFIDENCE_THRESHOLD:
        warnings.append(
            "The model is not highly confident in this "
            "prediction. Upload a clearer close-up image "
            "of a single leaf, or verify the result with "
            "a plant-disease professional."
        )

    if quality_warnings:
        warnings.append(
            "Image quality check: "
            + " ".join(quality_warnings)
            + " Try uploading a sharp, well-lit image "
              "with the leaf clearly visible."
        )

    # -------------------------------------
    # Step 6: Determine status
    # -------------------------------------

    if warnings:
        confidence_status = "low"
        confidence_warning = " ".join(warnings)

    elif is_healthy:
        confidence_status = "healthy"
        confidence_warning = None

    else:
        confidence_status = "high"
        confidence_warning = None

    # -------------------------------------
    # Step 7: Generate Grad-CAM image
    # -------------------------------------

    gradcam_image = create_gradcam_image(
        image,
        result["heatmap"],
    )

    # -------------------------------------
    # Step 8: Return analysis
    # -------------------------------------

    return {
        "filename": file.filename,
        "plant": plant,
        "disease": disease,
        "is_healthy": is_healthy,
        "confidence": confidence_percent,
        "confidence_status": confidence_status,
        "confidence_warning": confidence_warning,
        "image_quality_warnings": quality_warnings,
        "prediction_review_required": bool(warnings),
        "description": info.get(
            "description",
            "No additional information is available.",
        ),
        "symptoms": info.get("symptoms", []),
        "management": info.get("management", []),
        "prevention": info.get("prevention", []),
        "top_3": top_predictions,
        "gradcam_image": gradcam_image,
    }