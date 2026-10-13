import json
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
INFO_FILE = PROJECT_ROOT / "app" / "disease_info.json"
TARGET_FILE = PROJECT_ROOT / "frontend" / "src" / "diseaseTranslations.js"

with open(INFO_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

js_content = f"""// Auto-generated comprehensive Marathi translations for all 55 disease classes
// Provides complete localized symptoms, management, prevention, plant names, and descriptions

export const DISEASE_TRANSLATIONS_MR = {json.dumps(data, indent=2, ensure_ascii=False)};

// Plant name translations (English -> Marathi)
export const PLANT_NAMES_MR = {{
  "Apple": "सफरचंद",
  "Blueberry": "ब्ल्यूबेरी",
  "Cherry": "चेरी",
  "Cherry (including sour)": "चेरी",
  "Corn": "मका",
  "Corn (maize)": "मका",
  "Grape": "द्राक्ष",
  "Orange": "संत्रा",
  "Peach": "पीच",
  "Pepper, bell": "ढोबळी मिरची",
  "Potato": "बटाटा",
  "Raspberry": "रास्पबेरी",
  "Soybean": "सोयाबीन",
  "Squash": "भोपळा",
  "Strawberry": "स्ट्रॉबेरी",
  "Tomato": "टोमॅटो",
  "Cotton": "कापूस",
  "Sugarcane": "ऊस",
}};

// Helper: Normalize key for searching
function normalize(str) {{
  return (str || "").toLowerCase().replace(/[^a-z0-9]/g, "");
}}

// Find entry in database
export function findDiseaseEntry(diseaseName, plantName = null, classKey = null) {{
  if (classKey && DISEASE_TRANSLATIONS_MR[classKey]) {{
    return DISEASE_TRANSLATIONS_MR[classKey];
  }}

  // Direct match by class key pattern
  if (plantName && diseaseName) {{
    const cleanPlant = plantName.replace(/[(),]/g, "").replace(/ +/g, "_");
    const cleanDisease = diseaseName.replace(/[(),]/g, "").replace(/ +/g, "_");
    const combinedKey = `${{cleanPlant}}___${{cleanDisease}}`;
    if (DISEASE_TRANSLATIONS_MR[combinedKey]) {{
      return DISEASE_TRANSLATIONS_MR[combinedKey];
    }}
  }}

  // Exact or fuzzy match
  const targetDisease = normalize(diseaseName);
  const targetPlant = plantName ? normalize(plantName) : null;

  for (const [key, entry] of Object.entries(DISEASE_TRANSLATIONS_MR)) {{
    const entryDisease = normalize(entry.disease);
    const entryPlant = normalize(entry.plant);

    if (targetPlant) {{
      if (entryPlant === targetPlant && entryDisease === targetDisease) {{
        return entry;
      }}
    }} else {{
      if (entryDisease === targetDisease) {{
        return entry;
      }}
    }}
  }}

  // Partial match fallback
  for (const [key, entry] of Object.entries(DISEASE_TRANSLATIONS_MR)) {{
    const entryDisease = normalize(entry.disease);
    if (targetDisease && (targetDisease.includes(entryDisease) || entryDisease.includes(targetDisease))) {{
      return entry;
    }}
  }}

  return null;
}}

export function getLocalizedPlant(plantName, lang = "en") {{
  if (lang !== "mr") return plantName;
  if (!plantName) return "";
  return PLANT_NAMES_MR[plantName] || plantName;
}}

export function getLocalizedDisease(diseaseName, lang = "en", classKey = null, plantName = null) {{
  if (lang !== "mr") return diseaseName;
  if (!diseaseName) return "";
  if (diseaseName.toLowerCase() === "healthy") return "निरोगी";
  const entry = findDiseaseEntry(diseaseName, plantName, classKey);
  return entry?.disease_mr || diseaseName;
}}

export function getLocalizedDescription(diseaseName, lang = "en", defaultDesc = "", classKey = null, plantName = null) {{
  if (lang !== "mr") return defaultDesc;
  const entry = findDiseaseEntry(diseaseName, plantName, classKey);
  return entry?.description_mr || defaultDesc;
}}

export function getLocalizedSymptoms(diseaseName, lang = "en", defaultSymptoms = [], classKey = null, plantName = null) {{
  if (lang !== "mr") return defaultSymptoms;
  const entry = findDiseaseEntry(diseaseName, plantName, classKey);
  if (entry?.symptoms_mr && entry.symptoms_mr.length > 0) {{
    return entry.symptoms_mr;
  }}
  return defaultSymptoms;
}}

export function getLocalizedManagement(diseaseName, lang = "en", defaultManagement = [], classKey = null, plantName = null) {{
  if (lang !== "mr") return defaultManagement;
  const entry = findDiseaseEntry(diseaseName, plantName, classKey);
  if (entry?.management_mr && entry.management_mr.length > 0) {{
    return entry.management_mr;
  }}
  return defaultManagement;
}}

export function getLocalizedPrevention(diseaseName, lang = "en", defaultPrevention = [], classKey = null, plantName = null) {{
  if (lang !== "mr") return defaultPrevention;
  const entry = findDiseaseEntry(diseaseName, plantName, classKey);
  if (entry?.prevention_mr && entry.prevention_mr.length > 0) {{
    return entry.prevention_mr;
  }}
  return defaultPrevention;
}}
"""

with open(TARGET_FILE, "w", encoding="utf-8") as f:
    f.write(js_content)

print(f"Generated {TARGET_FILE} with size {len(js_content)} bytes")
