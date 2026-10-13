"""
AgriSense - Chemical Tank-Mix Compatibility Database
Evaluates agricultural chemical and fertilizer combinations for tank mixing.
Flags antagonism, curdling, neutralization, and phytotoxicity (leaf burn) risks.
"""

from typing import Dict, List, Any

# Common agricultural chemicals & spray tonics used in Maharashtra
CHEMICAL_DATABASE = [
    {"id": "mancozeb", "name": "Mancozeb 75 WP (Dithane M-45)", "category": "Contact Fungicide", "ph": "Neutral"},
    {"id": "metalaxyl", "name": "Metalaxyl + Mancozeb (Ridomil Gold)", "category": "Systemic Fungicide", "ph": "Neutral"},
    {"id": "chlorothalonil", "name": "Chlorothalonil 75 WP (Kavach)", "category": "Broad-spectrum Fungicide", "ph": "Slightly Acidic"},
    {"id": "copper_oxychloride", "name": "Copper Oxychloride 50 WP (Blitox)", "category": "Copper Fungicide", "ph": "Alkaline"},
    {"id": "sulphur", "name": "Wettable Sulphur 80 WDG (Sulfex)", "category": "Inorganic Fungicide/Acaricide", "ph": "Neutral/Acidic"},
    {"id": "hexaconazole", "name": "Hexaconazole 5% SC (Contaf Plus)", "category": "Triazole Fungicide", "ph": "Neutral"},
    {"id": "azoxystrobin", "name": "Azoxystrobin 23% SC (Amistar)", "category": "Strobilurin Fungicide", "ph": "Neutral"},
    {"id": "imidacloprid", "name": "Imidacloprid 17.8% SL (Confidor)", "category": "Systemic Insecticide", "ph": "Neutral"},
    {"id": "chlorpyrifos", "name": "Chlorpyrifos 20% EC", "category": "Organophosphate Insecticide", "ph": "Acidic"},
    {"id": "neem_oil", "name": "Neem Oil 10000 PPM (Azadirachtin)", "category": "Bio-Pesticide", "ph": "Neutral"},
    {"id": "npk_19_19_19", "name": "19:19:19 Water Soluble Fertilizer", "category": "Foliar Fertilizer", "ph": "Slightly Acidic"},
    {"id": "micronutrient_zinc_fe", "name": "Chelated Micronutrients (Zn, Fe, Mn)", "category": "Micronutrient Tonic", "ph": "Neutral"},
    {"id": "boron_20", "name": "Soluble Boron 20%", "category": "Micronutrient", "ph": "Slightly Alkaline"},
    {"id": "spreader_sticker", "name": "Silicon Spreader / Wetting Agent", "category": "Adjuvant", "ph": "Neutral"}
]

# Incompatibility Rules matrix
INCOMPATIBILITY_RULES = [
    {
        "pair": {"copper_oxychloride", "chlorpyrifos"},
        "status": "DANGEROUS",
        "risk_en": "High Risk of Curdling & Rapid Chemical Breakdown",
        "risk_mr": "द्रावण फाटणे (Curdling) व कीटकनाशक निकामी होण्याचा मोठा धोका",
        "detail": "Copper compounds degrade organophosphates like Chlorpyrifos very rapidly in the spray tank due to high alkalinity.",
        "action": "Do NOT mix. Spray Copper Oxychloride separately with at least 3 days gap."
    },
    {
        "pair": {"copper_oxychloride", "npk_19_19_19"},
        "status": "INCOMPATIBLE",
        "risk_en": "Precipitate Formation & Nozzle Clogging",
        "risk_mr": "तळाशी गाळ बसणे व पंपाचे नोझल चोक होण्याचा धोका",
        "detail": "Soluble phosphates in 19:19:19 react with copper ions forming insoluble copper phosphate sludge.",
        "action": "Avoid tank mixing. Apply 19:19:19 as a separate spray."
    },
    {
        "pair": {"sulphur", "neem_oil"},
        "status": "DANGEROUS",
        "risk_en": "Severe Phytotoxicity (Foliage & Leaf Burning)",
        "risk_mr": "पाने जळणे (Phytotoxicity) व करपण्याचा तीव्र धोका",
        "detail": "Mixing sulphur with oils (Neem or mineral oil) creates toxic heat reaction under direct sunlight causing acute leaf scorch.",
        "action": "Strictly maintain at least 14 days interval between Sulphur and oil-based sprays."
    },
    {
        "pair": {"boron_20", "copper_oxychloride"},
        "status": "CAUTION",
        "risk_en": "Chemical Neutralization Risk",
        "risk_mr": "दोन्ही घटकांची कार्यक्षमता कमी होण्याचा धोका",
        "detail": "Alkaline pH shift reduces copper fungicide adherence and boron uptake.",
        "action": "Perform a jar test (काचेच्या बाटलीत चाचणी) in 1L water before pouring into the main drum."
    },
    {
        "pair": {"mancozeb", "chlorothalonil"},
        "status": "REDUNDANT",
        "risk_en": "Redundant Contact Modes of Action",
        "risk_mr": "दोन्ही स्पर्शजन्य बुरशीनाशके असल्याने दुहेरी खर्च",
        "detail": "Both are multi-site contact protectants. Combining them increases cost without providing systemic vascular protection.",
        "action": "Pair one contact fungicide (Mancozeb) with a systemic partner (Metalaxyl or Hexaconazole) instead."
    }
]

def check_tank_mix_compatibility(chem1_id: str, chem2_id: str) -> Dict[str, Any]:
    """
    Checks compatibility between two chemicals.
    Returns status: 'COMPATIBLE', 'CAUTION', 'INCOMPATIBLE', or 'DANGEROUS'.
    """
    c1 = chem1_id.lower().strip()
    c2 = chem2_id.lower().strip()
    
    if c1 == c2:
        return {
            "status": "SAME_CHEMICAL",
            "is_safe": True,
            "badge_color": "#3b82f6",
            "title_en": "Same Product Selected",
            "title_mr": "एकच उत्पादन निवडले आहे",
            "explanation_en": "You have selected the same chemical twice.",
            "explanation_mr": "तुम्ही एकच औषध दोनदा निवडले आहे.",
            "recommendation": "Select two different products to check compatibility."
        }

    pair_set = {c1, c2}
    for rule in INCOMPATIBILITY_RULES:
        if rule["pair"] == pair_set:
            status = rule["status"]
            color = "#ef4444" if status in ["DANGEROUS", "INCOMPATIBLE"] else "#f59e0b"
            return {
                "status": status,
                "is_safe": False,
                "badge_color": color,
                "title_en": rule["risk_en"],
                "title_mr": rule["risk_mr"],
                "explanation_en": rule["detail"],
                "explanation_mr": rule["detail"],
                "recommendation": rule["action"]
            }

    # Default: Compatible with standard jar test reminder
    return {
        "status": "COMPATIBLE",
        "is_safe": True,
        "badge_color": "#16a34a",
        "title_en": "✓ Safe & Compatible for Tank Mix",
        "title_mr": "✓ एकत्र फवारणीसाठी सुरक्षित (सुसंगत)",
        "explanation_en": "No known negative chemical antagonism between these two products. Always dissolve wettable powders (WP/WDG) first, then liquids (SC/SL/EC), and add adjuvant/spreader last.",
        "explanation_mr": "या दोन घटकांमध्ये रासायनिक विरोध नाही. प्रथम पावडर (WP) विरघळवा, नंतर लिक्विड (SC/EC) घाला व शेवटी स्टिकर टाका.",
        "recommendation": "Safe to tank mix in 15L / 20L / 200L spray tanks. Ensure continuous agitation."
    }
