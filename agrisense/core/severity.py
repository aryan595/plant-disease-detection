"""
AgriSense - Severity Estimation Engine
Algorithm: Computer Vision HSV Color Deconvolution + Grad-CAM Saliency Fusion
Categorizes disease damage into: Healthy / Mild (<15%) / Moderate (15-35%) / Severe (>=35%)
"""

from typing import Dict, Tuple, Optional

import cv2
import numpy as np
from PIL import Image


def estimate_severity(
    image: Image.Image,
    heatmap: Optional[np.ndarray] = None,
    is_healthy: bool = False
) -> Dict:
    """
    Estimates the percentage of leaf surface infected by combining HSV color segmentation
    with optional Grad-CAM spatial activation weights.
    """
    if is_healthy:
        return {
            "level": "Healthy",
            "level_mr": "निरोगी (कोणताही संसर्ग नाही)",
            "affected_percentage": 0.0,
            "badge_color": "#28a745",
            "description_en": "No significant lesion progression observed on the leaf surface.",
            "description_mr": "पानावर कोणत्याही रोगाचे डाग किंवा नुकसान आढळलेले नाही.",
            "annotated_mask_pil": image
        }

    image_rgb = image.convert("RGB")
    img_np = np.array(image_rgb)
    hsv = cv2.cvtColor(img_np, cv2.COLOR_RGB2HSV)

    # 1. Segment Total Leaf Tissue from background
    h_channel = hsv[:, :, 0]
    s_channel = hsv[:, :, 1]
    v_channel = hsv[:, :, 2]

    # Leaf pixels generally have moderate to high saturation and sufficient brightness
    leaf_mask = (s_channel > 25) & (v_channel > 25) & (v_channel < 245)
    total_leaf_pixels = np.sum(leaf_mask)

    if total_leaf_pixels < 500:
        leaf_mask = np.ones((img_np.shape[0], img_np.shape[1]), dtype=bool)
        total_leaf_pixels = leaf_mask.size

    # 2. Segment Healthy Green foliage: Hue between 35 and 88 in OpenCV (scale 0-180)
    healthy_green_mask = leaf_mask & (h_channel >= 35) & (h_channel <= 88) & (s_channel >= 40)

    # 3. Identify Color Anomaly / Necrotic Lesion Tissue
    color_lesion_mask = leaf_mask & (~healthy_green_mask)

    # 4. Integrate Grad-CAM Saliency (> 0.40 attention threshold within leaf tissue)
    if heatmap is not None:
        cam_attention_mask = (heatmap > 0.40) & leaf_mask
    else:
        cam_attention_mask = color_lesion_mask

    # 5. Combined Diseased Area: Color anomaly verified by CNN attention or strong focal lesions
    if heatmap is not None:
        combined_diseased_mask = (color_lesion_mask & (heatmap > 0.20)) | (cam_attention_mask & (color_lesion_mask | (v_channel < 100)))
    else:
        combined_diseased_mask = color_lesion_mask

    diseased_pixels = np.sum(combined_diseased_mask)
    affected_percentage = float((diseased_pixels / total_leaf_pixels) * 100.0)
    affected_percentage = max(0.5, min(95.0, round(affected_percentage, 1)))

    # Determine Severity Level
    if affected_percentage < 15.0:
        level = "Mild"
        level_mr = "कमी / सौम्य प्रादुर्भाव (Mild)"
        badge_color = "#28a745"  # Green / Yellow-Green
        desc_en = (
            f"Early stage localized infection ({affected_percentage}% leaf area). "
            "Timely intervention will prevent canopy colonization."
        )
        desc_mr = (
            f"सुरुवातीचा सौम्य प्रादुर्भाव ({affected_percentage}% पानावरील भाग बाधित). "
            "वेळेत उपाययोजना केल्यास रोग सहज आटोक्यात येईल."
        )
    elif 15.0 <= affected_percentage < 35.0:
        level = "Moderate"
        level_mr = "मध्यम प्रादुर्भाव (Moderate)"
        badge_color = "#fd7e14"  # Orange
        desc_en = (
            f"Established infection spreading across leaf venation ({affected_percentage}% affected). "
            "Systemic or bio-fungicide spray recommended to arrest secondary sporulation."
        )
        desc_mr = (
            f"रोगाचा मध्यम प्रसार झाला आहे ({affected_percentage}% पानावरील भाग बाधित). "
            "बुरशीचे बीजाणू रोखण्यासाठी त्वरित फवारणी आवश्यक आहे."
        )
    else:
        level = "Severe"
        level_mr = "तीव्र / गंभीर प्रादुर्भाव (Severe)"
        badge_color = "#dc3545"  # Red
        desc_en = (
            f"Extensive tissue necrosis across {affected_percentage}% of leaf area. "
            "High risk of defoliation and spore transmission to neighboring vines/shoots."
        )
        desc_mr = (
            f"रोगाचा तीव्र प्रादुर्भाव झाला आहे ({affected_percentage}% पानावरील भाग नष्ट). "
            "पानगळ होण्याची आणि लगतच्या पिकात वेगाने पसरण्याची दाट शक्यता."
        )

    # Generate an annotated visual mask (highlighting diseased lesions in semi-transparent red)
    annotated = img_np.copy()
    annotated[combined_diseased_mask] = (
        0.5 * annotated[combined_diseased_mask] + 0.5 * np.array([255, 50, 50])
    ).astype(np.uint8)

    annotated_pil = Image.fromarray(annotated)

    return {
        "level": level,
        "level_mr": level_mr,
        "affected_percentage": affected_percentage,
        "badge_color": badge_color,
        "description_en": desc_en,
        "description_mr": desc_mr,
        "annotated_mask_pil": annotated_pil
    }
