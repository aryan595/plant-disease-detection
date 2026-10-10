
import json
import shutil
from pathlib import Path


# =========================================
# Paths
# =========================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

INFO_FILE = PROJECT_ROOT / "app" / "disease_info.json"

CHECKPOINT_FILE = (
    PROJECT_ROOT
    / "models"
    / "efficientnet_b0_combined_55class.pth"
)

BACKUP_FILE = (
    PROJECT_ROOT
    / "app"
    / "disease_info.backup.json"
)


# =========================================
# New class information
# =========================================

NEW_DISEASE_INFO = {

    # -------------------------------------
    # Cotton
    # -------------------------------------

    "Cotton___Alternaria_leaf_spot": {
        "plant": "Cotton",
        "disease": "Alternaria Leaf Spot",
        "description": (
            "A leaf condition associated with Alternaria fungi. "
            "Correct identification should be confirmed using "
            "symptoms and, when needed, expert assessment."
        ),
        "symptoms": [
            "Brown or dark leaf spots may develop.",
            "Spots can enlarge and develop darker margins.",
            "Severe damage may contribute to leaf deterioration."
        ],
        "management": [
            "Inspect affected plants and monitor symptom progression.",
            "Remove heavily affected plant material where appropriate.",
            "Seek local agricultural advice before selecting a treatment."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain field sanitation.",
            "Monitor plants regularly, especially in favorable disease conditions."
        ]
    },

    "Cotton___Bacterial_blight": {
        "plant": "Cotton",
        "disease": "Bacterial Blight",
        "description": (
            "A bacterial disease of cotton that may affect leaves, "
            "stems, and other plant tissues."
        ),
        "symptoms": [
            "Angular or dark water-soaked leaf lesions may appear.",
            "Lesions may darken as symptoms develop.",
            "Affected plant tissues may deteriorate in severe cases."
        ],
        "management": [
            "Inspect plants and confirm the suspected disease.",
            "Follow locally recommended sanitation and crop-management practices.",
            "Consult an agricultural specialist about suitable management options."
        ],
        "prevention": [
            "Use certified or otherwise healthy seed.",
            "Follow locally recommended resistant-variety guidance.",
            "Avoid moving potentially infected plant material between fields."
        ]
    },

    "Cotton___Fusarium_wilt": {
        "plant": "Cotton",
        "disease": "Fusarium Wilt",
        "description": (
            "A fungal wilt disease associated with Fusarium species "
            "that can interfere with water movement through the plant."
        ),
        "symptoms": [
            "Yellowing and wilting may occur.",
            "Leaves may become discolored or drop.",
            "Internal vascular discoloration may occur in affected stems."
        ],
        "management": [
            "Confirm the cause of wilting before treatment decisions.",
            "Seek advice on locally appropriate resistant varieties.",
            "Manage affected fields according to local agricultural guidance."
        ],
        "prevention": [
            "Use healthy seed and planting material.",
            "Maintain appropriate crop rotation where effective.",
            "Clean equipment when moving between potentially affected fields."
        ]
    },

    "Cotton___Verticillium_wilt": {
        "plant": "Cotton",
        "disease": "Verticillium Wilt",
        "description": (
            "A soil-associated fungal wilt disease that can affect "
            "water transport and plant vigor."
        ),
        "symptoms": [
            "Yellowing may develop between leaf veins.",
            "Leaves may wilt or show uneven discoloration.",
            "Plant growth may be reduced."
        ],
        "management": [
            "Obtain confirmation because other problems can cause similar symptoms.",
            "Check local guidance on suitable varieties and crop management.",
            "Avoid moving contaminated soil or plant debris between fields."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Consider locally recommended crop rotation.",
            "Maintain field and equipment sanitation."
        ]
    },

    "Cotton___healthy": {
        "plant": "Cotton",
        "disease": "Healthy",
        "description": (
            "The model classified this image as a healthy cotton leaf. "
            "This prediction does not rule out every possible disease "
            "or plant health problem."
        ),
        "symptoms": [
            "No major disease symptoms were identified by the model.",
            "Inspect leaves for discoloration, spots, wilting, or distortion."
        ],
        "management": [
            "Continue routine crop scouting.",
            "Provide suitable water and nutrition based on crop needs."
        ],
        "prevention": [
            "Maintain field sanitation.",
            "Monitor plants regularly.",
            "Use recommended crop-management practices."
        ]
    },

    # -------------------------------------
    # Grape
    # -------------------------------------

    "Grape___Bacterial_leaf_spot": {
        "plant": "Grape",
        "disease": "Bacterial Leaf Spot",
        "description": (
            "A possible bacterial leaf condition. Visual symptoms can "
            "overlap with fungal diseases and other sources of leaf damage."
        ),
        "symptoms": [
            "Dark or water-soaked spots may appear on leaves.",
            "Lesions may enlarge or develop surrounding discoloration.",
            "Affected foliage may deteriorate in severe cases."
        ],
        "management": [
            "Confirm the suspected cause before applying treatments.",
            "Remove affected material where locally recommended.",
            "Seek advice from a grape-production specialist."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain vineyard sanitation.",
            "Avoid unnecessary leaf wetness and monitor disease symptoms."
        ]
    },

    "Grape___Downy_mildew": {
        "plant": "Grape",
        "disease": "Downy Mildew",
        "description": (
            "A grape disease caused by the oomycete Plasmopara viticola. "
            "It can affect leaves and other green tissues."
        ),
        "symptoms": [
            "Yellowish or oily-looking areas may form on leaf surfaces.",
            "Whitish growth may appear on the undersides of leaves in suitable conditions.",
            "Affected leaves may brown or fall prematurely."
        ],
        "management": [
            "Inspect both leaf surfaces and monitor weather conditions.",
            "Use locally recommended vineyard-management practices.",
            "Consult regional guidance before choosing any disease-control treatment."
        ],
        "prevention": [
            "Maintain good canopy airflow.",
            "Monitor during humid and wet weather.",
            "Remove infected plant material where appropriate."
        ]
    },

    "Grape___Powdery_mildew": {
        "plant": "Grape",
        "disease": "Powdery Mildew",
        "description": (
            "A fungal disease associated with Erysiphe necator that "
            "can affect grape leaves, shoots, and fruit."
        ),
        "symptoms": [
            "Pale powdery growth may appear on leaf surfaces.",
            "Affected tissue may become distorted or discolored.",
            "Severe infections may affect fruit quality."
        ],
        "management": [
            "Monitor leaves and developing fruit.",
            "Use regionally recommended vineyard disease-management practices.",
            "Obtain local advice before applying disease-control products."
        ],
        "prevention": [
            "Maintain an open canopy where appropriate.",
            "Scout regularly during susceptible growth stages.",
            "Remove affected plant material when recommended."
        ]
    },

    # -------------------------------------
    # Soybean
    # -------------------------------------

    "Soybean___Bacterial_blight": {
        "plant": "Soybean",
        "disease": "Bacterial Blight",
        "description": (
            "A bacterial soybean disease commonly associated with "
            "Pseudomonas savastanoi pv. glycinea."
        ),
        "symptoms": [
            "Small water-soaked spots may form on leaves.",
            "Lesions may become brown and angular.",
            "Damaged tissue may dry or tear."
        ],
        "management": [
            "Confirm the disease rather than relying on appearance alone.",
            "Follow locally recommended crop-management practices.",
            "Consult agricultural guidance if symptoms spread."
        ],
        "prevention": [
            "Use healthy seed where available.",
            "Maintain field sanitation.",
            "Avoid unnecessary movement of potentially contaminated plant material."
        ]
    },

    "Soybean___Cercospora_leaf_blight": {
        "plant": "Soybean",
        "disease": "Cercospora Leaf Blight",
        "description": (
            "A fungal disease associated with Cercospora species that "
            "may cause leaf discoloration and reduced canopy health."
        ),
        "symptoms": [
            "Leaves may show purple, reddish, or bronze discoloration.",
            "Leaf surfaces may appear bronzed or blotchy.",
            "Symptoms can become more noticeable later in the growing season."
        ],
        "management": [
            "Monitor disease development through the growing season.",
            "Consult local recommendations on resistant varieties and management.",
            "Confirm diagnosis before deciding on treatment."
        ],
        "prevention": [
            "Use locally recommended varieties.",
            "Maintain crop residue management practices appropriate to the region.",
            "Scout fields regularly."
        ]
    },

    "Soybean___Rust": {
        "plant": "Soybean",
        "disease": "Soybean Rust",
        "description": (
            "A fungal disease caused by Phakopsora pachyrhizi that can "
            "damage soybean foliage and reduce plant productivity."
        ),
        "symptoms": [
            "Small tan or reddish-brown lesions may develop.",
            "Tiny raised pustules may occur, particularly on leaf undersides.",
            "Leaves may yellow and drop prematurely."
        ],
        "management": [
            "Confirm suspected rust with an agricultural specialist.",
            "Monitor regional disease alerts and local guidance.",
            "Follow locally approved management recommendations."
        ],
        "prevention": [
            "Scout fields regularly during susceptible growth stages.",
            "Monitor regional disease reports.",
            "Follow recommended crop and volunteer-plant management."
        ]
    },

    "Soybean___Sudden_death_syndrome": {
        "plant": "Soybean",
        "disease": "Sudden Death Syndrome",
        "description": (
            "A soybean disease commonly associated with Fusarium virguliforme "
            "and related Fusarium species, depending on the region."
        ),
        "symptoms": [
            "Interveinal yellowing may develop on leaves.",
            "Yellow areas may turn brown while veins remain greener.",
            "Root damage may occur, and foliage symptoms can appear above ground."
        ],
        "management": [
            "Confirm the diagnosis because several problems produce similar symptoms.",
            "Consult local recommendations for variety selection and field management.",
            "Review drainage and soil conditions where relevant."
        ],
        "prevention": [
            "Use healthy seed and locally recommended varieties.",
            "Manage soil and drainage conditions appropriately.",
            "Scout affected fields and document symptom patterns."
        ]
    },

    # -------------------------------------
    # Sugarcane
    # -------------------------------------

    "Sugarcane___Mosaic": {
        "plant": "Sugarcane",
        "disease": "Mosaic",
        "description": (
            "A viral disease category associated with mosaic patterns "
            "on sugarcane leaves. The exact causal virus can vary."
        ),
        "symptoms": [
            "Light and dark green patches may form a mosaic pattern.",
            "Leaf color may appear uneven or streaked.",
            "Severe symptoms may be associated with reduced plant vigor."
        ],
        "management": [
            "Verify the suspected disease with a local sugarcane specialist.",
            "Follow regional advice on managing affected plants.",
            "Use certified healthy planting material when available."
        ],
        "prevention": [
            "Use disease-free seed cane.",
            "Monitor crops for unusual mosaic patterns.",
            "Follow regional recommendations for resistant varieties and sanitation."
        ]
    },

    "Sugarcane___Red_rot": {
        "plant": "Sugarcane",
        "disease": "Red Rot",
        "description": (
            "A serious sugarcane disease associated with the fungus "
            "Colletotrichum falcatum."
        ),
        "symptoms": [
            "Internal stalk tissue may show reddish discoloration.",
            "Pale patches may appear within red tissue.",
            "Affected stalks may deteriorate and produce an abnormal smell."
        ],
        "management": [
            "Seek prompt expert confirmation if red rot is suspected.",
            "Use locally recommended disease-management practices.",
            "Avoid using suspected infected stalks as planting material."
        ],
        "prevention": [
            "Use healthy, disease-free seed cane.",
            "Follow regional resistant-variety recommendations.",
            "Sanitize tools and manage infected residue as locally advised."
        ]
    },

    "Sugarcane___Rust": {
        "plant": "Sugarcane",
        "disease": "Rust",
        "description": (
            "A sugarcane leaf disease category characterized by rust-like "
            "pustules. Several rust species can affect sugarcane."
        ),
        "symptoms": [
            "Orange, brown, or reddish pustules may occur on leaves.",
            "Leaf tissue around lesions may become discolored.",
            "Severe infection may reduce functional leaf area."
        ],
        "management": [
            "Confirm the rust type where possible.",
            "Follow locally recommended variety and crop-management guidance.",
            "Seek local expert advice before treatment decisions."
        ],
        "prevention": [
            "Monitor leaves for developing pustules.",
            "Use locally recommended varieties where available.",
            "Maintain field sanitation and crop monitoring."
        ]
    },

    "Sugarcane___Yellow_disease": {
        "plant": "Sugarcane",
        "disease": "Yellow Disease",
        "description": (
            "A yellowing-related sugarcane condition in this dataset. "
            "The label alone does not establish the exact cause, which "
            "may require expert diagnosis."
        ),
        "symptoms": [
            "Leaves may develop yellow discoloration.",
            "Yellowing may vary in distribution and severity.",
            "Plant vigor may decline depending on the underlying cause."
        ],
        "management": [
            "Inspect plants and confirm the underlying cause.",
            "Check for nutritional, water-related, pest, and disease problems.",
            "Seek region-specific sugarcane management advice."
        ],
        "prevention": [
            "Use healthy planting material.",
            "Maintain suitable soil nutrition and irrigation.",
            "Monitor crop symptoms and consult local agricultural services."
        ]
    },

    "Sugarcane___healthy": {
        "plant": "Sugarcane",
        "disease": "Healthy",
        "description": (
            "The model classified this image as a healthy sugarcane leaf. "
            "The prediction does not rule out every possible disease "
            "or plant health problem."
        ),
        "symptoms": [
            "No major disease symptoms were identified by the model.",
            "Inspect leaves for unusual spots, streaks, pustules, or yellowing."
        ],
        "management": [
            "Continue routine crop scouting.",
            "Maintain appropriate water and nutrition."
        ],
        "prevention": [
            "Use healthy seed cane.",
            "Monitor plants regularly.",
            "Maintain field sanitation and suitable growing conditions."
        ]
    },
}


# =========================================
# Main
# =========================================

def main():

    if not INFO_FILE.is_file():
        raise FileNotFoundError(
            f"Disease information file not found: {INFO_FILE}"
        )

    if not CHECKPOINT_FILE.is_file():
        raise FileNotFoundError(
            f"Model checkpoint not found: {CHECKPOINT_FILE}"
        )

    # Validate the new information before modifying files.
    with open(
        CHECKPOINT_FILE,
        "rb",
    ) as file:
        checkpoint = __import__("torch").load(
            file,
            map_location="cpu",
            weights_only=False,
        )

    classes = set(checkpoint["class_to_idx"])

    unknown_new_entries = (
        set(NEW_DISEASE_INFO) - classes
    )

    if unknown_new_entries:
        raise ValueError(
            "These new information entries do not match the model: "
            f"{sorted(unknown_new_entries)}"
        )

    with open(
        INFO_FILE,
        "r",
        encoding="utf-8",
    ) as file:

        existing_info = json.load(file)

    if not isinstance(existing_info, dict):
        raise ValueError(
            "Expected disease_info.json to contain a JSON object."
        )

    # Create the backup only if it doesn't already exist.
    if not BACKUP_FILE.exists():
        shutil.copy2(
            INFO_FILE,
            BACKUP_FILE,
        )

        print("Backup created:", BACKUP_FILE)

    # Add entries without overwriting existing content.
    added = 0

    for class_name, information in NEW_DISEASE_INFO.items():

        if class_name not in existing_info:
            existing_info[class_name] = information
            added += 1

    missing = classes - set(existing_info)

    if missing:
        raise ValueError(
            "Some model classes still lack disease information: "
            f"{sorted(missing)}. "
            "No changes were written."
        )

    # Write atomically so an interrupted write does not
    # leave a partially written JSON file.
    temporary_file = INFO_FILE.with_suffix(".tmp")

    with open(
        temporary_file,
        "w",
        encoding="utf-8",
    ) as file:

        json.dump(
            existing_info,
            file,
            indent=2,
            ensure_ascii=False,
        )

        file.write("\n")

    temporary_file.replace(INFO_FILE)

    print("\nDisease information updated successfully.")
    print("Classes in checkpoint:", len(classes))
    print("Entries added:", added)
    print("Total information entries:", len(existing_info))
    print("Updated file:", INFO_FILE)
    print("Backup:", BACKUP_FILE)


if __name__ == "__main__":
    main()
