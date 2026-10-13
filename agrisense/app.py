"""
AgriSense: Explainable Plant Disease Detection & Localized Advisory System for Maharashtra Farmers
Main Streamlit Application
"""

import sys
from datetime import datetime
from pathlib import Path
from PIL import Image
import streamlit as st

# Ensure repository root is in python path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from agrisense.core.model import AgriSenseModel
from agrisense.core.gradcam import GradCAMExplainer
from agrisense.core.severity import estimate_severity
from agrisense.core.weather import (
    MAHARASHTRA_DISTRICTS,
    fetch_live_weather,
    evaluate_progression_warning
)
from agrisense.core.chatbot import GroundedAgriChatbot
from agrisense.core.report_generator import generate_pdf_report
from agrisense.core.tts import synthesize_advisory_speech
from agrisense.data.treatments_db import get_treatment_for_disease, CROP_MAPPING
from agrisense.utils.translations import TRANSLATIONS, get_text


# =============================================================================
# Streamlit Page Configuration & Modern Agritech Theme
# =============================================================================
st.set_page_config(
    page_title="AgriSense | Maharashtra Plant Disease Advisory",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for polished, mobile-responsive UI
st.markdown("""
<style>
    /* Primary Colors & Typography */
    .main-title {
        color: #1b5e20;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        margin-bottom: 0px;
    }
    .sub-title {
        color: #4a5568;
        font-size: 1.05rem;
        margin-bottom: 20px;
    }
    .step-card {
        background: #f8faf8;
        border-left: 5px solid #2e7d32;
        padding: 14px 18px;
        border-radius: 8px;
        margin-bottom: 16px;
    }
    .step-header {
        color: #1b5e20;
        font-weight: 600;
        font-size: 1.15rem;
        margin-bottom: 6px;
    }
    .metric-badge {
        padding: 6px 12px;
        border-radius: 6px;
        font-weight: 600;
        display: inline-block;
    }
    .stButton>button {
        background-color: #2e7d32;
        color: white;
        border-radius: 8px;
        font-weight: 600;
        border: none;
        padding: 0.5rem 1.2rem;
    }
    .stButton>button:hover {
        background-color: #1b5e20;
        color: white;
    }
    /* Tab Styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #e8f5e9;
        border-radius: 6px 6px 0 0;
        padding: 8px 16px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #2e7d32 !important;
        color: white !important;
    }
</style>
""", unsafe_allow_html=True)


# =============================================================================
# Cached Resource Initialization
# =============================================================================
@st.cache_resource(show_spinner="Initializing AgriSense Deep Learning Engine...")
def load_agrisense_engine():
    model_engine = AgriSenseModel()
    explainer = GradCAMExplainer(model_engine)
    chatbot = GroundedAgriChatbot()
    return model_engine, explainer, chatbot


model_engine, explainer, chatbot = load_agrisense_engine()


# =============================================================================
# Session State Initialization
# =============================================================================
if "language" not in st.session_state:
    st.session_state["language"] = "en"  # "en" or "mr"

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

if "last_analysis" not in st.session_state:
    st.session_state["last_analysis"] = None


# =============================================================================
# Sidebar: Language Toggle & Regional Agricultural Controls
# =============================================================================
with st.sidebar:
    st.image(
        "https://images.unsplash.com/photo-1595974482597-4b8da8879bc5?auto=format&fit=crop&w=400&q=80",
        caption="Maharashtra Agritech Intelligence (पुणे व नाशिक पट्टा)",
        use_container_width=True
    )

    # 1. Bilingual Switcher (Type-safe static keys)
    st.markdown("### 🌐 भाषा / Language")
    lang_code = st.radio(
        label="Select Application Language:",
        options=["en", "mr"],
        format_func=lambda l: "English" if l == "en" else "मराठी (Marathi)",
        horizontal=True,
        key="agrisense_lang_radio"
    )
    st.session_state["language"] = lang_code
    lang = lang_code
    t = TRANSLATIONS[lang]

    st.markdown("---")

    # 2. Agricultural District Selection (Default: Pune)
    st.markdown(f"### 📍 {t['district_select_label']}")
    selected_district = st.selectbox(
        label="District / Belt:",
        options=list(MAHARASHTRA_DISTRICTS.keys()),
        index=0,
        key="agrisense_district_selector"
    )

    # Fetch live weather for the selected region (in-memory cached)
    owm_key = None
    try:
        if "OPENWEATHERMAP_API_KEY" in st.secrets:
            owm_key = st.secrets["OPENWEATHERMAP_API_KEY"]
    except Exception:
        owm_key = None
    weather_data = fetch_live_weather(selected_district, owm_api_key=owm_key)

    # Quick Weather Card in Sidebar
    st.markdown(f"""
    <div style="background:#e8f5e9; padding:12px; border-radius:8px; border:1px solid #c8e6c9;">
        <div style="font-weight:600; color:#1b5e20;">🌤️ {weather_data['district']}</div>
        <div style="font-size:0.9rem; color:#2e7d32;">
            🌡️ <b>{t['temp_label']}:</b> {weather_data['temperature_c']}°C<br>
            💧 <b>{t['humidity_label']}:</b> {weather_data['humidity_percent']}%<br>
            💨 <b>{t['wind_label']}:</b> {weather_data['wind_speed_kmh']} km/h<br>
            <i>{weather_data['description']}</i>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    **AgriSense System Profile:**
    - **Core DL Backbone:** EfficientNet-B0 (PyTorch)
    - **Explainability:** Grad-CAM Hook Architecture
    - **Target Crops:** Grapes, Tomato, Soybean
    - **Advisory Source:** MPKV Rahuri & ICAR
    """)


# =============================================================================
# Main Application Content
# =============================================================================
st.markdown(f"<h1 class='main-title'>🌿 {t['app_title']}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='sub-title'>{t['app_subtitle']}</p>", unsafe_allow_html=True)

col_input1, col_input2 = st.columns([1, 1], gap="medium")

# -----------------------------------------------------------------------------
# STEP 1: Crop Selection (Type-safe static keys with format_func)
# -----------------------------------------------------------------------------
with col_input1:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">🌱 {t['crop_select_header']}</div>
    </div>
    """, unsafe_allow_html=True)
    
    crop_options = ["Grapes", "Tomato", "Soybean"]
    selected_crop = st.selectbox(
        label=t["crop_select_label"],
        options=crop_options,
        format_func=lambda c: t["crops"].get(c, c),
        index=0,
        key="agrisense_crop_selector"
    )

    # If the user switched crops, automatically reset previous scan so no state conflict occurs
    if st.session_state.get("previous_crop") != selected_crop:
        st.session_state["previous_crop"] = selected_crop
        st.session_state["last_analysis"] = None
        st.session_state["analyzed_signature"] = None
        st.session_state["cached_pdf"] = None

# -----------------------------------------------------------------------------
# STEP 2: Leaf Image Input (Upload or Webcam)
# -----------------------------------------------------------------------------
with col_input2:
    st.markdown(f"""
    <div class="step-card">
        <div class="step-header">📷 {t['input_method_header']}</div>
    </div>
    """, unsafe_allow_html=True)

    input_mode = st.radio(
        label=t["input_method_label"],
        options=["upload", "camera"],
        format_func=lambda m: t["method_upload"] if m == "upload" else t["method_camera"],
        horizontal=True,
        key="agrisense_input_mode"
    )

    image_source = None
    if input_mode == "upload":
        uploaded_file = st.file_uploader(
            label=t["uploader_label"],
            type=["jpg", "jpeg", "png", "webp"],
            help="High-contrast close-up leaf images produce maximum diagnostic precision.",
            key="agrisense_uploader"
        )
        if uploaded_file is not None:
            image_source = uploaded_file
    else:
        camera_file = st.camera_input(
            label=t["camera_label"],
            help="Position single affected leaf in focus and click take photo.",
            key="agrisense_camera"
        )
        if camera_file is not None:
            image_source = camera_file

st.markdown("---")


# =============================================================================
# Diagnostic Analysis Execution
# =============================================================================
if image_source is not None:
    try:
        pil_image = Image.open(image_source).convert("RGB")
    except Exception as e:
        st.error(f"Error loading uploaded image: {e}")
        pil_image = None

    if pil_image is not None:
        # Show uploaded leaf thumbnail preview
        prev_col, btn_col = st.columns([1, 2])
        with prev_col:
            st.image(pil_image, caption="Selected Leaf Image", width=160)
        with btn_col:
            st.write("")
            st.write("")
            run_btn = st.button(f"🔬 {t['analyze_btn']}", use_container_width=True, type="primary")

        img_signature = f"{selected_crop}_{getattr(image_source, 'name', 'cam')}_{getattr(image_source, 'size', 0)}"
        needs_analysis = run_btn or (st.session_state.get("analyzed_signature") != img_signature and run_btn)

        if needs_analysis:
            with st.spinner(t["analyzing_spinner"]):
                # 1. Run Crop-conditioned DL Inference
                pred_res = model_engine.predict(
                    image=pil_image,
                    selected_crop=selected_crop,
                    confidence_threshold=0.70
                )

                # 2. Compute Grad-CAM Heatmap
                cam_res = explainer.generate_cam(
                    image=pil_image,
                    target_class_idx=pred_res["predicted_idx"]
                )

                # 3. Estimate Severity % (HSV + Saliency Fusion)
                sev_res = estimate_severity(
                    image=pil_image,
                    heatmap=cam_res["raw_heatmap"],
                    is_healthy=pred_res["is_healthy"]
                )

                # 4. Fetch Treatment Data
                treatment_info = get_treatment_for_disease(pred_res["class_key"])

                # 5. Evaluate Progression Risk based on humidity
                prog_res = evaluate_progression_warning(
                    disease_key=pred_res["class_key"],
                    severity_level=sev_res["level"],
                    humidity=weather_data["humidity_percent"],
                    temp_c=weather_data["temperature_c"],
                    language=lang
                )

                # 6. Pre-synthesize Voice Advisory Audio once
                d_name = treatment_info["display_name_mr"] if lang == "mr" else treatment_info["display_name_en"]
                s_name = sev_res["level_mr"] if lang == "mr" else sev_res["level"]
                chem_top = treatment_info['chemical_treatments'][0]['name'] if treatment_info.get('chemical_treatments') else ''
                chem_dos = treatment_info['chemical_treatments'][0]['dosage'] if treatment_info.get('chemical_treatments') else ''
                tts_text = (
                    f"{d_name} चे निदान झाले आहे. रोगाची तीव्रता {s_name} आहे. "
                    f"मुख्य उपाय: {chem_top}. प्रमाण: {chem_dos}."
                ) if lang == "mr" else (
                    f"Diagnosed with {d_name}. Severity stage is {sev_res['level']}. "
                    f"Recommended spray is {chem_top} at {chem_dos}."
                )
                audio_cache = synthesize_advisory_speech(tts_text, language=lang)

                # Store analysis in session state
                st.session_state["analyzed_signature"] = img_signature
                st.session_state["last_analysis"] = {
                    "image": pil_image,
                    "crop": selected_crop,
                    "prediction": pred_res,
                    "gradcam": cam_res,
                    "severity": sev_res,
                    "treatment": treatment_info,
                    "progression": prog_res,
                    "weather": weather_data,
                    "audio_bytes": audio_cache,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }


# =============================================================================
# Render Analysis Results
# =============================================================================
if st.session_state["last_analysis"] is not None:
    analysis = st.session_state["last_analysis"]
    pred = analysis["prediction"]
    cam = analysis["gradcam"]
    sev = analysis["severity"]
    treat = analysis["treatment"]
    prog = analysis["progression"]
    weather = analysis["weather"]
    orig_img = analysis["image"]

    disease_title = treat["display_name_mr"] if lang == "mr" else treat["display_name_en"]
    sev_text = sev["level_mr"] if lang == "mr" else sev["level"]

    # -------------------------------------------------------------------------
    # STEP 3: Results & Explainability
    # -------------------------------------------------------------------------
    st.markdown(f"### 🔍 {t['results_header']}")

    # Warning 1: Crop Mismatch Warning
    if pred.get("crop_mismatch_warning"):
        st.warning(f"⚠️ **{t['crop_mismatch_alert']}:** {pred['crop_mismatch_warning']}")

    # Warning 2: Confidence Threshold (< 70%) Warning
    if pred["is_low_confidence"]:
        st.error(f"⚠️ **{t['low_confidence_warning']}** ({t['confidence_label']}: {pred['confidence_percent']}%)")

    # High-level Metric Badges
    m_col1, m_col2, m_col3, m_col4 = st.columns(4)
    with m_col1:
        st.metric(
            label=t["detected_disease_label"],
            value=disease_title,
            delta="Healthy" if pred["is_healthy"] else "Pathogen Active",
            delta_color="normal" if pred["is_healthy"] else "inverse"
        )
    with m_col2:
        st.metric(
            label=t["confidence_label"],
            value=f"{pred['confidence_percent']}%",
            delta="High Accuracy" if not pred["is_low_confidence"] else "Review Required",
            delta_color="normal" if not pred["is_low_confidence"] else "off"
        )
    with m_col3:
        st.metric(
            label=t["severity_label"],
            value=f"{sev_text} ({sev['affected_percentage']}%)",
            delta=sev["level"]
        )
    with m_col4:
        st.metric(
            label=t["pathogen_label"],
            value=treat.get("pathogen_type", "Fungal"),
            delta=treat.get("causal_organism", "Pathogen")[:20]
        )

    # Visual Explainability Tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        t["tabs_analysis"]["tab_heatmap"],
        t["tabs_analysis"]["tab_side_by_side"],
        t["tabs_analysis"]["tab_lesion"],
        t["tabs_analysis"]["tab_top3"]
    ])

    with tab1:
        st.markdown(f"*{t['heatmap_explanation']}*")
        c1, c2 = st.columns(2)
        with c1:
            st.image(orig_img, caption="Original Uploaded Leaf", use_container_width=True)
        with c2:
            st.image(cam["overlay_pil"], caption="Grad-CAM Convolutional Heatmap Overlay", use_container_width=True)

    with tab2:
        st.image(cam["side_by_side_pil"], caption="Side-by-Side: Original Leaf vs Saliency Attention Map", use_container_width=True)

    with tab3:
        lc1, lc2 = st.columns(2)
        with lc1:
            st.image(sev["annotated_mask_pil"], caption="Annotated Lesion Segmentation Mask (HSV Deconvolution)", use_container_width=True)
        with lc2:
            st.markdown(f"""
            **Severity Quantification Summary:**
            - **Estimated Surface Damage:** `{sev['affected_percentage']}%`
            - **Severity Classification:** **{sev_text}**
            - **Clinical Assessment:** {sev['description_mr'] if lang == 'mr' else sev['description_en']}
            """)

    with tab4:
        st.markdown("**Top-3 Bayesian Class Probabilities:**")
        for p_item in pred["top_predictions"][:3]:
            class_info = get_treatment_for_disease(p_item["class_key"])
            c_name = class_info["display_name_mr"] if lang == "mr" else class_info["display_name_en"]
            st.write(f"- **{c_name}:** `{p_item['confidence_percent']}%`")
            st.progress(min(1.0, p_item["confidence"]))

    # Symptoms & Diagnostic Signs Section
    symptoms_list = treat.get("symptoms_mr" if lang == "mr" else "symptoms_en", [])
    if symptoms_list:
        with st.expander(f"🔎 {t.get('symptoms_header', 'Disease Symptoms')}", expanded=True):
            st.markdown(f"**{t.get('symptoms_label', 'Common Symptoms:')}**")
            for s_item in symptoms_list:
                st.markdown(f"- {s_item}")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # STEP 4: Live Weather & Progression Risk
    # -------------------------------------------------------------------------
    st.markdown(f"### 🌦️ {t['weather_progression_header']}")

    w_col1, w_col2 = st.columns([1, 2])
    with w_col1:
        st.markdown(f"""
        <div style="background:#eef7ee; padding:16px; border-radius:8px; border:1px solid #c8e6c9;">
            <div style="font-size:1.1rem; font-weight:700; color:#1b5e20;">📍 {weather['district']}</div>
            <div style="margin-top:8px;">
                🌡️ <b>{t['temp_label']}:</b> {weather['temperature_c']}°C<br>
                💧 <b>{t['humidity_label']}:</b> {weather['humidity_percent']}%<br>
                💨 <b>{t['wind_label']}:</b> {weather['wind_speed_kmh']} km/h<br>
                📡 <i>{t['weather_source']}: {weather['source']}</i>
            </div>
        </div>
        """, unsafe_allow_html=True)

    with w_col2:
        banner_type = prog.get("banner_type", "info")
        title_txt = prog["title_mr"] if lang == "mr" else prog["title_en"]
        msg_txt = prog["message_mr"] if lang == "mr" else prog["message_en"]
        act_txt = prog["action_mr"] if lang == "mr" else prog["action_en"]

        if banner_type == "error":
            st.error(f"**{title_txt}**\n\n{msg_txt}\n\n👉 **Recommended Action:** {act_txt}")
        elif banner_type == "warning":
            st.warning(f"**{title_txt}**\n\n{msg_txt}\n\n👉 **Recommended Action:** {act_txt}")
        else:
            st.success(f"**{title_txt}**\n\n{msg_txt}\n\n👉 **Recommended Action:** {act_txt}")

    st.markdown("---")

    # -------------------------------------------------------------------------
    # STEP 5: Localized Treatment Recommendations
    # -------------------------------------------------------------------------
    st.markdown(f"### 💊 {t['treatment_header']}")

    # TTS Audio Listen
    audio_bytes = analysis.get("audio_bytes")
    if not audio_bytes:
        audio_bytes = synthesize_advisory_speech(tts_text, language=lang)
        analysis["audio_bytes"] = audio_bytes
    if audio_bytes:
        st.audio(audio_bytes, format="audio/mp3")

    treat_tab1, treat_tab2, treat_tab3 = st.tabs([
        t["chemical_tab_title"],
        t["organic_tab_title"],
        t["preventive_tab_title"]
    ])

    with treat_tab1:
        st.markdown("**Chemical Fungicide / Pesticide Prescriptions (Maharashtra APMC Market):**")
        for idx, chem in enumerate(treat.get("chemical_treatments", [])):
            with st.expander(f"🧪 {idx+1}. {chem['name']}", expanded=(idx == 0)):
                st.write(f"• **{t['col_chem_dosage']}:** `{chem['dosage']}`")
                st.write(f"• **{t['col_chem_cost']}:** `{chem['cost_range_inr']}`")
                st.write(f"• **{t['col_chem_phi']}:** `{chem['phi_days']} Days before harvest`")
                st.write(f"• **Application Timing:** {chem['application_schedule']}")

    with treat_tab2:
        st.markdown("**Organic & Biological Alternatives (Zero Chemical Residue):**")
        for idx, org in enumerate(treat.get("organic_treatments", [])):
            with st.expander(f"🌿 {idx+1}. {org['name']}", expanded=(idx == 0)):
                st.write(f"• **Dosage / Rate:** `{org['dosage']}`")
                st.write(f"• **Cost:** `{org['cost_range_inr']}`")
                st.write(f"• **Preparation Instructions:** {org.get('prep_instructions', 'Apply in early morning/evening.')}")

    with treat_tab3:
        st.markdown("**Field Hygiene & Cultural Hygiene Measures:**")
        prev_items = treat.get("preventive_measures_mr" if lang == "mr" else "preventive_measures_en", [])
        for item in prev_items:
            st.write(f"✅ {item}")
        st.info(f"**Regional Field Note:** {treat.get('maharashtra_zone_notes', 'Standard for Maharashtra agronomy.')}")

    # Prominent Statutory Disclaimer
    st.markdown(f"""
    <div style="background:#fff3e0; border-left:5px solid #ff9800; padding:12px; border-radius:6px; margin-top:16px;">
        <b style="color:#e65100;">{t['disclaimer_header']}</b><br>
        <span style="font-size:0.85rem; color:#424242;">{t['disclaimer_text']}</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # -------------------------------------------------------------------------
    # STEP 6: Grounded AI Chatbot Section
    # -------------------------------------------------------------------------
    st.markdown(f"### 🤖 {t['chatbot_header']}")
    st.caption(t["chatbot_subtitle"])

    # Quick Suggestion Question Buttons
    st.write(f"**{t['suggested_questions_label']}**")
    q_cols = st.columns(4)
    suggested_clicked = None
    for i, q in enumerate(t["suggested_questions"]):
        with q_cols[i]:
            if st.button(q, key=f"sugg_q_{i}", use_container_width=True):
                suggested_clicked = q

    # Render Existing Chat History
    for msg in st.session_state["chat_history"]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # User Input Field
    user_query = st.chat_input(placeholder=t["chat_placeholder"])
    prompt_to_send = user_query or suggested_clicked

    if prompt_to_send:
        # Display User Message
        st.session_state["chat_history"].append({"role": "user", "content": prompt_to_send})
        with st.chat_message("user"):
            st.markdown(prompt_to_send)

        # Context Object for Grounding
        detection_context = {
            "selected_crop": analysis["crop"],
            "class_key": pred["class_key"],
            "severity_level": sev["level"],
            "weather": weather
        }

        # Generate Grounded Reply
        with st.chat_message("assistant"):
            with st.spinner("Consulting agricultural database..."):
                reply = chatbot.generate_reply(
                    user_prompt=prompt_to_send,
                    detection_context=detection_context,
                    language=lang
                )
                st.markdown(reply)
                st.session_state["chat_history"].append({"role": "assistant", "content": reply})

    st.markdown("---")

    # -------------------------------------------------------------------------
    # STEP 7: Download Formal PDF Diagnosis Report
    # -------------------------------------------------------------------------
    st.markdown(f"### 📄 {t['report_header']}")
    
    rep_col1, rep_col2 = st.columns([1, 1])
    with rep_col1:
        farmer_input = st.text_input(
            label=t["farmer_name_label"],
            value=t["default_farmer_name"]
        )
    with rep_col2:
        st.write("") # vertical spacing
        st.write("")
        pdf_cache_key = f"{farmer_input}_{analysis['crop']}_{pred['class_key']}"
        if "cached_pdf" not in st.session_state or st.session_state.get("cached_pdf_key") != pdf_cache_key:
            st.session_state["cached_pdf"] = generate_pdf_report(
                crop=analysis["crop"],
                detection_res=pred,
                treatment_info=treat,
                weather_info=weather,
                progression_info=prog,
                severity_res=sev,
                original_img=orig_img,
                gradcam_img=cam["overlay_pil"],
                farmer_name=farmer_input,
                taluka_district=weather["district"]
            )
            st.session_state["cached_pdf_key"] = pdf_cache_key

        pdf_bytes = st.session_state["cached_pdf"]
        file_name = f"AgriSense_Prescription_{analysis['crop']}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"
        st.download_button(
            label=t["report_btn"],
            data=pdf_bytes,
            file_name=file_name,
            mime="application/pdf",
            use_container_width=True
        )

else:
    # Initial Landing Prompt
    st.info(
        "👋 **Welcome to AgriSense!** Please select your crop in Step 1 and upload or capture a leaf photo in Step 2 to begin."
        if lang == "en" else
        "👋 **अग्रीसेन्स प्रणालीत आपले स्वागत आहे!** कृपया पायरी १ मध्ये आपले पीक निवडा आणि पायरी २ मध्ये पानाचा फोटो देऊन निदान सुरू करा."
    )
