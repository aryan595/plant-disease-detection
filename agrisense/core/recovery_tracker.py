"""
AgriSense - Crop Disease Recovery Tracker
Compares "Before Spray (Day 0)" and "After Spray (Day 4-7)" leaf photos
to quantify disease suppression, lesion drying, and treatment efficacy.
"""

from typing import Dict, Any
from PIL import Image
from agrisense.core.severity import estimate_severity


def compare_leaf_recovery(
    before_image: Image.Image,
    after_image: Image.Image,
    crop_name: str,
    disease_name: str
) -> Dict[str, Any]:
    """
    Computes disease severity reduction between before and after leaf images.
    """
    # Analyze severity on both images
    before_sev = estimate_severity(before_image, is_healthy=False)
    after_sev = estimate_severity(after_image, is_healthy=False)

    p_before = before_sev["affected_percentage"]
    p_after = after_sev["affected_percentage"]

    # Calculate difference
    diff = p_before - p_after
    if p_before > 0:
        improvement_pct = round((diff / p_before) * 100, 1)
    else:
        improvement_pct = 0.0

    if diff > 3.0:
        status = "EXCELLENT_RECOVERY"
        badge = "🟢 रोग नियंत्रणात आला आहे (Effective Suppression)"
        status_color = "#16a34a"
        message_mr = f"अभिनंदन! बुरशीचे डाग सुकले असून रोगाचा प्रादुर्भाव {abs(improvement_pct)}% ने कमी झाला आहे. नवीन फूट निरोगी आहे."
        message_en = f"Treatment Successful! Lesions have dried out and affected surface area reduced by {abs(improvement_pct)}%. Fungal spread halted."
        next_step = "Repeat booster spray of organic Trichoderma or bio-stimulant after 7 days to maintain leaf vigor."
    elif diff >= -2.0:
        status = "STABILIZED"
        badge = "🟡 रोग वाढ थांबली आहे (Disease Arrested)"
        status_color = "#f59e0b"
        message_mr = f"रोगाची वाढ जागेवरच थांबली आहे. डागांचा विस्तार झालेला नाही."
        message_en = f"Infection has stabilized. The spread to adjacent leaf veins has been arrested."
        next_step = "Inspect underside of new young leaves. If humidity stays above 80%, apply second protective spray."
    else:
        status = "PROGRESSING"
        badge = "🔴 रोगाचा प्रादुर्भाव वाढला आहे (Infection Spread)"
        status_color = "#ef4444"
        message_mr = f"रोगाचा प्रादुर्भाव वाढलेला दिसत आहे. औषधाची प्रतिकारशक्ती (Resistance) आली असण्याची शक्यता आहे."
        message_en = f"Infection has spread further. The pathogen may be resistant to the applied chemical group."
        next_step = "Switch immediately to a different chemical group with systemic vascular action."

    return {
        "crop": crop_name,
        "disease": disease_name,
        "before_severity_pct": p_before,
        "after_severity_pct": p_after,
        "improvement_pct": improvement_pct,
        "status": status,
        "status_badge": badge,
        "badge_color": status_color,
        "message_mr": message_mr,
        "message_en": message_en,
        "actionable_next_step": next_step
    }
