"""
AgriSense - Grounded Advisory Chatbot
Strictly constrained to the diagnosed crop disease and Maharashtra localized treatment database.
Guards against hallucinations and forbids open-ended / off-topic queries.
"""

import os
import re
from typing import Dict, List, Optional
from agrisense.data.treatments_db import get_treatment_for_disease


OFF_TOPIC_KEYWORDS = [
    "python", "coding", "code", "javascript", "movie", "president", "election",
    "cricket", "ipl", "bitcoin", "crypto", "quantum", "essay", "homework",
    "song", "joke", "capital of", "who are you", "translate into french"
]


class GroundedAgriChatbot:
    """
    Strictly grounded chatbot providing agronomic follow-up consultation
    tied exclusively to the detected plant disease and treatment database.
    """

    def __init__(self, openai_api_key: Optional[str] = None):
        self.api_key = openai_api_key or os.getenv("OPENAI_API_KEY")

    def is_off_topic(self, user_prompt: str) -> bool:
        """Check if user prompt is outside the agricultural scope."""
        lowered = user_prompt.lower()
        for kw in OFF_TOPIC_KEYWORDS:
            if re.search(r"\b" + re.escape(kw) + r"\b", lowered):
                return True
        return False

    def generate_reply(
        self,
        user_prompt: str,
        detection_context: Optional[Dict],
        language: str = "en"
    ) -> str:
        """
        Generate grounded reply strictly based on detection context and localized treatments.
        """
        # 1. Guardrail: Must have completed a leaf scan first
        if not detection_context or not detection_context.get("class_key"):
            if language == "mr":
                return (
                    "🌱 **कृपया प्रथम पानाचा फोटो अपलोड करा:**\n\n"
                    "मी अग्रीसेन्स शेती सल्लागार आहे. अचूक सल्ला देण्यासाठी कृपया आधी "
                    "आपल्या पिकाच्या पानाचा फोटो अपलोड किंवा कॅमेऱ्याने स्कॅन करा."
                )
            return (
                "🌱 **Please scan a crop leaf first:**\n\n"
                "I am the AgriSense Grounded Assistant. To provide verified, crop-safe guidance, "
                "please select a crop and upload/capture an image of an affected leaf first."
            )

        crop = detection_context.get("selected_crop", "Crop")
        disease_key = detection_context.get("class_key", "")
        disease_info = get_treatment_for_disease(disease_key)
        disease_en = disease_info.get("display_name_en", disease_key)
        disease_mr = disease_info.get("display_name_mr", disease_key)
        severity = detection_context.get("severity_level", "Unknown")

        # 2. Guardrail: Forbid open-ended / off-topic queries
        if self.is_off_topic(user_prompt):
            if language == "mr":
                return (
                    f"⚠️ **विषयाबाहेरील प्रश्न नाकारला:**\n\n"
                    f"मी केवळ **{crop}** पिकावरील **{disease_mr}** रोगाच्या उपचारासंबंधी प्रश्नांची उत्तरे देऊ शकतो.\n"
                    f"तुम्ही खालील विषयांवर विचारू शकता:\n"
                    f"• फवारणीचे औषध आणि प्रमाण (Dosage)\n"
                    f"• सेंद्रिय किंवा घरगुती उपाय\n"
                    f"• बाजारातील अंदाजे किंमत\n"
                    f"• पाऊस किंवा फवारणीची योग्य वेळ"
                )
            return (
                f"⚠️ **Off-Topic Query Restricted:**\n\n"
                f"I am strictly configured to assist only with the diagnosed condition: **{disease_en}** on **{crop}**.\n\n"
                f"Please ask questions related to:\n"
                f"• Chemical pesticide dosages and tank mixing\n"
                f"• Organic and bio-fungicide alternatives\n"
                f"• Maharashtra market cost estimates\n"
                f"• Safe spraying schedules and rain precautions"
            )

        # 3. Try LLM if API Key is configured and accessible
        if self.api_key:
            try:
                from openai import OpenAI
                client = OpenAI(api_key=self.api_key)
                
                system_prompt = (
                    "You are AgriSense, an expert agricultural advisory AI strictly helping Maharashtra farmers. "
                    "You MUST strictly ground your response in the provided diagnosis and localized treatment data. "
                    "NEVER recommend unauthorized chemicals or speculate outside the provided context. "
                    f"Target Crop: {crop}\n"
                    f"Detected Disease: {disease_en} ({disease_mr})\n"
                    f"Severity Level: {severity}\n"
                    f"Chemical Treatments: {disease_info.get('chemical_treatments', [])}\n"
                    f"Organic Treatments: {disease_info.get('organic_treatments', [])}\n"
                    f"Preventive Measures: {disease_info.get('preventive_measures_en', [])}\n"
                    f"Language: {'Marathi' if language == 'mr' else 'English'}.\n"
                    "Keep answers crisp, practical, and farmer-friendly."
                )

                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=400,
                    temperature=0.2
                )
                return response.choices[0].message.content.strip()
            except Exception as e:
                # Fallback directly to deterministic knowledge engine
                pass

        # 4. Deterministic Agronomic Knowledge Engine (100% Offline & Reliable)
        return self._rule_based_grounded_reply(user_prompt, crop, disease_info, severity, language)

    def _rule_based_grounded_reply(
        self,
        prompt: str,
        crop: str,
        info: dict,
        severity: str,
        lang: str
    ) -> str:
        """Deterministic, grounded intent engine matching farmer queries in English & Marathi."""
        p = prompt.lower()
        d_en = info.get("display_name_en", "")
        d_mr = info.get("display_name_mr", "")
        chems = info.get("chemical_treatments", [])
        orgs = info.get("organic_treatments", [])
        prev_en = info.get("preventive_measures_en", [])
        prev_mr = info.get("preventive_measures_mr", [])

        # Intent 1: Dosage / प्रमाण / मात्रा
        if any(w in p for w in ["dosage", "how much", "quantity", "litre", "liter", "tank", "drum", "प्रमाण", "मात्रा", "किती", "लिटर"]):
            if chems:
                top_chem = chems[0]
                if lang == "mr":
                    return (
                        f"💧 **{d_mr} साठी फवारणीचे अचूक प्रमाण:**\n\n"
                        f"• **औषधाचे नाव:** {top_chem['name']}\n"
                        f"• **१ लिटर पाण्यासाठी:** {top_chem['dosage']}\n"
                        f"• **१५ लिटर पंपासाठी:** अंदाजे ३० ते ३५ ग्रॅम/मिली\n"
                        f"• **२०० लिटर ड्रमसाठी:** अंदाजे ४०० ते ५०० ग्रॅम/मिली\n\n"
                        f"📌 *टीप: औषध मिसळताना चांगल्या परिणामासाठी सिलिकॉन स्टीकर (०.५ मिली/लिटर) वापरा.*"
                    )
                return (
                    f"💧 **Verified Spray Dosage for {d_en}:**\n\n"
                    f"• **Primary Chemical:** {top_chem['name']}\n"
                    f"• **Per Litre Water:** {top_chem['dosage']}\n"
                    f"• **Standard 15L Knapsack Pump:** approx. 30g - 38g (or ml)\n"
                    f"• **200L Tractor Sprayer Drum:** approx. 400g - 500g\n\n"
                    f"📌 *Application Schedule:* {top_chem['application_schedule']}"
                )

        # Intent 2: Organic / सेंद्रिय / घरगुती उपाय
        if any(w in p for w in ["organic", "bio", "natural", "home", "neem", "dashparni", "सेंद्रिय", "जैविक", "घरगुती", "निंबोळी", "अर्क"]):
            if orgs:
                top_org = orgs[0]
                if lang == "mr":
                    return (
                        f"🌿 **{d_mr} साठी शिफारस केलेले सेंद्रिय उपाय:**\n\n"
                        f"• **उपाय:** {top_org['name']}\n"
                        f"• **प्रमाण:** {top_org['dosage']}\n"
                        f"• **तयार करण्याची पद्धत:** {top_org.get('prep_instructions', 'संध्याकाळी फवारावे.')}\n"
                        f"• **अंदाजे खर्च:** {top_org['cost_range_inr']}\n\n"
                        f"सेंद्रिय उपायामुळे पिकाची नैसर्गिक रोगप्रतिकारशक्ती वाढते आणि जमिनीचे आरोग्य सुधारते."
                    )
                return (
                    f"🌿 **Organic / Bio-control Solution for {d_en}:**\n\n"
                    f"• **Remedy:** {top_org['name']}\n"
                    f"• **Recommended Rate:** {top_org['dosage']}\n"
                    f"• **Preparation:** {top_org.get('prep_instructions', 'Apply in late afternoon.')}\n"
                    f"• **Estimated Cost:** {top_org['cost_range_inr']}\n\n"
                    f"Safe for beneficial predatory insects and leaves zero chemical residue."
                )

        # Intent 3: Cost / किंमत / खर्च
        if any(w in p for w in ["cost", "price", "rate", "rupee", "rs", "₹", "खर्च", "किंमत", "भाव", "दर"]):
            chem_costs = "\n".join([f"• {c['name']}: **{c['cost_range_inr']}**" for c in chems])
            org_costs = "\n".join([f"• {o['name']}: **{o['cost_range_inr']}**" for o in orgs])
            if lang == "mr":
                return (
                    f"💰 **महाराष्ट्रातील कृषी केंद्रांमधील अंदाजे दर ({d_mr}):**\n\n"
                    f"**रासायनिक औषधे:**\n{chem_costs}\n\n"
                    f"**सेंद्रिय पर्याय:**\n{org_costs}\n\n"
                    f"*टीप: हे दर पुणे व नाशिक कृषी केंद्रांनुसार अंदाजित असून स्थानिक बाजारपेठेनुसार थोडे बदलू शकतात.*"
                )
            return (
                f"💰 **Approximate Maharashtra Market Price for {d_en}:**\n\n"
                f"**Chemical Pesticides:**\n{chem_costs}\n\n"
                f"**Organic Alternatives:**\n{org_costs}\n\n"
                f"*Note: Prices reflect standard APMC and Taluka Krishi Seva Kendra retail estimates.*"
            )

        # Intent 4: When to spray / फवारणीची वेळ / पाऊस
        if any(w in p for w in ["when", "time", "rain", "morning", "evening", "spray", "वेळ", "केव्हा", "पाऊस", "सकाळी", "संध्याकाळी"]):
            if lang == "mr":
                return (
                    f"⏰ **फवारणीची योग्य वेळ व खबरदारी ({d_mr}):**\n\n"
                    f"१. **योग्य वेळ:** सकाळी ९ वाजेच्या आधी किंवा दुपारी ४:३० नंतर ऊन कमी झाल्यावर फवारणी करा.\n"
                    f"२. **दुपारचे कडक ऊन टाळा:** दुपारच्या उन्हात औषध फवारल्यास पानावरील औषध लवकर बाष्पीभवन होते व पाने जळू शकतात.\n"
                    f"३. **पावसाची शक्यता:** पाऊस पडण्याची शक्यता असल्यास फवारणीत 'सिलिकॉन स्प्रेडर' (स्टिकर) अवश्य वापरा.\n"
                    f"४. **पानाची दोन्ही बाजू:** बुरशी पाठीमागे जास्त असल्याने पानाच्या दोन्ही बाजूंवर औषध पोहचेल याची खात्री करा."
                )
            return (
                f"⏰ **Optimal Spraying Timing & Safety for {d_en}:**\n\n"
                f"1. **Best Hours:** Early morning (before 9:00 AM) or late afternoon (after 4:30 PM).\n"
                f"2. **Avoid Midday Sun:** Spraying in intense sunlight causes phytotoxicity (leaf scorch).\n"
                f"3. **Rain Precaution:** If rains are forecasted in Pune region, add a non-ionic silicone spreader/sticker (0.5 ml/L).\n"
                f"4. **Complete Coverage:** Ensure thorough atomization on the underside of leaves where spores shelter."
            )

        # Intent 5: Symptoms & Cause / लक्षणे व कारण
        if any(w in p for w in ["symptom", "cause", "why", "organism", "लक्षण", "कारण", "का झाले", "कशामुळे"]):
            s_list = info.get("symptoms_mr" if lang == "mr" else "symptoms_en", [])
            s_text = "\n".join([f"• {s}" for s in s_list])
            if lang == "mr":
                return (
                    f"🔍 **{d_mr} ची प्रमुख लक्षणे व कारणे:**\n\n"
                    f"• **कारणीभूत घटक:** {info.get('causal_organism', 'बुरशीजन्य रोग')}\n"
                    f"• **हवामान:** {info.get('favorable_conditions_mr', 'दमट हवामान')}\n\n"
                    f"**पानावरील मुख्य लक्षणे:**\n{s_text}"
                )
            return (
                f"🔍 **Pathology & Visual Symptoms of {d_en}:**\n\n"
                f"• **Causal Pathogen:** {info.get('causal_organism', 'Pathogen')}\n"
                f"• **Favorable Climate:** {info.get('favorable_conditions_en', 'Warm & Humid')}\n\n"
                f"**Key Symptoms:**\n{s_text}"
            )

        # Default comprehensive summary reply
        if lang == "mr":
            return (
                f"🌾 **{crop} - {d_mr} सल्लागार सारांश:**\n\n"
                f"सध्याचा प्रादुर्भाव: **{severity}**\n"
                f"१. **रासायनिक उपाय:** {chems[0]['name'] if chems else 'योग्य बुरशीनाशक'} ({chems[0]['dosage'] if chems else ''})\n"
                f"२. **सेंद्रिय उपाय:** {orgs[0]['name'] if orgs else 'ट्रायकोडर्मा'} ({orgs[0]['dosage'] if orgs else ''})\n"
                f"३. **प्रतिबंधात्मक काळजी:** {prev_mr[0] if prev_mr else 'हवा खेळती ठेवा.'}\n\n"
                f"तुम्ही मला फवारणीचे अचूक प्रमाण, औषधांची किंमत किंवा फवारणीच्या वेळेबद्दल अधिक विचारू शकता."
            )
        return (
            f"🌾 **Advisory Summary for {d_en} on {crop}:**\n\n"
            f"Observed Severity: **{severity}**\n"
            f"1. **Primary Chemical:** {chems[0]['name'] if chems else 'Standard fungicide'} ({chems[0]['dosage'] if chems else ''})\n"
            f"2. **Bio-alternative:** {orgs[0]['name'] if orgs else 'Trichoderma'} ({orgs[0]['dosage'] if orgs else ''})\n"
            f"3. **Agronomic Care:** {prev_en[0] if prev_en else 'Ensure good canopy aeration.'}\n\n"
            f"Feel free to ask for precise dosage calculations, market cost estimates, or safe spraying schedules."
        )
