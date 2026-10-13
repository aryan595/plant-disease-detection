"""
AgriSense - Plant Disease Etiology & Progression Timeline Engine
Generates biological timelines explaining:
1. Past Cause (How the pathogen infected the leaf 3-5 days ago)
2. Current Status (Pathological status today based on severity)
3. Future Forecast (What will happen in 7-10 days if untreated)
"""

from typing import Dict, Any

CROP_DISEASE_ETIOLOGY = {
    "blight": {
        "cause_en": "Airborne spores splashed from soil or adjacent plants during rainfall and germinated under high nighttime leaf wetness (>4 hours).",
        "cause_mr": "मातीतून उडालेले पाण्याचे शिंतोडे आणि हवेतील बुरशीचे बीजाणू रात्रीच्या जास्त ओलाव्यामुळे पानात शिरले.",
        "pathology_en": "Fungal hyphae are actively expanding through intercellular leaf tissue, degrading chlorophyll and causing necrotic lesions.",
        "pathology_mr": "बुरशीचे तंतू पानांच्या पेशींमध्ये वेगाने पसरत असून हरितद्रव्य नष्ट करून काळे डाग तयार करत आहेत.",
        "untreated_en": "Lesions will rapidly merge within 7-10 days, causing severe leaf blighting, premature defoliation, and 35-50% crop yield loss.",
        "untreated_mr": "पुढील ७ ते १० दिवसांत डाग एकमेकांत मिसळतील, पाने जळून गळतील आणि उत्पादनात ३५ ते ५०% नुकसान होईल."
    },
    "mildew": {
        "cause_en": "Microscopic conidia/sporangia carried by morning winds settled onto leaves and multiplied in warm, humid microclimates.",
        "cause_mr": "सकाळच्या वाऱ्यासोबत आलेले सूक्ष्म बुरशीचे बीजाणू पानांवर स्थिरावले आणि उबदार-दमट हवेत झपाट्याने वाढले.",
        "pathology_en": "Dense fungal mycelium is colonizing leaf surfaces, suffocating stomatal respiration and sap-feeding from leaf veins.",
        "pathology_mr": "पानाच्या पृष्ठभागावर बुरशीचे जाळे तयार झाले असून पानाच्या नसांमधील अन्नरस शोषून पानांची ताकद कमी करत आहे.",
        "untreated_en": "Cottony sporulation will engulf fresh shoots and fruit clusters, causing tissue cracking and devastating marketable harvest.",
        "untreated_mr": "बुरशी नवीन फुटवे आणि फळांवर पसरेल, ज्यामुळे फळांना तडे जाऊन संपूर्ण काढणीयोग्य पिकाचे नुकसान होईल."
    },
    "rust": {
        "cause_en": "Urediniospores from previous crop residue or windborne drift germinated during prolonged morning dew and warm temperatures.",
        "cause_mr": "मागील पिकाचे अवशेष किंवा वाऱ्यातून आलेले तांबेरा बीजाणू सकाळच्या दवबिंदूंमुळे पानांवर रुजले.",
        "pathology_en": "Pustules erupt through the leaf cuticle, rupturing epidermal cells and releasing millions of powdery secondary spores.",
        "pathology_mr": "पानांच्या त्वचेतून तांबूस रंगाचे फोड फुटले असून लाखो पावडरसारखे बीजाणू हवेत उडण्यासाठी तयार आहेत.",
        "untreated_en": "Widespread pustule coverage will dry out the foliage completely, causing early leaf burn and drastic grain/fruit shriveling.",
        "untreated_mr": "संपूर्ण पानावर तांबेरा पसरून पाने करपून वाळतील आणि दाणे/फळे बारीक राहून उत्पादनात मोठी घट होईल."
    },
    "spot": {
        "cause_en": "Bacterial or fungal inoculum entered through natural leaf stomata or micro-wounds created by wind friction and insects.",
        "cause_mr": "पानावरील सूक्ष्म छिद्रांमधून किंवा किडींनी केलेल्या जखमांमधून बुरशी/जिवाणू पानाच्या आत शिरले.",
        "pathology_en": "Localized enzymatic destruction has formed water-soaked lesions with characteristic chlorotic yellow halos.",
        "pathology_mr": "विशिष्ट भागातील पेशी नष्ट झाल्याने पिवळ्या कडा असलेले डाग पानावरील अन्न निर्मिती थांबवत आहेत.",
        "untreated_en": "Spots will coalesce, shot-holing the leaf blades and dropping foliage, leaving developing fruit exposed to sunscald.",
        "untreated_mr": "डागांमुळे पानांना छिद्रे पडून पानगळ होईल, ज्यामुळे फळांवर थेट ऊन पडून फळे खराब होतील."
    },
    "healthy": {
        "cause_en": "Excellent cultural sanitation, balanced fertigation, and optimal natural canopy aeration.",
        "cause_mr": "उत्कृष्ट स्वच्छता, संतुलित खत व्यवस्थापन आणि झाडांमध्ये योग्य सूर्यप्रकाश व हवा.",
        "pathology_en": "Vibrant chloroplast activity with strong cell wall integrity; foliage is free of parasitic pathogens.",
        "pathology_mr": "पाने पूर्णपणे निरोगी असून अन्न निर्मितीची प्रक्रिया अत्यंत जोमाने सुरू आहे.",
        "untreated_en": "Plant will continue standard vegetative and reproductive development. Maintain routine preventive scouting.",
        "untreated_mr": "पीक जोमाने वाढत राहील. नियमित पाहणी सुरू ठेवा आणि रोग प्रतिबंधात्मक काळजी घ्या."
    }
}


def generate_disease_timeline(
    plant: str,
    disease: str,
    severity_level: str,
    affected_percentage: float
) -> Dict[str, Any]:
    """
    Build an explainable 3-stage temporal disease progression timeline.
    """
    d_lower = disease.lower()
    
    if "healthy" in d_lower:
        archetype = "healthy"
    elif "blight" in d_lower or "rot" in d_lower:
        archetype = "blight"
    elif "mildew" in d_lower:
        archetype = "mildew"
    elif "rust" in d_lower:
        archetype = "rust"
    elif "spot" in d_lower or "scab" in d_lower:
        archetype = "spot"
    else:
        archetype = "blight"

    data = CROP_DISEASE_ETIOLOGY[archetype]
    is_healthy = archetype == "healthy"

    return {
        "archetype": archetype,
        "is_healthy": is_healthy,
        "stage_1_cause": {
            "title_en": "Stage 1: Infection & Pathogen Entry (Past 3–5 Days)",
            "title_mr": "टप्पा १: संसर्ग आणि बुरशीचा शिरकाव (मागील ३ ते ५ दिवस)",
            "description_en": data["cause_en"],
            "description_mr": data["cause_mr"],
            "badge_en": "Past Infection",
            "badge_mr": "मागील संसर्ग",
            "icon": "🌱"
        },
        "stage_2_current": {
            "title_en": f"Stage 2: Current Pathology Today ({severity_level})",
            "title_mr": f"टप्पा २: आजची रोगाची स्थिती ({severity_level})",
            "description_en": (
                f"Active visible symptoms currently encompass {affected_percentage}% of the leaf blade. "
                f"{data['pathology_en']}"
            ),
            "description_mr": (
                f"पानाच्या सुमारे {affected_percentage}% भागावर लक्षणे दिसत आहेत. "
                f"{data['pathology_mr']}"
            ),
            "badge_en": f"{affected_percentage}% Area Infected",
            "badge_mr": f"{affected_percentage}% भाग बाधित",
            "icon": "🔎"
        },
        "stage_3_future": {
            "title_en": "Stage 3: Forecast If Untreated (Next 7–10 Days)",
            "title_mr": "टप्पा ३: उपचार न केल्यास पुढील धोका (पुढील ७ ते १० दिवस)",
            "description_en": data["untreated_en"],
            "description_mr": data["untreated_mr"],
            "badge_en": "Projected Outcome",
            "badge_mr": "संभाव्य नुकसान",
            "icon": "⚠️"
        },
        "curative_window": {
            "urgency_en": "High Action Window (Next 24 to 48 Hours)" if not is_healthy else "Routine Care",
            "urgency_mr": "तातडीने फवारणी करा (२४ ते ४८ तास)" if not is_healthy else "नियमित काळजी",
            "action_en": (
                f"Apply prescribed fungicide spray within 24-48 hours to prevent spores spreading to adjacent leaves."
                if not is_healthy else "Maintain optimal drip fertigation and scout weekly."
            ),
            "action_mr": (
                f"रोगाचा पुढील पानांवर प्रसार रोखण्यासाठी २४ ते ४८ तासांच्या आत योग्य मात्रेनुसार फवारणी करा."
                if not is_healthy else "नियमित पाहणी करा आणि संतुलित खतांचा वापर करा."
            )
        }
    }
