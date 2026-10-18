import base64
import json
import os
from io import BytesIO
from pathlib import Path
from typing import Optional
from PIL import Image

import cv2
import numpy as np

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from app.predictor import PlantDiseasePredictor
from app.gradcam_service import GradCAMService
from app.chat_routes import router as chat_router
from fastapi.responses import Response

from agrisense.core.severity import estimate_severity
from agrisense.core.weather import (
    fetch_live_weather,
    evaluate_progression_warning,
    calculate_spray_window,
    get_all_districts,
)
from agrisense.core.timeline import generate_disease_timeline
from agrisense.core.report_generator import generate_pdf_report
from agrisense.data.treatments_db import get_treatment_for_disease
from agrisense.data.mandi_db import get_mandi_rates_for_crop
from agrisense.core.tts import synthesize_advisory_speech
from agrisense.data.compatibility_db import CHEMICAL_DATABASE, check_tank_mix_compatibility
from agrisense.core.forecast import fetch_7day_epidemic_forecast
from agrisense.data.krishi_kendra_db import get_krishi_kendras_for_district
from agrisense.core.recovery_tracker import compare_leaf_recovery
from agrisense.core.pmfby_generator import generate_pmfby_claim_certificate


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

cors_origins_env = os.getenv("CORS_ORIGINS", "").strip()
cors_origins_list = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5174",
    "http://127.0.0.1:5174",
    "http://localhost:5175",
    "http://127.0.0.1:5175",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if cors_origins_env and cors_origins_env != "*":
    for item in cors_origins_env.split(","):
        cleaned = item.strip()
        if cleaned:
            cors_origins_list.append(cleaned)

if cors_origins_env == "*":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_origins_list,
        allow_origin_regex=r"^https?://.*",
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
# Plant Foliage & Out-of-Distribution (OOD) Verification
# =========================================

YUNET_MODEL_PATH = PROJECT_ROOT / "models" / "face_detection_yunet_2023mar.onnx"
_face_detector = None


def get_face_detector():
    """Lazily load and cache OpenCV YuNet state-of-the-art face detector."""
    global _face_detector
    if _face_detector is None and YUNET_MODEL_PATH.exists():
        try:
            _face_detector = cv2.FaceDetectorYN.create(
                model=str(YUNET_MODEL_PATH),
                config="",
                input_size=(320, 320),
                score_threshold=0.35,  # High sensitivity for face, selfie, tilted, or webcam portraits
                nms_threshold=0.3,
                top_k=50,
            )
        except Exception as e:
            print(f"Warning: Could not initialize YuNet face detector: {e}")
            _face_detector = False
    return _face_detector if _face_detector is not False else None


def check_human_face(img_rgb: np.ndarray):
    """
    Detect human faces using OpenCV's YuNet ONNX deep learning detector.
    Returns (face_detected: bool, max_confidence: float).
    """
    detector = get_face_detector()
    if detector is None:
        return False, 0.0

    try:
        h, w = img_rgb.shape[:2]
        max_dim = max(h, w)
        scale = min(1.0, 640.0 / max_dim)
        nw = max(32, (int(w * scale) // 2) * 2)
        nh = max(32, (int(h * scale) // 2) * 2)

        img_bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        resized = cv2.resize(img_bgr, (nw, nh))

        detector.setInputSize((nw, nh))
        _, faces = detector.detect(resized)
        if faces is not None and len(faces) > 0:
            best_conf = float(np.max(faces[:, -1]))
            return True, best_conf
    except Exception as e:
        print(f"Warning: Error during face detection check: {e}")

    return False, 0.0


def validate_plant_leaf(image: Image.Image):
    """
    Bio-chromatic and Out-of-Distribution (OOD) verification gate.
    Ensures that uploaded images contain genuine plant foliage and rejects:
    - Human faces / portraits / selfies (via YuNet AI neural detector)
    - Skin-dominant photos (portraits, hands without leaves, chest/body)
    - Non-plant objects (paper, screens, walls, furniture, cars, textiles)
    """
    img_rgb = np.asarray(image.convert("RGB"))

    # Stage 1: Color Space Analysis
    ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
    cr = ycrcb[:, :, 1]
    cb = ycrcb[:, :, 2]
    skin_pixels = (cr >= 133) & (cr <= 173) & (cb >= 77) & (cb <= 127)
    skin_ratio = float(np.mean(skin_pixels))

    hsv = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2HSV)
    h = hsv[:, :, 0]
    s = hsv[:, :, 1]
    v = hsv[:, :, 2]
    green_mask = (h >= 24) & (h <= 88) & (s >= 25) & (v >= 25)
    green_ratio = float(np.mean(green_mask))

    # Stage 2: AI Human Face Detection (YuNet Neural Network)
    has_face, face_conf = check_human_face(img_rgb)
    if has_face:
        # Confirm true human portrait (high confidence or skin presence without leaf foliage)
        is_true_face = (face_conf >= 0.60) or (face_conf >= 0.35 and (skin_ratio > 0.05 or green_ratio < 0.15))
        if is_true_face:
            return False, "HUMAN_DETECTED", (
                f"🚫 Human face detected ({face_conf * 100:.0f}% confidence)! AgriSense is an agricultural crop disease detection system. "
                "Please upload a clear photograph focused on a plant leaf (e.g., Tomato, Grape, Soybean), not a human face or selfie."
            )

    # Chlorotic yellow halos/spots
    yellow_mask = (h >= 14) & (h < 24) & (s >= 35) & (v >= 35)
    yellow_ratio = float(np.mean(yellow_mask))
    yellow_mask = (h >= 14) & (h < 24) & (s >= 35) & (v >= 35)
    yellow_ratio = float(np.mean(yellow_mask))

    # Excess Green Index (ExG = 2*G - R - B) - true biological chlorophyll indicator
    r = img_rgb[:, :, 0].astype(float)
    g = img_rgb[:, :, 1].astype(float)
    b = img_rgb[:, :, 2].astype(float)
    exg = 2 * g - r - b
    exg_ratio = float(np.mean(exg > 8))

    # Check: Human Skin Dominance (e.g., selfie where face was off-angle, close-up of skin, body without leaf)
    if skin_ratio > 0.10 and green_ratio < 0.08:
        return False, "HUMAN_DETECTED", (
            f"🚫 Human portrait or skin detected ({skin_ratio * 100:.0f}% skin coverage). "
            "AgriSense is designed for plant leaves. Please upload a photograph of a crop leaf."
        )

    # Check: Non-plant Object / Blank / Wall / Paper / Screen / Furniture
    # A genuine crop leaf must have either green canopy or strong chlorophyll ExG
    if green_ratio < 0.04 and exg_ratio < 0.03:
        if yellow_ratio > 0.08:
            # Rare severe chlorotic leaf
            pass
        else:
            return False, "NON_PLANT_DETECTED", (
                "🚫 No plant leaf detected in this photo. Please upload a clear photo of a crop leaf "
                "(e.g., Tomato, Grape, Potato, Soybean, Corn) under natural lighting."
            )

    return True, "VALID_LEAF", "Plant foliage verified."


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
    """
    State-of-the-art Grad-CAM visualization with bio-chromatic foliage masking.
    Highlights actual disease lesions in vivid red/yellow heatmaps while preserving
    natural leaf texture and suppressing background table/indoor artifacts.
    """
    original = np.asarray(original_image.convert("RGB"))
    h_orig, w_orig = original.shape[:2]

    # Resize heatmap to match image dimensions
    if heatmap.shape[:2] != (h_orig, w_orig):
        heatmap_resized = cv2.resize(heatmap, (w_orig, h_orig), interpolation=cv2.INTER_CUBIC)
    else:
        heatmap_resized = heatmap
    heatmap_resized = np.clip(heatmap_resized, 0.0, 1.0)

    # Segment foliage / leaf areas using HSV
    hsv = cv2.cvtColor(original, cv2.COLOR_RGB2HSV)
    h_ch, s_ch, v_ch = hsv[:, :, 0], hsv[:, :, 1], hsv[:, :, 2]

    green_mask = (h_ch >= 22) & (h_ch <= 90) & (s_ch >= 20) & (v_ch >= 20)
    yellow_mask = (h_ch >= 12) & (h_ch < 22) & (s_ch >= 25) & (v_ch >= 25)
    brown_mask = (h_ch >= 4) & (h_ch < 22) & (s_ch >= 20) & (v_ch >= 15) & (v_ch <= 210)

    leaf_mask = (green_mask | yellow_mask | brown_mask).astype(np.float32)

    # If leaf detected in image, smooth it to softly bound the saliency
    if np.mean(leaf_mask) > 0.04:
        kernel = np.ones((7, 7), np.uint8)
        leaf_mask = cv2.dilate(leaf_mask, kernel, iterations=2)
        leaf_mask = cv2.GaussianBlur(leaf_mask, (15, 15), 0)
        # Saliency threshold: only highlight activations above noise floor
        alpha = np.clip((heatmap_resized - 0.15) / 0.85, 0.0, 1.0)
        alpha = (alpha ** 1.2) * np.clip(leaf_mask * 1.2, 0.0, 1.0)
    else:
        alpha = np.clip((heatmap_resized - 0.20) / 0.80, 0.0, 1.0) ** 1.3

    alpha = np.expand_dims(alpha, axis=-1)

    # Colorize using JET colormap
    heatmap_uint8 = (heatmap_resized * 255).astype(np.uint8)
    colored_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    colored_rgb = cv2.cvtColor(colored_heatmap, cv2.COLOR_BGR2RGB).astype(np.float32)

    overlay = (1.0 - 0.70 * alpha) * original.astype(np.float32) + (0.70 * alpha) * colored_rgb
    overlay = np.clip(overlay, 0, 255).astype(np.uint8)

    buffer = BytesIO()
    Image.fromarray(overlay).save(buffer, format="PNG")
    encoded = base64.b64encode(buffer.getvalue()).decode("utf-8")
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
        "model": "EfficientNet-V2-S",
        "classes": len(predictor.classes),
        "device": str(predictor.device),
        "disease_info_classes": len(disease_info),
    }


# =========================================
# Regional Districts & APMC Mandi Endpoints
# =========================================

@app.get("/districts")
def list_districts():
    """Returns list of supported agricultural districts in Maharashtra."""
    return {"districts": get_all_districts()}


@app.get("/weather")
def get_district_weather(
    district: str = "Pune (पुणे)",
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    """Fetch live weather and spray feasibility for a given district or GPS coordinates."""
    w = fetch_live_weather(district, lat=lat, lon=lon)
    spray = calculate_spray_window(w["temperature_c"], w["humidity_percent"], w["wind_speed_kmh"])
    return {
        "district": w["district"],
        "district_mr": w.get("district_mr"),
        "is_gps": w.get("is_gps", False),
        "lat": w.get("lat"),
        "lon": w.get("lon"),
        "nearest_district": w.get("nearest_district"),
        "nearest_district_mr": w.get("nearest_district_mr"),
        "distance_km": w.get("distance_km"),
        "weather": w,
        "spray_window": spray
    }


@app.get("/mandi-rates")
def get_mandi_rates(crop: str = "Tomato", district: str = "Pune (पुणे)"):
    """Returns daily APMC mandi market benchmark rates for the crop."""
    return get_mandi_rates_for_crop(crop, district)


class TTSRequest(BaseModel):
    text: str
    language: str = "mr"


@app.post("/tts")
def tts_endpoint(req: TTSRequest):
    """Synthesizes high-fidelity audio advisory speech stream via gTTS."""
    audio_bytes = synthesize_advisory_speech(req.text, req.language)
    if not audio_bytes:
        raise HTTPException(status_code=500, detail="Audio synthesis failed.")
    return Response(content=audio_bytes, media_type="audio/mpeg")


# =========================================
# Prediction endpoint
# =========================================

@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    crop: Optional[str] = Form(None),
):

    image = await validate_image(file)

    is_leaf, ood_type, ood_message = validate_plant_leaf(image)
    if not is_leaf:
        raise HTTPException(
            status_code=400,
            detail=ood_message
        )

    results = predictor.predict(image, crop=crop)

    best = results[0]

    plant, disease, info = get_display_information(
        best["class"]
    )

    top_predictions = []

    for prediction in results:

        result_plant, result_disease, result_info = (
            get_display_information(
                prediction["class"]
            )
        )

        top_predictions.append({
            "plant": result_plant,
            "disease": result_disease,
            "plant_mr": result_info.get("plant_mr", result_plant),
            "disease_mr": result_info.get("disease_mr", result_disease),
            "class_name": prediction["class"],
            "confidence": round(
                prediction["confidence"] * 100,
                2,
            ),
        })

    image_quality_warnings = assess_image_quality(image)
    confidence_score = float(best["confidence"])
    is_healthy = disease.strip().lower() == "healthy"

    # Diagnostic Safety Guardrail: Prevent false-negative "Healthy" on low confidence
    if confidence_score < 0.60 and is_healthy:
        is_healthy = False
        disease = "Inconclusive / Review Required"
        disease_mr = "अस्पष्ट / पुनर्परीक्षण आवश्यक"
        description = "Model confidence is below 60%. Please capture a clearer close-up leaf image in good light."
        description_mr = "खात्री कमी आहे (६०% पेक्षा कमी). कृपया पानाचा स्पष्ट, जवळून फोटो काढून पुनर्परीक्षण करा."
    else:
        disease_mr = info.get("disease_mr", disease)
        description = info.get("description", "No additional information is available.")
        description_mr = info.get("description_mr", description)

    return {
        "filename": file.filename,
        "class_name": best["class"],
        "plant": plant,
        "disease": disease,
        "plant_mr": info.get("plant_mr", plant),
        "disease_mr": disease_mr,
        "is_healthy": is_healthy,
        "confidence": round(
            best["confidence"] * 100,
            2,
        ),
        "description": description,
        "description_mr": description_mr,
        "symptoms": info.get("symptoms", []),
        "symptoms_mr": info.get("symptoms_mr", info.get("symptoms", [])),
        "management": info.get("management", []),
        "management_mr": info.get("management_mr", info.get("management", [])),
        "prevention": info.get("prevention", []),
        "prevention_mr": info.get("prevention_mr", info.get("prevention", [])),
        "top_3": top_predictions[:3],
        "image_quality_warnings": image_quality_warnings,
    }


# =========================================
# Grad-CAM endpoint
# =========================================

@app.post("/gradcam")
async def gradcam(
    file: UploadFile = File(...),
    crop: Optional[str] = Form(None),
):

    image = await validate_image(file)

    is_leaf, ood_type, ood_message = validate_plant_leaf(image)
    if not is_leaf:
        raise HTTPException(
            status_code=400,
            detail=ood_message
        )

    result = gradcam_service.generate(image, crop=crop)

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
async def analyze(
    file: UploadFile = File(...),
    district: str = Form("Pune (पुणे)"),
    crop: Optional[str] = Form(None),
):

    # -------------------------------------
    # Step 1: Validate uploaded image
    # -------------------------------------

    image = await validate_image(file)

    # -------------------------------------
    # Step 1b: Verify image contains plant foliage
    # -------------------------------------

    is_leaf, ood_type, ood_message = validate_plant_leaf(image)
    if not is_leaf:
        raise HTTPException(
            status_code=400,
            detail=ood_message
        )

    # -------------------------------------
    # Step 2: Assess basic image quality
    # -------------------------------------

    quality_warnings = assess_image_quality(image)

    # -------------------------------------
    # Step 3: Run prediction + Grad-CAM
    # -------------------------------------

    result = gradcam_service.analyze(image, crop=crop)

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

        result_plant, result_disease, result_info = (
            get_display_information(
                prediction["class"]
            )
        )

        top_predictions.append({
            "plant": result_plant,
            "disease": result_disease,
            "plant_mr": result_info.get("plant_mr", result_plant),
            "disease_mr": result_info.get("disease_mr", result_disease),
            "class_name": prediction["class"],
            "confidence": round(
                prediction["confidence"] * 100,
                2,
            ),
        })

    # -------------------------------------
    # Step 5: Construct warnings & Safety Guardrails
    # -------------------------------------

    warnings = []

    # Diagnostic Safety Guardrail: Prevent false-negative "Healthy" on low confidence
    if confidence_score < 0.60:
        if is_healthy:
            is_healthy = False
            disease = "Inconclusive / Review Required"
            info["disease_mr"] = "अस्पष्ट / पुनर्परीक्षण आवश्यक"
            info["description"] = (
                "The AI model confidence is too low (<60%) to confirm crop health. "
                "Please capture a sharp, close-up photograph of a single leaf in daylight."
            )
            info["description_mr"] = (
                "पानाचा फोटो पुरेशा खात्रीने तपासता आला नाही (६०% पेक्षा कमी). निरोगी समजण्यापूर्वी "
                "कृपया चांगल्या प्रकाशात जवळून स्पष्ट फोटो काढून पुन्हा तपासा."
            )
        warnings.append(
            "Confidence is below 60%. Inspect leaf lesions closely or upload a clearer close-up photograph."
        )
    elif confidence_score < LOW_CONFIDENCE_THRESHOLD:
        warnings.append(
            "The model confidence is moderate. Upload a clearer close-up image "
            "of a single leaf, or verify the result with a plant pathologist."
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

    if confidence_score < 0.60 and not is_healthy:
        confidence_status = "inconclusive"
        confidence_warning = " ".join(warnings)

    elif warnings:
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
    # Step 8: Calculate Explainable Severity & Weather Risk
    # -------------------------------------

    severity_data = estimate_severity(
        image=image,
        heatmap=result["heatmap"],
        is_healthy=is_healthy
    )

    weather_data = fetch_live_weather(district)

    progression_data = evaluate_progression_warning(
        disease_key=best_class,
        severity_level=severity_data["level"],
        humidity=weather_data["humidity_percent"],
        temp_c=weather_data["temperature_c"]
    )

    treatment_data = get_treatment_for_disease(best_class)
    mandi_data = get_mandi_rates_for_crop(plant, district)

    # -------------------------------------
    # Step 8b: Process Chemical & Organic Tank-Mix Guidance
    # -------------------------------------
    import re

    def parse_dose_num(dose_text: str) -> float:
        try:
            m = re.search(r"(\d+(?:\.\d+)?)", dose_text)
            if m:
                return float(m.group(1))
        except Exception:
            pass
        return 2.0

    raw_chemicals = treatment_data.get("chemical_treatments", [])
    standardized_chemicals = []
    for chem in raw_chemicals:
        c_name = chem.get("commercial_name") or chem.get("name", "Curative Spray")
        chem_ing = chem.get("chemical_name", "")
        dose_str = chem.get("dosage", "2.0 g/L")
        price_str = chem.get("approx_price_inr") or chem.get("cost_range_inr", "₹250 - ₹400")
        sched = chem.get("instructions") or chem.get("application_schedule", "Foliar spray on affected leaves")
        phi = chem.get("phi_days", 14)
        dose_num = parse_dose_num(dose_str)
        dose_15l = chem.get("dose_15l_pump") or f"{(dose_num * 15):.0f}g per 15L Pump (१५ लिटर पंपासाठी {(dose_num * 15):.0f} ग्रॅम)"
        spreader_15l = chem.get("spreader_15l") or "10 ml Silicon Spreader (१० मिली स्टीकर)"
        timing_str = chem.get("timing") or "Early morning before 9 AM or evening after 4 PM (शांत हवेत)"
        standardized_chemicals.append({
            "commercial_name": c_name,
            "chemical_name": chem_ing,
            "dosage": dose_str,
            "dosage_per_liter": dose_num,
            "dose_15l_pump": dose_15l,
            "spreader_15l": spreader_15l,
            "timing": timing_str,
            "approx_price_inr": price_str,
            "phi_days": phi,
            "instructions": sched
        })

    raw_organics = treatment_data.get("organic_treatments", [])
    standardized_organics = []
    for org in raw_organics:
        o_name = org.get("name", "Bio-fungicide")
        dose_str = org.get("dosage", "5 ml/L")
        price_str = org.get("approx_price_inr") or org.get("cost_range_inr", "₹150 - ₹250")
        notes = org.get("notes") or org.get("prep_instructions", "Eco-safe foliar spray")
        dose_num = parse_dose_num(dose_str)
        org_dose_15l = org.get("dose_15l_pump") or f"{(dose_num * 15):.0f}ml/g per 15L Pump"
        standardized_organics.append({
            "name": o_name,
            "dosage": dose_str,
            "dosage_per_liter": dose_num,
            "dose_15l_pump": org_dose_15l,
            "approx_price_inr": price_str,
            "notes": notes
        })

    spray_window_data = calculate_spray_window(
        temp_c=weather_data["temperature_c"],
        humidity=weather_data["humidity_percent"],
        wind_speed_kmh=weather_data["wind_speed_kmh"]
    )

    timeline_data = generate_disease_timeline(
        plant=plant,
        disease=disease,
        severity_level=severity_data["level"],
        affected_percentage=severity_data["affected_percentage"]
    )

    # -------------------------------------
    # Step 9: Return comprehensive analysis
    # -------------------------------------

    symptoms_mr = info.get("symptoms_mr", [])
    if not symptoms_mr and treatment_data.get("symptoms_mr"):
        symptoms_mr = treatment_data.get("symptoms_mr")

    management_mr = info.get("management_mr", [])
    prevention_mr = info.get("prevention_mr", treatment_data.get("preventive_measures_mr", []))

    return {
        "filename": file.filename,
        "class_name": best_class,
        "plant": plant,
        "disease": disease,
        "plant_mr": info.get("plant_mr", treatment_data.get("crop_mr", plant)),
        "disease_mr": info.get("disease_mr", treatment_data.get("display_name_mr", disease)),
        "is_healthy": is_healthy,
        "confidence": confidence_percent,
        "confidence_status": confidence_status,
        "confidence_warning": confidence_warning,
        "image_quality_warnings": quality_warnings,
        "prediction_review_required": bool(warnings),
        "description": info.get(
            "description",
            treatment_data.get("description_en", "No additional information is available."),
        ),
        "description_mr": info.get(
            "description_mr",
            treatment_data.get("description_mr", info.get("description", "माहिती उपलब्ध नाही.")),
        ),
        "symptoms": info.get("symptoms", treatment_data.get("symptoms_en", [])),
        "symptoms_mr": symptoms_mr,
        "management": info.get("management", []),
        "management_mr": management_mr,
        "prevention": info.get("prevention", treatment_data.get("preventive_measures_en", [])),
        "prevention_mr": prevention_mr,
        "top_3": top_predictions,
        "gradcam_image": gradcam_image,
        # New Major Project Features:
        "severity": {
            "level": severity_data["level"],
            "level_mr": severity_data["level_mr"],
            "affected_percentage": severity_data["affected_percentage"],
            "badge_color": severity_data["badge_color"],
            "description_en": severity_data["description_en"],
            "description_mr": severity_data["description_mr"]
        },
        "weather_progression": {
            "district": weather_data["district"],
            "temperature_c": weather_data["temperature_c"],
            "humidity_percent": weather_data["humidity_percent"],
            "wind_speed_kmh": weather_data["wind_speed_kmh"],
            "risk_level": progression_data["risk_level"],
            "risk_level_mr": progression_data["risk_level_mr"],
            "alert_title_en": progression_data["title_en"],
            "alert_title_mr": progression_data["title_mr"],
            "alert_message_en": progression_data["message_en"],
            "alert_message_mr": progression_data["message_mr"],
            "recommended_action_en": progression_data["action_en"],
            "recommended_action_mr": progression_data["action_mr"]
        },
        "spray_window": spray_window_data,
        "timeline": timeline_data,
        "tank_mix_presets": [
            {"name": "15L Knapsack Pump (नॅपसॅक पंप)", "capacity_liters": 15, "type": "knapsack", "standard_spreader_ml": 10},
            {"name": "20L Battery Sprayer (बॅटरी पंप)", "capacity_liters": 20, "type": "battery", "standard_spreader_ml": 15},
            {"name": "200L Tractor Drum (ट्रॅक्टर बॅरल)", "capacity_liters": 200, "type": "tractor", "standard_spreader_ml": 100}
        ],
        "mandi_rates": mandi_data,
        "treatment_advisory": {
            "chemical_treatments": standardized_chemicals,
            "organic_treatments": standardized_organics,
            "preventive_measures_en": treatment_data.get("preventive_measures_en", []),
            "preventive_measures_mr": treatment_data.get("preventive_measures_mr", []),
            "disclaimer": treatment_data.get("disclaimer", "")
        },
        "plain_explanation": {
            "what_happened_en": treatment_data.get("what_happened_en", f"The {plant} foliage is showing symptoms of {disease}."),
            "what_happened_mr": treatment_data.get("what_happened_mr", f"{info.get('plant_mr', plant)} पिकावर {info.get('disease_mr', disease)} चा प्रादुर्भाव आढळला आहे."),
            "why_it_happened_en": treatment_data.get("why_it_happened_en", "Environmental moisture, high humidity, and overcast skies triggered pathogen germination."),
            "why_it_happened_mr": treatment_data.get("why_it_happened_mr", "जास्त आर्द्रता, ढगाळ वातावरण आणि ओलावा यामुळे हा प्रादुर्भाव वाढला आहे."),
            "how_it_spreads_en": treatment_data.get("how_it_spreads_en", "Spreads via rain splash droplets, wind gusts, tools, and brushing against wet leaves."),
            "how_it_spreads_mr": treatment_data.get("how_it_spreads_mr", "पावसाचे उडणारे थेंब, वारा, अवजारे आणि ओल्या पानांच्या संपर्काद्वारे रोग इतर झाडांवर पसरतो."),
            "risk_if_neglected_en": treatment_data.get("risk_if_neglected_en", "Risk of rapid defoliation, sunburn on fruit, and 25-45% yield reduction if left unmanaged."),
            "risk_if_neglected_mr": treatment_data.get("risk_if_neglected_mr", "वेळेवर उपाय न केल्यास तीव्र पानगळ होऊन उत्पादनात २५ ते ४५ टक्के घट होऊ शकते."),
            "pathogen_type": treatment_data.get("pathogen_type", "Fungal 🍄"),
            "pathogen_type_mr": treatment_data.get("pathogen_type_mr", "बुरशीजन्य रोग 🍄"),
            "causal_organism": treatment_data.get("causal_organism", disease),
            "sanitation_steps_en": treatment_data.get("sanitation_steps_en", [
                "Pluck heavily spotted bottom leaves and safely bury or burn outside the field.",
                "Stop overhead sprinkler watering; irrigate strictly at the soil base using drip lines.",
                "Apply mulch around plant bases to prevent rain from splashing soil-borne spores onto leaves."
            ]),
            "sanitation_steps_mr": treatment_data.get("sanitation_steps_mr", [
                "रोगाने जास्त बाधित झालेली पाने खुडून शेताबाहेर नेऊन जाळून किंवा खड्ड्यात गाडून नष्ट करा.",
                "तुषार सिंचनाने पानांवर पाणी उडवणे टाळा; फक्त ठिबक सिंचनाने मुळाशी पाणी द्या.",
                "पावसाचे पाणी मातीतून पानांवर उडू नये म्हणून झाडाच्या बुंध्याशी आच्छादन (मल्चिंग) करा."
            ])
        }
    }


# =========================================
# Download PDF Diagnostic Report Endpoint
# =========================================

@app.post("/download-report")
async def download_report_endpoint(
    file: UploadFile = File(...),
    farmer_name: str = Form("Grower / Farmer"),
    district: str = Form("Pune (पुणे)"),
):
    image = await validate_image(file)

    is_leaf, ood_type, ood_message = validate_plant_leaf(image)
    if not is_leaf:
        raise HTTPException(
            status_code=400,
            detail=ood_message
        )

    result = gradcam_service.analyze(image)
    best_class = result["class"]
    plant, disease, info = get_display_information(best_class)
    is_healthy = disease.strip().lower() == "healthy"

    severity_data = estimate_severity(
        image=image,
        heatmap=result["heatmap"],
        is_healthy=is_healthy
    )
    weather_data = fetch_live_weather(district)
    progression_data = evaluate_progression_warning(
        disease_key=best_class,
        severity_level=severity_data["level"],
        humidity=weather_data["humidity_percent"],
        temp_c=weather_data["temperature_c"]
    )
    treatment_data = get_treatment_for_disease(best_class)

    from PIL import Image as PILImage
    heatmap_uint8 = (np.clip(result["heatmap"], 0, 1) * 255).astype(np.uint8)
    colored_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    colored_heatmap = cv2.cvtColor(colored_heatmap, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(np.asarray(image.convert("RGB")), 0.5, colored_heatmap, 0.5, 0)
    overlay_pil = PILImage.fromarray(overlay)

    detection_res = {
        "class_key": best_class,
        "confidence_percent": round(result["confidence"] * 100, 2)
    }

    pdf_bytes = generate_pdf_report(
        crop=plant,
        detection_res=detection_res,
        treatment_info=treatment_data,
        weather_info=weather_data,
        progression_info=progression_data,
        severity_res=severity_data,
        original_img=image,
        gradcam_img=overlay_pil,
        farmer_name=farmer_name,
        taluka_district=weather_data["district"]
    )

    clean_filename = f"AgriSense_Diagnostic_Report_{plant}_{disease}.pdf".replace(" ", "_")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{clean_filename}"'}
    )


# =========================================
# Additional Agronomy & Regional Endpoints
# =========================================




# =========================================
# Tank-Mix Compatibility Endpoints
# =========================================

class CompatibilityRequest(BaseModel):
    chem1: str
    chem2: str


@app.get("/compatibility-chemicals")
async def list_compatibility_chemicals():
    """Returns database of common agricultural chemicals and tonics."""
    return {"chemicals": CHEMICAL_DATABASE}


@app.post("/check-compatibility")
async def check_compatibility_endpoint(req: CompatibilityRequest):
    """Evaluates chemical antagonism, curdling, and leaf burning risks."""
    return check_tank_mix_compatibility(req.chem1, req.chem2)


# =========================================
# 7-Day Epidemic Forecast Endpoint
# =========================================

@app.get("/forecast")
async def get_forecast_endpoint(
    district: str = "Pune (पुणे)",
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    """Fetches 7-day weather predictions and fungal epidemic risk alerts for district or GPS coords."""
    return fetch_7day_epidemic_forecast(district, lat=lat, lon=lon)


# =========================================
# Krishi Seva Kendra Directory Endpoint
# =========================================

@app.get("/krishi-kendras")
async def get_krishi_kendras_endpoint(district: str = "Pune (पुणे)"):
    """Returns verified dealers and standard CIB&RC pricing benchmarks."""
    return get_krishi_kendras_for_district(district)


# =========================================
# Crop Disease Recovery Tracker Endpoint
# =========================================

@app.post("/compare-recovery")
async def compare_recovery_endpoint(
    before_file: UploadFile = File(...),
    after_file: UploadFile = File(...),
    crop: str = Form("Tomato"),
    disease: str = Form("Early Blight")
):
    """Compares Before Spray vs After Spray leaf images to measure recovery %."""
    before_img = await validate_image(before_file)
    after_img = await validate_image(after_file)
    return compare_leaf_recovery(before_img, after_img, crop, disease)


# =========================================
# PMFBY Crop Insurance Damage Certificate
# =========================================

@app.post("/download-pmfby-certificate")
async def download_pmfby_certificate_endpoint(
    file: UploadFile = File(...),
    farmer_name: str = Form("Ramesh Patil"),
    district: str = Form("Pune (पुणे)"),
    farm_size: str = Form("2.5 Acres (100 Gunthas)"),
):
    """Generates official PMFBY Crop Insurance Loss Assessment Certificate PDF."""
    image = await validate_image(file)
    is_leaf, ood_type, ood_message = validate_plant_leaf(image)
    if not is_leaf:
        raise HTTPException(status_code=400, detail=ood_message)

    result = gradcam_service.analyze(image)
    best_class = result["class"]
    plant, disease, _ = get_display_information(best_class)
    is_healthy = disease.strip().lower() == "healthy"

    severity_data = estimate_severity(image=image, heatmap=result["heatmap"], is_healthy=is_healthy)

    from PIL import Image as PILImage
    heatmap_uint8 = (np.clip(result["heatmap"], 0, 1) * 255).astype(np.uint8)
    colored_heatmap = cv2.applyColorMap(heatmap_uint8, cv2.COLORMAP_JET)
    colored_heatmap = cv2.cvtColor(colored_heatmap, cv2.COLOR_BGR2RGB)
    overlay = cv2.addWeighted(np.asarray(image.convert("RGB")), 0.5, colored_heatmap, 0.5, 0)
    overlay_pil = PILImage.fromarray(overlay)

    pdf_bytes = generate_pmfby_claim_certificate(
        farmer_name=farmer_name,
        crop=plant,
        disease=disease,
        severity_pct=severity_data["affected_percentage"],
        confidence_str=f"{result['confidence'] * 100:.1f}%",
        district=district,
        farm_size_str=farm_size,
        original_img=image,
        gradcam_img=overlay_pil
    )

    clean_filename = f"PMFBY_Claim_Certificate_{plant}_{disease}.pdf".replace(" ", "_")
    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={"Content-Disposition": f'attachment; filename="{clean_filename}"'}
    )
