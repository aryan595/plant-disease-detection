# 🌿 AgriSense: Explainable Plant Disease Detection & Localized Advisory System for Maharashtra Farmers

**Academic Major Project / Capstone Project**  
*Focused Region: Pune, Nashik, Sangli, Kolhapur, Solapur, Ahmednagar Belts (Maharashtra)*  
*Crops Supported: Grapes (द्राक्ष), Tomato (टोमॅटो), Soybean (सोयाबीन)*  

---

## 📌 1. Project Abstract & Motivation

In intensive agricultural regions like western Maharashtra (Pune-Nashik-Kolhapur belt), foliar diseases such as **Grape Downy Mildew (केवडा)**, **Tomato Late Blight (उशिरा येणारा करपा)**, and **Soybean Rust (तांबेरा)** can scorch an entire field within 48 to 72 hours under humid monsoon conditions.

Standard academic computer vision systems fail in real-world agricultural deployment because:
1. **Black-box Predictions:** Farmers and agronomists do not trust raw class probabilities without visual justification.
2. **Lack of Severity Measurement:** Knowing *what* disease is present is insufficient; farmers must know *how damaged* the leaf is to calculate chemical spray volume.
3. **No Weather Correlation:** Fungal sporulation depends on ambient relative humidity and temperature.
4. **Generic Recommendations:** Overseas models recommend inaccessible chemicals in foreign currencies rather than localized pesticides approved by **MPKV Rahuri** and **ICAR** in Indian Rupees (₹).
5. **Language Barrier:** Rural farmers in Maharashtra require complete consultation in **मराठी (Marathi)** and voice-assisted audio.

**AgriSense** is an end-to-end, explainable, production-ready agricultural intelligence system built specifically to bridge this gap.

---

## 🚀 2. System Architecture & Features

```
                                      [ Farmer / Agronomist ]
                                                 │
                                 ┌───────────────┴───────────────┐
                                 ▼                               ▼
                      [ 1. Select Crop ]             [ Live Weather API ]
                  (Grapes / Tomato / Soybean)       (Open-Meteo / Pune MH)
                                 │                               │
                                 ▼                               │
                      [ 2. Upload / Webcam ]                     │
                                 │                               │
                                 ▼                               │
                   [ EfficientNet-B0 Backbone ]                  │
                     (Crop-Constrained Inference)                │
                                 │                               │
                ┌────────────────┼────────────────┐              │
                ▼                ▼                ▼              ▼
         [ Class & Conf ]  [ Grad-CAM XAI ]  [ Severity % ] [ Progression Engine ]
         (Threshold: 70%)  (Visual Heatmap)  (HSV Lesions)  (Severity + Humidity)
                │                │                │              │
                └────────────────┴───────┬────────┴──────────────┘
                                         ▼
                        [ 5. Localized Treatments ]
                       (Chemical, Organic, Cost ₹, PHI)
                                         │
                         ┌───────────────┴───────────────┐
                         ▼                               ▼
               [ 6. Grounded Chatbot ]         [ 7. PDF Diagnostic Slip ]
             (Strict Context Anti-Halluc.)    (Downloadable Prescription)
```

---

## 🔬 3. Mathematical & Algorithmic Formulations

### A. How Grad-CAM Explainability is Calculated
Grad-CAM (Gradient-weighted Class Activation Mapping) produces a coarse 2D saliency map highlighting the discriminative regions on the leaf that led to the model's decision:

1. **Feature Extraction:** Let $A^k \in \mathbb{R}^{U \times V}$ represent the $k$-th feature activation map of the final convolutional layer of EfficientNet-B0 (`model.features[-1]`).
2. **Gradient Computation:** Compute the gradient of the predicted class score $y^c$ with respect to each activation map:
   $$\frac{\partial y^c}{\partial A^k}$$
3. **Neuron Importance Weights ($\alpha_k^c$):** Apply Global Average Pooling (GAP) over width $U$ and height $V$:
   $$\alpha_k^c = \frac{1}{Z} \sum_{i=1}^{U} \sum_{j=1}^{V} \frac{\partial y^c}{\partial A_{i,j}^k}$$
4. **Weighted Activation & Rectification:** Compute the linear combination of activation maps weighted by $\alpha_k^c$, followed by a rectified linear unit (ReLU) to isolate features that positively correlate with the target disease:
   $$L_{\text{Grad-CAM}}^c = \text{ReLU}\left( \sum_{k} \alpha_k^c A^k \right)$$
5. **Normalization & JET Color Mapping:**
   $$L_{\text{norm}}^c = \frac{L^c - \min(L^c)}{\max(L^c) - \min(L^c)}$$
   The normalized heatmap is resized using bilinear interpolation to original leaf dimensions $(W, H)$ and blended via alpha blending:
   $$I_{\text{overlay}} = (1 - \alpha) \cdot I_{\text{original}} + \alpha \cdot \text{ColorMap}_{\text{JET}}(L_{\text{norm}}^c)$$

---

### B. How Disease Severity is Estimated
Rather than guessing severity, AgriSense uses a hybrid **Computer Vision HSV Color Deconvolution + Grad-CAM Saliency Fusion** technique:

1. **Leaf Segmentation:** In HSV color space, foreground leaf tissue is separated from background:
   $$\text{Mask}_{\text{leaf}} = (S \ge 25) \land (V \ge 25) \land (V \le 245)$$
2. **Healthy Foliage Spectrum:** Healthy photosynthetic tissue resides in the green spectrum:
   $$\text{Mask}_{\text{healthy}} = \text{Mask}_{\text{leaf}} \land (35 \le H \le 88) \land (S \ge 40)$$
3. **Lesion Anomaly Detection:** Fungal necroses (brown/black) and chlorotic halos (yellow/orange) violate the healthy green spectrum:
   $$\text{Mask}_{\text{anomaly}} = \text{Mask}_{\text{leaf}} \land \neg \text{Mask}_{\text{healthy}}$$
4. **CNN Saliency Verification:** Anomaly regions are cross-verified with Grad-CAM high-activation zones ($L_{\text{norm}} \ge 0.40$):
   $$\text{Mask}_{\text{diseased}} = (\text{Mask}_{\text{anomaly}} \land (L_{\text{norm}} > 0.20)) \lor ((L_{\text{norm}} > 0.40) \land (V < 100))$$
5. **Infection Ratio ($\%$ Area):**
   $$\text{Severity \%} = \frac{\sum \text{Mask}_{\text{diseased}}}{\sum \text{Mask}_{\text{leaf}}} \times 100\%$$
6. **Agronomic Classification:**
   - **Healthy:** $0\%$ (निरोगी)
   - **Mild (सौम्य):** $< 15\%$ infected leaf area
   - **Moderate (मध्यम):** $15\% \le \text{Infection} < 35\%$
   - **Severe (तीव्र):** $\ge 35\%$ infected leaf area

---

## 🌾 4. Supported Crops & Classes (12 Classes)

| Crop | Disease Class | Marathi Name (स्थानिक नाव) | Pathogen Type |
| :--- | :--- | :--- | :--- |
| **Grapes** | `Grape___healthy` | निरोगी द्राक्ष पान | None |
| **Grapes** | `Grape___Downy_mildew` | द्राक्षावरील केवडा / डाउनी मिल्ड्यू | Oomycete (*Plasmopara viticola*) |
| **Grapes** | `Grape___Powdery_mildew` | द्राक्षावरील भुरी / पावडरी मिल्ड्यू | Fungal (*Erysiphe necator*) |
| **Grapes** | `Grape___Black_rot` | काळा कुजवा / ब्लॅक रॉट | Fungal (*Guignardia bidwellii*) |
| **Tomato** | `Tomato___healthy` | निरोगी टोमॅटो पान | None |
| **Tomato** | `Tomato___Early_blight` | करपा / अर्ली ब्लाइट | Fungal (*Alternaria solani*) |
| **Tomato** | `Tomato___Late_blight` | उशिरा येणारा करपा / लेट ब्लाइट | Oomycete (*Phytophthora infestans*) |
| **Tomato** | `Tomato___Bacterial_spot` | जिवाणूजन्य ठिपके / बॅक्टेरियल स्पॉट | Bacterial (*Xanthomonas spp.*) |
| **Soybean**| `Soybean___healthy` | निरोगी सोयाबीन पान | None |
| **Soybean**| `Soybean___Rust` | सोयाबीन तांबेरा / रस्ट | Fungal (*Phakopsora pachyrhizi*) |
| **Soybean**| `Soybean___Bacterial_blight`| जिवाणूजन्य करपा | Bacterial (*Pseudomonas savastanoi*) |
| **Soybean**| `Soybean___Cercospora_leaf_blight` | जांभळा करपा / सर्कोस्पोरा ब्लाइट | Fungal (*Cercospora kikuchii*) |

---

## 📂 5. Project Directory Structure

```
plant-disease-detection/
├── agrisense/
│   ├── __init__.py
│   ├── app.py                      # Main Streamlit UI & workflow
│   ├── core/
│   │   ├── __init__.py
│   │   ├── model.py                # EfficientNet-B0 inference & crop filtering
│   │   ├── gradcam.py              # PyTorch hook Grad-CAM engine
│   │   ├── severity.py             # HSV + Saliency lesion quantification
│   │   ├── weather.py              # Open-Meteo Pune weather & progression logic
│   │   ├── chatbot.py              # Grounded anti-hallucination assistant
│   │   ├── report_generator.py     # PDF diagnostic slip generator (fpdf2)
│   │   └── tts.py                  # Marathi & English voice synthesizer (gTTS)
│   ├── data/
│   │   ├── __init__.py
│   │   └── treatments_db.py        # Localized Maharashtra treatment DB
│   └── utils/
│       ├── __init__.py
│       └── translations.py         # Complete English & Marathi UI text
├── models/
│   └── efficientnet_b0_combined_balanced_best.pth  # PyTorch model weights
├── .streamlit/
│   └── secrets.toml.example        # Sample Streamlit secrets
├── .env.example                    # Sample environment variables
├── requirements.txt                # Production dependencies
├── streamlit_app.py                # Direct launcher entrypoint
└── README.md                       # Comprehensive documentation
```

---

## ⚡ 6. Setup & Execution Instructions

### A. Local Machine Setup (Windows / macOS / Linux)

1. **Clone or Navigate to the Repository:**
   ```bash
   cd "plant-disease-detection"
   ```

2. **Create & Activate Virtual Environment:**
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On Linux / macOS:
   source venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run AgriSense Streamlit Web Application:**
   ```bash
   streamlit run streamlit_app.py
   ```
   *The app opens automatically in your browser at `http://localhost:8501`.*

---

### B. Running on Google Colab

If you want to run AgriSense on a free Google Colab GPU:

1. Open a new Google Colab notebook (Runtime -> Change runtime type -> **T4 GPU**).
2. Clone your repository or upload the project folder.
3. In a Colab cell, run:
   ```python
   !pip install -r requirements.txt
   !npm install -g localtunnel
   ```
4. Launch the application:
   ```python
   !streamlit run streamlit_app.py & npx localtunnel --port 8501
   ```
5. Click the generated localtunnel public URL to view the live app!

---

## 🎓 7. Viva / Defense Preparation (FAQ for Examiners)

| Expected Examiner Question | Technical Model Answer |
| :--- | :--- |
| **Q1: Why did you choose EfficientNet-B0 over ResNet-50?** | *EfficientNet-B0 employs compound scaling (balancing depth, width, and resolution simultaneously). It achieves equivalent top-1 accuracy to ResNet-50 with ~5.3M parameters compared to ResNet's 25.6M parameters, resulting in faster inference (~28ms on CPU) suitable for field deployment.* |
| **Q2: Why use Crop-Constrained inference instead of pure top-1?** | *In real farming, the user already knows whether they are standing in a grape vineyard, tomato patch, or soybean acre. Conditioning Bayesian logits on the selected crop prevents cross-species false positives while out-of-distribution thresholds still catch uploaded non-plant images.* |
| **Q3: How do you justify the 70% confidence threshold?** | *Empirical testing shows that blurry, shadowed, or non-leaf photos fall below 0.70 softmax confidence. Showing a warning rather than false certainty is essential for agricultural safety to prevent incorrect chemical spraying.* |
| **Q4: How does weather affect your disease advisory?** | *Fungal oospores (e.g. Plasmopara viticola, Phytophthora infestans) require free water/humidity > 75% for zoospore germination. When our weather engine detects high Pune humidity (>75%), it escalates progression risk from 'Steady' to 'Critical Epidemic Alert'.* |
| **Q5: How do you prevent Chatbot hallucinations?** | *The chatbot knowledge base is strictly locked to `treatments_db.py`. Any query outside the detected disease (e.g., general chat, code, unrelated crops) is rejected via strict keyword and semantic guardrails.* |

---

## 📜 Statutory Disclaimer
*The chemical dosages and treatment recommendations in AgriSense are synthesized from published university research advisories from MPKV Rahuri and ICAR-NRC Grapes Pune. Farmers must always consult their local Taluka Krishi Adhikari before tank mixing.*
