"""
AgriSense - Bilingual Language System (English & Marathi)
Tailored for Maharashtra farmers in Pune, Nashik, Sangli, and Kolhapur regions.
"""

TRANSLATIONS = {
    "en": {
        "app_title": "AgriSense: Explainable Plant Disease Detection & Localized Advisory System",
        "app_subtitle": "Maharashtra Agricultural Intelligence Platform | Pune & Western Ghats Region",
        "lang_toggle_label": "भाषा निवडा / Select Language",
        "crop_select_header": "Step 1: Select Your Crop",
        "crop_select_label": "Select Crop:",
        "crops": {
            "Grapes": "Grapes (द्राक्ष)",
            "Tomato": "Tomato (टोमॅटो)",
            "Soybean": "Soybean (सोयाबीन)",
        },
        "district_select_label": "Select Agricultural Region (Maharashtra):",
        "input_method_header": "Step 2: Upload or Capture Leaf Image",
        "input_method_label": "Choose Image Input Method:",
        "method_upload": "📁 Upload Image from Device",
        "method_camera": "📷 Live Camera Capture",
        "uploader_label": "Choose a clear JPG, PNG or WEBP close-up leaf image:",
        "camera_label": "Capture leaf photo with camera:",
        "analyze_btn": "🔬 Run Diagnosis & AI Analysis",
        "analyzing_spinner": "Running EfficientNet-B0 inference & computing Grad-CAM saliency...",
        
        # Results Section
        "results_header": "Step 3: Diagnostic Findings & Explainability",
        "crop_mismatch_alert": "Crop Mismatch Warning",
        "detected_disease_label": "Identified Condition",
        "confidence_label": "Model Confidence",
        "severity_label": "Severity Stage",
        "pathogen_label": "Pathogen Class",
        "symptoms_header": "Disease Symptoms & Identification",
        "symptoms_label": "Common Symptoms:",
        "low_confidence_warning": "Low confidence detection. Please upload a clearer, well-lit image of a single leaf.",
        "tabs_analysis": {
            "tab_heatmap": "🔥 Grad-CAM Heatmap",
            "tab_lesion": "🎯 Lesion Severity Mask",
            "tab_side_by_side": "↔️ Side-by-Side Comparison",
            "tab_top3": "📊 Class Probability Distribution"
        },
        "heatmap_explanation": "Grad-CAM visualizes the exact convolutional feature regions influencing the AI prediction. Red/yellow zones highlight active infection foci.",

        # Weather & Progression Section
        "weather_progression_header": "Step 4: Live Microclimate & Progression Risk",
        "weather_source": "Live Meteorological Feed",
        "temp_label": "Temperature",
        "humidity_label": "Relative Humidity",
        "wind_label": "Wind Velocity",
        "progression_warning_title": "Progression Risk Assessment",

        # Localized Treatment Section
        "treatment_header": "Step 5: Localized Maharashtra Treatment Advisory",
        "chemical_tab_title": "🧪 Chemical Controls (Pesticides)",
        "organic_tab_title": "🌿 Organic & Bio Alternatives",
        "preventive_tab_title": "🛡️ Preventive Agronomic Measures",
        "col_chem_name": "Product & Active Ingredient",
        "col_chem_dosage": "Recommended Dosage",
        "col_chem_cost": "Approx. Market Cost (₹)",
        "col_chem_phi": "Pre-Harvest Interval (PHI)",
        "listen_advisory_btn": "🔊 Listen to Voice Advisory (Read Aloud)",
        "disclaimer_header": "⚠️ Official Statutory Advisory Disclaimer",
        "disclaimer_text": "The pesticide and management recommendations are based on research advisories from MPKV Rahuri and ICAR-NRC Grapes. Farmers are strongly advised to verify with their local Taluka Krishi Adhikari (तालुका कृषी अधिकारी) or authorized Krishi Seva Kendra before field tank mixing. Wear protective gear.",

        # Chatbot Section
        "chatbot_header": "Step 6: Grounded Plant Health Assistant",
        "chatbot_subtitle": "Ask follow-up questions strictly related to the detected disease and treatment dosage.",
        "chat_placeholder": "Ask about spraying dosage, market cost, organic remedies, or best time to spray...",
        "send_btn": "Send",
        "suggested_questions_label": "Quick Questions:",
        "suggested_questions": [
            "What is the exact dosage per 15L pump?",
            "What organic alternative can I use?",
            "What is the approximate market price in Maharashtra?",
            "What is the best time to spray?"
        ],

        # Download Report Section
        "report_header": "Step 7: Download Formal Advisory Report",
        "report_btn": "📥 Download PDF Diagnostic & Prescription Slip",
        "farmer_name_label": "Enter Farmer Name / Farm Plot ID:",
        "default_farmer_name": "Maharashtra Farmer (Grower)",
        "report_ready": "Your agricultural diagnostic slip has been generated successfully."
    },

    "mr": {
        "app_title": "अग्रीसेन्स (AgriSense): पिकांवरील रोग निदान आणि स्थानिक शेती सल्लागार प्रणाली",
        "app_subtitle": "महाराष्ट्र शेती बुद्धिमत्ता मंच | पुणे व पश्चिम महाराष्ट्र पट्टा",
        "lang_toggle_label": "Select Language / भाषा निवडा",
        "crop_select_header": "पायरी १: आपले पीक निवडा",
        "crop_select_label": "पीक निवडा:",
        "crops": {
            "Grapes": "द्राक्ष (Grapes)",
            "Tomato": "टोमॅटो (Tomato)",
            "Soybean": "सोयाबीन (Soybean)",
        },
        "district_select_label": "शेती विभाग / जिल्हा निवडा (महाराष्ट्र):",
        "input_method_header": "पायरी २: रोगाचे पान अपलोड करा किंवा कॅमेऱ्याने फोटो घ्या",
        "input_method_label": "फोटो देण्याची पद्धत निवडा:",
        "method_upload": "📁 मोबाईल / संगणकावरून फोटो अपलोड करा",
        "method_camera": "📷 लाईव्ह कॅमेऱ्याने पानाचा फोटो काढा",
        "uploader_label": "एका पानाचा स्पष्ट व चांगल्या प्रकाशातील फोटो निवडा (JPG, PNG):",
        "camera_label": "कॅमेऱ्याच्या चौकटीत पान ठेवून फोटो घ्या:",
        "analyze_btn": "🔬 रोग निदान व तपासणी सुरू करा",
        "analyzing_spinner": "कृत्रिम बुद्धिमत्ता (AI) द्वारे पानाचे विश्लेषण व ग्रॅड-कॅम तपासणी सुरू आहे...",

        # Results Section
        "results_header": "पायरी ३: रोग निदान व स्पष्टीकरण (Diagnosis & Grad-CAM)",
        "crop_mismatch_alert": "पीक निवडीमध्ये तफावत",
        "detected_disease_label": "आढळलेला रोग / स्थिती",
        "confidence_label": "मॉडेल अचूकता (Confidence)",
        "severity_label": "रोगाची तीव्रता (Severity)",
        "pathogen_label": "रोगाचा प्रकार",
        "symptoms_header": "रोगाची मुख्य लक्षणे व पाहणी (Disease Symptoms)",
        "symptoms_label": "रोगाची सामान्य लक्षणे:",
        "low_confidence_warning": "कमी अचूकता आढळली. कृपया एकाच पानाचा चांगल्या प्रकाशातील आणि स्पष्ट फोटो अपलोड करा.",
        "tabs_analysis": {
            "tab_heatmap": "🔥 ग्रॅड-कॅम हीटमॅप (Grad-CAM)",
            "tab_lesion": "🎯 रोगाचे प्रमाण (Lesion Mask)",
            "tab_side_by_side": "↔️ तुलनात्मक पाहणी",
            "tab_top3": "📊 संभाव्य रोगांची टक्केवारी"
        },
        "heatmap_explanation": "ग्रॅड-कॅम द्वारे मॉडेलने पानावरील नेमक्या कोणत्या भागावर लक्ष केंद्रित केले ते समजते. लाल व पिवळा भाग रोगाचा मुख्य प्रादुर्भाव दर्शवतो.",

        # Weather & Progression Section
        "weather_progression_header": "पायरी ४: स्थानिक हवामान आणि रोगाचा वाढीचा अंदाज",
        "weather_source": "लाईव्ह हवामान माहिती",
        "temp_label": "तापमान",
        "humidity_label": "हवेतील आर्द्रता",
        "wind_label": "वाऱ्याचा वेग",
        "progression_warning_title": "रोगाच्या प्रसाराचा अंदाज (Progression Risk)",

        # Localized Treatment Section
        "treatment_header": "पायरी ५: महाराष्ट्रासाठी स्थानिक औषध फवारणी व उपाय",
        "chemical_tab_title": "🧪 रासायनिक औषधे (बुरशीनाशक/कीटकनाशक)",
        "organic_tab_title": "🌿 सेंद्रिय व जैविक पर्याय",
        "preventive_tab_title": "🛡️ प्रतिबंधात्मक शेती पद्धती",
        "col_chem_name": "औषधाचे नाव व घटक",
        "col_chem_dosage": "फवारणीचे प्रमाण (प्रति लिटर)",
        "col_chem_cost": "अंदाजे बाजारभाव (₹)",
        "col_chem_phi": "काढणी कालावधी (PHI दिवस)",
        "listen_advisory_btn": "🔊 व्हॉईस सल्ला ऐका (मराठीत ऑडिओ)",
        "disclaimer_header": "⚠️ वैधानिक कृषी सल्ला सूचना (Statutory Disclaimer)",
        "disclaimer_text": "औषध फवारणीची शिफारस महात्मा फुले कृषी विद्यापीठ (राहुरी) आणि राष्ट्रीय द्राक्ष संशोधन केंद्र (पुणे) यांच्या मार्गदर्शक तत्त्वांवर आधारित आहे. मोठ्या प्रमाणावर फवारणी करण्यापूर्वी आपल्या तालुका कृषी अधिकारी किंवा कृषी सेवा केंद्राचा सल्ला घ्या. फवारणी करताना तोंडाला मास्क व हातमोजे वापरा.",

        # Chatbot Section
        "chatbot_header": "पायरी ६: अग्रीसेन्स शेती सल्लागार (AI Chatbot)",
        "chatbot_subtitle": "आढळलेल्या रोगाच्या उपचारासंबंधी, फवारणीच्या प्रमाणासंबंधी किंवा खतांसंबंधी प्रश्न विचारा.",
        "chat_placeholder": "औषधाचे प्रमाण, फवारणीची वेळ किंवा सेंद्रिय उपायांबद्दल विचारा...",
        "send_btn": "पाठवा",
        "suggested_questions_label": "विचारण्यासाठी नेहमीचे प्रश्न:",
        "suggested_questions": [
            "१५ लिटर पंपासाठी औषधाचे प्रमाण किती टाकावे?",
            "या रोगावर कोणता सेंद्रिय उपाय करावा?",
            "औषधाची बाजारात अंदाजे किंमत किती आहे?",
            "फवारणीची योग्य वेळ कोणती?"
        ],

        # Download Report Section
        "report_header": "पायरी ७: कृषी निदान अहवाल डाऊनलोड करा",
        "report_btn": "📥 अधिकृत PDF निदान अहवाल डाऊनलोड करा",
        "farmer_name_label": "शेतकऱ्याचे नाव / गट नंबर:",
        "default_farmer_name": "महाराष्ट्र शेतकरी (बागायतदार)",
        "report_ready": "आपला कृषी निदान अहवाल तयार झाला आहे."
    }
}


def get_text(key: str, lang: str = "en") -> str:
    """Retrieve translated text string for given key."""
    dict_lang = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    return dict_lang.get(key, TRANSLATIONS["en"].get(key, key))
