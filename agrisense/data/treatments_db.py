"""
AgriSense - Localized Agricultural Treatment Database for Maharashtra Farmers
Region Focus: Pune, Nashik, Sangli, Kolhapur, Solapur, Ahmednagar Belts
Crops Supported: Grapes (द्राक्ष), Tomato (टोमॅटो), Soybean (सोयाबीन)
Data Sourced from: ICAR, MPKV Rahuri, NRC Grapes Pune, and Maharashtra Krishi Kendra Guidelines.
"""

TREATMENTS_DATABASE = {
    # =========================================================================
    # GRAPES (द्राक्ष)
    # =========================================================================
    "Grape___healthy": {
        "crop": "Grapes",
        "crop_mr": "द्राक्ष",
        "display_name_en": "Healthy Grape Leaf",
        "display_name_mr": "निरोगी द्राक्ष पान",
        "causal_organism": "None (Healthy)",
        "pathogen_type": "None",
        "description_en": "The grape canopy exhibits robust vegetative vigor with no visible fungal or bacterial sporulation.",
        "description_mr": "द्राक्षाचे पान पूर्णपणे निरोगी आणि तजेलदार असून पानावर कोणताही बुरशीजन्य किंवा जिवाणूजन्य रोग आढळलेला नाही.",
        "symptoms_en": [
            "Uniform emerald green foliage",
            "No necrotic lesions, yellow halos, or powdery sporulation",
            "Healthy venation and normal leaf margins"
        ],
        "symptoms_mr": [
            "तजेलदार हिरवेगार पान",
            "पानांवर कोणतेही काळे, पिवळे किंवा तपकिरी डाग नाहीत",
            "पानाची रचना व नसा पूर्णपणे निरोगी"
        ],
        "favorable_conditions_en": "Optimal sunlight, balanced drip fertigation, and good canopy airflow.",
        "favorable_conditions_mr": "योग्य सूर्यप्रकाश, संतुलित खत व्यवस्थापन आणि मांडवामध्ये खेळती हवा.",
        "chemical_treatments": [
            {
                "name": "Prophylactic Micronutrient Foliar Spray (Zinc + Boron + Magnesium)",
                "dosage": "1.5 g - 2.0 g per litre of water",
                "application_schedule": "Spray every 15-20 days during active canopy expansion.",
                "phi_days": 0,
                "cost_range_inr": "₹180 - ₹320 per 500g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Cold-pressed Neem Oil (10,000 PPM) + Cow Urine Dilution",
                "dosage": "2.0 ml Neem Oil + 10 ml Cow Urine per litre of water",
                "cost_range_inr": "₹150 - ₹250 per litre",
                "prep_instructions": "Spray during early morning or late evening to build systemic plant immunity."
            }
        ],
        "preventive_measures_en": [
            "Maintain trellis canopy training to ensure 360-degree sunlight penetration",
            "Avoid over-application of nitrogenous fertilizers which attract sucking pests",
            "Conduct routine scouting after post-monsoon cane pruning"
        ],
        "preventive_measures_mr": [
            "मांडवामध्ये सूर्यप्रकाश व हवा खेळती राहण्यासाठी छाटणी वेळेवर करा",
            "अतिरिक्त युरिया/नायट्रोजनचा वापर टाळा",
            "छाटणीनंतर बागेची नियमित पाहणी करा"
        ],
        "maharashtra_zone_notes": "Ideal condition observed in Nashik (Dindori/Niphad) and Pune (Narayangaon/Baramati) well-managed vineyards.",
        "disclaimer": "Continue prophylactic bio-pesticide spray schedule during overcast monsoon days."
    },

    "Grape___Downy_mildew": {
        "crop": "Grapes",
        "crop_mr": "द्राक्ष",
        "display_name_en": "Grape Downy Mildew (Kewada)",
        "display_name_mr": "द्राक्षावरील केवडा / डाउनी मिल्ड्यू",
        "causal_organism": "Plasmopara viticola (Oomycete)",
        "pathogen_type": "Fungal/Oomycete",
        "description_en": "The most destructive grape disease in Maharashtra during monsoon and cloudy weather. Attacks leaves, tendrils, and emerging grape bunches.",
        "description_mr": "महाराष्ट्रातील द्राक्ष बागायतदारांसाठी अत्यंत घातक रोग. ढगाळ व दमट हवामानात पानांवर तेलकट डाग पडून पाठीमागे पांढरी बुरशी येते.",
        "symptoms_en": [
            "Translucent, oily 'oil spots' (yellowish) on upper leaf surface",
            "Dense white, downy cottony fungal growth on the underside of leaves",
            "Infected tissue turns brown, necrotic, and drops prematurely (scorched leaf appearance)"
        ],
        "symptoms_mr": [
            "पानाच्या वरच्या बाजूला पिवळसर तेलकट डाग दिसतात",
            "पानाच्या खालच्या बाजूला पांढुरकी कापसासारखी बुरशी वाढते",
            "गंभीर अवस्थेत पाने जळून वाळल्यासारखी होतात व पानगळ होते"
        ],
        "favorable_conditions_en": "Relative humidity > 80%, continuous drizzle, night temperature 18-24°C, and leaf wetness for 4+ hours.",
        "favorable_conditions_mr": "हवेतील आर्द्रता ८०% पेक्षा जास्त, सततची रिमझिम आणि रात्रीचे तापमान १८-२४ अंश सेल्सिअस.",
        "chemical_treatments": [
            {
                "name": "Ridomil Gold (Metalaxyl-M 4% + Mancozeb 64% WP)",
                "dosage": "2.5 g per litre of water (500 g per 200 L drum)",
                "application_schedule": "Curative spray within 48 hours of rain or first lesion appearance.",
                "phi_days": 40,
                "cost_range_inr": "₹450 - ₹620 per 500g"
            },
            {
                "name": "Profiler (Fluopicolide 4.44% + Fosetyl-Al 66.67% WG)",
                "dosage": "2.5 g per litre of water",
                "application_schedule": "Systemic protective spray during high humidity warnings.",
                "phi_days": 45,
                "cost_range_inr": "₹850 - ₹1,150 per 500g"
            },
            {
                "name": "Aliette (Fosetyl-Al 80% WP)",
                "dosage": "2.0 g per litre of water",
                "application_schedule": "Spray during shoot elongation stage.",
                "phi_days": 35,
                "cost_range_inr": "₹420 - ₹580 per 250g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Bordeaux Mixture (1% Neutral Solution) / बोर्डो मिश्रण",
                "dosage": "1 kg Copper Sulphate + 1 kg Quicklime in 100 litres of water",
                "cost_range_inr": "₹160 - ₹220 per 100 L prep",
                "prep_instructions": "Prepare freshly in plastic/earthen container. Test neutral pH using iron knife before spraying."
            },
            {
                "name": "Trichoderma viride / harzianum Liquid Bio-fungicide",
                "dosage": "5.0 ml per litre of water",
                "cost_range_inr": "₹180 - ₹280 per litre",
                "prep_instructions": "Apply in late afternoon when UV radiation is minimal to colonize leaf surface."
            }
        ],
        "preventive_measures_en": [
            "Prune lower trailing shoots touching the moist soil",
            "Keep canopy open to reduce microclimatic leaf wetness",
            "Spray prophylactic contact fungicide (Mancozeb @ 2g/L) prior to anticipated rainfall"
        ],
        "preventive_measures_mr": [
            "जमिनीला टेकणाऱ्या वेलींच्या काड्या छाटून टाका",
            "हवा खेळती राहण्यासाठी बागेत गर्दी होणार नाही याची काळजी घ्या",
            "पाऊस पडण्यापूर्वी प्रतिबंधात्मक बोर्डो किंवा मॅन्कोझेबची फवारणी करा"
        ],
        "maharashtra_zone_notes": "High alert in Junnar, Narayangaon, Niphad, and Sangli belts during July to October.",
        "disclaimer": "Do not spray systemic fungicides with the same mode of action repeatedly to prevent chemical resistance."
    },

    "Grape___Powdery_mildew": {
        "crop": "Grapes",
        "crop_mr": "द्राक्ष",
        "display_name_en": "Grape Powdery Mildew (Bhuri)",
        "display_name_mr": "द्राक्षावरील भुरी / पावडरी मिल्ड्यू",
        "causal_organism": "Erysiphe necator (Uncinula necator)",
        "pathogen_type": "Fungal",
        "description_en": "Common dry-weather fungal disease affecting grape berries, foliage, and canes in western Maharashtra vineyards.",
        "description_mr": "महाराष्ट्रात ऑक्टोबर छाटणीनंतर कोरड्या व थंड हवामानात येणारा प्रमुख बुरशीजन्य रोग. पानांवर पांढरी भुकटी जमा होते.",
        "symptoms_en": [
            "White to ash-grey powdery patches on both leaf surfaces and young shoots",
            "Leaves curl upwards and exhibit crisp, crinkled margins",
            "Berries crack, harden, and fail to mature if infected early"
        ],
        "symptoms_mr": [
            "पानांवर व कोवळ्या फुटींवर राखाडी-पांढऱ्या रंगाची पावडर किंवा भुकटी दिसते",
            "पानांच्या कडा वरच्या बाजूला वाकतात आणि वाळतात",
            "घडावर प्रादुर्भाव झाल्यास मण्यांना तडे जातात आणि मणी कडक होतात"
        ],
        "favorable_conditions_en": "Temperature 22-30°C, moderate humidity (50-70%), dry cloudy days, and dense unpruned shade.",
        "favorable_conditions_mr": "तापमान २२-३० अंश सेल्सिअस, मध्यम आर्द्रता (५०-७०%) आणि दाट पानांची सावली.",
        "chemical_treatments": [
            {
                "name": "Nativo (Tebuconazole 50% + Trifloxystrobin 25% WG)",
                "dosage": "0.6 g per litre of water (120 g per 200 L water)",
                "application_schedule": "Spray at pre-bloom and fruit set stage.",
                "phi_days": 35,
                "cost_range_inr": "₹750 - ₹1,050 per 100g"
            },
            {
                "name": "Topas (Penconazole 10% EC)",
                "dosage": "0.5 ml per litre of water",
                "application_schedule": "Curative spray upon first sign of powdery talc on leaves.",
                "phi_days": 30,
                "cost_range_inr": "₹480 - ₹650 per 100ml"
            },
            {
                "name": "Wettable Sulphur 80% WP (Sulfex)",
                "dosage": "2.0 - 2.5 g per litre of water",
                "application_schedule": "Prophylactic spray during cane development.",
                "phi_days": 15,
                "cost_range_inr": "₹120 - ₹180 per 1 kg"
            }
        ],
        "organic_treatments": [
            {
                "name": "Potassium Bicarbonate + Horticultural Oil Solution",
                "dosage": "4.0 g Potassium Bicarbonate + 2 ml oil per litre water",
                "cost_range_inr": "₹220 - ₹350 per kg",
                "prep_instructions": "Changes leaf surface pH rapidly, desiccating powdery mildew spores instantly."
            },
            {
                "name": "Ampelomyces quisqualis Bio-agent (Hyperparasite fungus)",
                "dosage": "5.0 g per litre of water",
                "cost_range_inr": "₹250 - ₹400 per 500g",
                "prep_instructions": "Natural biocontrol organism that parasitizes and kills powdery mildew."
            }
        ],
        "preventive_measures_en": [
            "Thin out shoots and leaves around grape clusters to ensure sunlight exposure",
            "Avoid spraying wettable sulphur when ambient temperatures exceed 34°C to prevent leaf scorching",
            "Dust agricultural sulfur early morning when dew is present"
        ],
        "preventive_measures_mr": [
            "घडाच्या भोवतालची पाने काढून मण्यांवर सूर्यप्रकाश पडू द्या",
            "तापमान ३४ अंश सेल्सिअसपेक्षा जास्त असल्यास गंधकाची फवारणी टाळा (पाने जळू शकतात)",
            "सकाळी दव असताना गंधकाची धुरळणी फायदेशीर ठरते"
        ],
        "maharashtra_zone_notes": "Prominent throughout Baramati, Indapur, Tasgaon, and Niphad during November - February.",
        "disclaimer": "Ensure protective eyewear while applying sulphur or triazole formulations."
    },

    "Grape___Black_rot": {
        "crop": "Grapes",
        "crop_mr": "द्राक्ष",
        "display_name_en": "Grape Black Rot (Kala Kujwa)",
        "display_name_mr": "द्राक्षावरील काळा कुजवा / ब्लॅक रॉट",
        "causal_organism": "Guignardia bidwellii",
        "pathogen_type": "Fungal",
        "description_en": "Causes leaf spotting and devastating fruit mummification in grape vineyards during warm wet spells.",
        "description_mr": "पानांवर तपकिरी-काळे ठिपके पडतात आणि द्राक्षाचे मणी सुकवून काळे ममीसारखे बनवणारा बुरशीजन्य रोग.",
        "symptoms_en": [
            "Small circular reddish-brown leaf spots with dark margins and tiny black dots (pycnidia)",
            "Elongated dark cankers on shoots and leaf petioles",
            "Berries shrivel into hard, black wrinkled 'mummies'"
        ],
        "symptoms_mr": [
            "पानांवर लालसर-तपकिरी रंगाचे गोलाकार डाग ज्याभोवती काळी कडा असते",
            "डागांच्या मध्यभागी लहान काळे दाणे (फळधारणा अवयव) दिसतात",
            "फळावर प्रादुर्भाव झाल्यास मणी सुरकुतून काळे दगडी बनतात"
        ],
        "favorable_conditions_en": "Warm rain, temperatures 24-28°C, and prolonged humidity.",
        "favorable_conditions_mr": "उबदार पाऊस, २४-२८ अंश सेल्सिअस तापमान आणि सतत ओलसर हवामान.",
        "chemical_treatments": [
            {
                "name": "Score (Difenoconazole 25% EC)",
                "dosage": "0.5 ml per litre of water (100 ml per 200 L drum)",
                "application_schedule": "Apply at bud-break and repeat 14 days later.",
                "phi_days": 30,
                "cost_range_inr": "₹550 - ₹780 per 100ml"
            },
            {
                "name": "Dithane M-45 (Mancozeb 75% WP)",
                "dosage": "2.5 g per litre of water",
                "application_schedule": "Protective spray during initial leafing.",
                "phi_days": 21,
                "cost_range_inr": "₹280 - ₹380 per 500g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Copper Oxychloride 50% WP (Blitox)",
                "dosage": "2.5 g per litre of water",
                "cost_range_inr": "₹260 - ₹380 per 500g",
                "prep_instructions": "Broad-spectrum contact protective spray; coat both leaf surfaces thoroughly."
            }
        ],
        "preventive_measures_en": [
            "Collect and burn all mummified berries and infected canes from previous season",
            "Prune dead wood during sub-cane pruning",
            "Ensure proper drainage to avoid root stagnation"
        ],
        "preventive_measures_mr": [
            "मागील हंगामातील वाळलेले काळे मणी गोळा करून नष्ट करा",
            "छाटणी करताना रोगट काड्या काढून टाका",
            "बागेमध्ये पाण्याचा योग्य निचरा ठेवा"
        ],
        "maharashtra_zone_notes": "Frequently observed in older vineyards in Solapur, Sangli, and Pune districts.",
        "disclaimer": "Avoid tank mixing copper with acidic foliar fertilizers."
    },

    # =========================================================================
    # TOMATO (टोमॅटो)
    # =========================================================================
    "Tomato___healthy": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Healthy Tomato Leaf",
        "display_name_mr": "निरोगी टोमॅटो पान",
        "causal_organism": "None (Healthy)",
        "pathogen_type": "None",
        "description_en": "Vibrant, green compound foliage free of fungal leaf blight, bacterial spots, or viral curling.",
        "description_mr": "टोमॅटोचे पान पूर्णपणे निरोगी, हिरवेगार असून पानावर कोणताही करपा किंवा विषाणूजन्य चुरडा-मुरडा नाही.",
        "symptoms_en": [
            "Dark green serrated leaflets",
            "Crisp turgid leaf texture without wilting",
            "No chlorosis (yellowing) or necrotic rings"
        ],
        "symptoms_mr": [
            "गडद हिरवेगार तजेलदार पान",
            "पानावर कोणत्याही प्रकारचे पिवळे किंवा काळे डाग नाहीत",
            "पान चुरडलेले किंवा वाळलेले नाही"
        ],
        "favorable_conditions_en": "Balanced drip nutrition, well-drained sandy loam soil, and warm sunshine.",
        "favorable_conditions_mr": "संतुलित ठिबक खते, उत्तम निचऱ्याची जमीन आणि योग्य सूर्यप्रकाश.",
        "chemical_treatments": [
            {
                "name": "Preventive 19:19:19 NPK + Chelated Micronutrients",
                "dosage": "3.0 - 4.0 g per litre of water",
                "application_schedule": "Foliar feed every 12-14 days to boost plant vigor.",
                "phi_days": 0,
                "cost_range_inr": "₹150 - ₹240 per 1 kg"
            }
        ],
        "organic_treatments": [
            {
                "name": "Jeev Amrut / Panchagavya Foliar Spray",
                "dosage": "30 ml per litre of water (3% solution)",
                "cost_range_inr": "₹60 - ₹120 per litre",
                "prep_instructions": "Spray every 15 days to encourage beneficial phyllosphere microflora."
            }
        ],
        "preventive_measures_en": [
            "Stake tomato vines with trellising wire/bamboo to keep foliage off bare wet soil",
            "Maintain drip irrigation rather than overhead sprinkler watering",
            "Mulch beds with silver-black mulch to prevent soil splashing"
        ],
        "preventive_measures_mr": [
            "टोमॅटोच्या झाडांना बांबू व सुतळीच्या साहाय्याने आधार (स्टेकिंग) द्या",
            "पानांवर पाणी उडणार नाही याची काळजी घ्या, ठिबक सिंचन वापरा",
            "मल्चिंग पेपरचा वापर करा ज्यामुळे जमिनीतील बुरशी पानांवर उडत नाही"
        ],
        "maharashtra_zone_notes": "Typical for high-tech polyhouses and staked open-field plots in Junnar and Narayangaon.",
        "disclaimer": "Continue scouting for thrips and whiteflies which vector tomato leaf curl virus."
    },

    "Tomato___Early_blight": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Early Blight (Karpa)",
        "display_name_mr": "टोमॅटो करपा / अर्ली ब्लाइट",
        "causal_organism": "Alternaria solani",
        "pathogen_type": "Fungal",
        "description_en": "Widespread fungal disease in Maharashtra tomato fields causing distinctive concentric 'target board' lesions on older leaves.",
        "description_mr": "महाराष्ट्रातील टोमॅटो पिकावरील अत्यंत सामान्य रोग. खालच्या जुन्या पानांवर गोलाकार वळ्यांसारखे (टार्गेट बोर्ड) डाग पडतात.",
        "symptoms_en": [
            "Brown-black circular lesions with concentric rings resembling a target board",
            "Yellow halo (chlorotic ring) surrounding each lesion",
            "Older lower leaves infected first, gradually progressing upwards causing complete defoliation"
        ],
        "symptoms_mr": [
            "पानांवर एकाआड एक गोलाकार कडे असलेले तपकिरी-काळे डाग (टार्गेट बोर्डसारखे)",
            "डागांच्या भोवती पिवळसर कडा तयार होते",
            "सुरुवातीला झाडाच्या खालच्या पानांवर प्रादुर्भाव होतो व नंतर वरची पाने करपतात"
        ],
        "favorable_conditions_en": "Alternating dry and humid spells, temperature 24-30°C, and heavy morning dew.",
        "favorable_conditions_mr": "उष्ण आणि दमट हवामान, २४-३० अंश सेल्सिअस तापमान आणि सकाळी पडणारे दाट दव.",
        "chemical_treatments": [
            {
                "name": "Kavach (Chlorothalonil 75% WP)",
                "dosage": "2.0 g per litre of water (400 g per 200 L water)",
                "application_schedule": "Spray immediately upon noticing target spots on lower foliage.",
                "phi_days": 7,
                "cost_range_inr": "₹420 - ₹580 per 500g"
            },
            {
                "name": "Amistar Top (Azoxystrobin 18.2% + Difenoconazole 11.4% SC)",
                "dosage": "1.0 ml per litre of water",
                "application_schedule": "Curative systemic spray for fast arresting of fungal mycelia.",
                "phi_days": 5,
                "cost_range_inr": "₹720 - ₹950 per 200ml"
            },
            {
                "name": "Antracol (Propineb 70% WP)",
                "dosage": "2.5 g per litre of water",
                "application_schedule": "Protective contact spray containing zinc nutrition.",
                "phi_days": 10,
                "cost_range_inr": "₹320 - ₹460 per 500g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Trichoderma harzianum Bio-fungicide",
                "dosage": "5.0 g per litre of water",
                "cost_range_inr": "₹160 - ₹240 per 1 kg",
                "prep_instructions": "Mix with 2 g jaggery in water, keep for 2 hours and spray thoroughly on canopy."
            },
            {
                "name": "Dashparni Ark (दशपर्णी अर्क)",
                "dosage": "25 ml per litre of water",
                "cost_range_inr": "₹80 - ₹140 per litre",
                "prep_instructions": "Organic botanical concoction prepared with neem, karanj, and calotropis leaves."
            }
        ],
        "preventive_measures_en": [
            "Prune and discard the bottom 12 inches of foliage touching ground",
            "Practice 3-year crop rotation with non-solanaceous crops (maize, marigold, legumes)",
            "Disinfect pruning scissors and stakes with 1% sodium hypochlorite"
        ],
        "preventive_measures_mr": [
            "जमिनीलगतची खालची १ फूट उंचीपर्यंतची जुनी पाने छाटून टाका",
            "टोमॅटोनंतर वांगी किंवा बटाटा न घेता मका किंवा झेंडूची फेरपालट करा",
            "रोगट पाने शेताबाहेर नेऊन जमिनीत गाडून टाका"
        ],
        "maharashtra_zone_notes": "Extremely prevalent across Khed, Manchar, Narayangaon, and Sangamner during kharif and rabi seasons.",
        "disclaimer": "Observe strict 5-7 days pre-harvest waiting interval before harvesting tomato fruit for local APMC markets."
    },

    "Tomato___Late_blight": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Late Blight (Ushira Yenaara Karpa)",
        "display_name_mr": "टोमॅटो उशिरा येणारा करपा / लेट ब्लाइट",
        "causal_organism": "Phytophthora infestans",
        "pathogen_type": "Fungal/Oomycete",
        "description_en": "Highly destructive rapid epidemic disease. Can scorch and destroy an entire tomato acre within 72 hours in continuous rain.",
        "description_mr": "अतिशय वेगाने पसरणारा विध्वंसक रोग. ढगाळ व पावसाळी हवामानात ३ ते ४ दिवसांत संपूर्ण टोमॅटोचे पीक जाळून नष्ट करतो.",
        "symptoms_en": [
            "Large irregular water-soaked dark lesions appearing greasy on leaf tips",
            "Delicate white fuzzy fungal mildew on leaf undersides under high humidity",
            "Stems develop dark brown-black lesions, collapse, and plant gives rotten odor"
        ],
        "symptoms_mr": [
            "पानांच्या टोकांवर पाणी शोषल्यासारखे काळे-तपकिरी ओले डाग पडतात",
            "दमट हवेमध्ये डागांच्या खालच्या बाजूला पांढरी बुरशी वाढते",
            "फांद्या काळ्या पडून वाळतात आणि संपूर्ण झाड होरपळल्यासारखे दिसते"
        ],
        "favorable_conditions_en": "Continuous overcast skies, cool temperature (15-22°C), high humidity (> 85%), and driving rain.",
        "favorable_conditions_mr": "सतत ढगाळ हवामान, थंड वारे, १५-२२ अंश तापमान आणि हवेतील आर्द्रता ८५% पेक्षा जास्त.",
        "chemical_treatments": [
            {
                "name": "Curzate (Cymoxanil 8% + Mancozeb 64% WP)",
                "dosage": "2.0 g per litre of water",
                "application_schedule": "Apply immediately upon overcast rainy weather forecast.",
                "phi_days": 10,
                "cost_range_inr": "₹480 - ₹680 per 500g"
            },
            {
                "name": "Acrobat (Dimethomorph 50% WP)",
                "dosage": "1.5 g per litre of water mixed with Mancozeb 2.0 g/L",
                "application_schedule": "Translaminar curative action against sporulating oospores.",
                "phi_days": 14,
                "cost_range_inr": "₹650 - ₹890 per 200g"
            },
            {
                "name": "Sectin (Fenamidone 10% + Mancozeb 50% WG)",
                "dosage": "2.5 g per litre of water",
                "application_schedule": "Emergency knockdown spray during continuous rain breaks.",
                "phi_days": 7,
                "cost_range_inr": "₹550 - ₹750 per 300g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Copper Hydroxide 53.8% DF (Kocide 2000)",
                "dosage": "2.0 g per litre of water",
                "cost_range_inr": "₹380 - ₹520 per 500g",
                "prep_instructions": "Premium micronized copper barrier spray providing persistent rain-fast protection."
            },
            {
                "name": "Pseudomonas fluorescens 1% WP (Bio-bactericide & Fungicide)",
                "dosage": "5.0 g per litre of water",
                "cost_range_inr": "₹150 - ₹220 per kg",
                "prep_instructions": "Foliar colonization to outcompete water mold zoospores."
            }
        ],
        "preventive_measures_en": [
            "Never allow standing water in furrows; ensure rapid trench drainage",
            "Avoid overhead spray irrigation in afternoon or evening",
            "Burn infected residues immediately; do not compost blighted haulms"
        ],
        "preventive_measures_mr": [
            "वाफ्यांमध्ये पाणी साचू देऊ नका, पाण्याचा तात्काळ निचरा करा",
            "संध्याकाळच्या वेळी झाडावर पाणी फवारणे टाळा",
            "रोगट झाडे त्वरित उपटून नष्ट करा, उकिरड्यावर टाकू नका"
        ],
        "maharashtra_zone_notes": "High emergency alert in Pune (Junnar/Ambegaon) and Satara (Wai/Koregaon) during August and September.",
        "disclaimer": "Emergency spray must be completed before rain sets in. Use spreading sticker (silicone spreader @ 0.5ml/L)."
    },

    "Tomato___Bacterial_spot": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Bacterial Spot (Jivanujanya Thipke)",
        "display_name_mr": "टोमॅटो जिवाणूजन्य ठिपके / बॅक्टेरियल स्पॉट",
        "causal_organism": "Xanthomonas perforans / euvesicatoria",
        "pathogen_type": "Bacterial",
        "description_en": "Seed-borne and rain-splashed bacterial infection attacking foliage, stems, and unripened green tomatoes.",
        "description_mr": "पावसाच्या पाण्याने पसरणारा जिवाणूजन्य रोग. पानांवर लहान तेलकट काळे ठिपके पडतात आणि पाने गळतात.",
        "symptoms_en": [
            "Small (2-3 mm) dark brown-black greasy water-soaked spots on leaves",
            "Lesions develop a prominent translucent yellow halo",
            "Spots may tear or fall out, giving leaves a ragged shot-hole appearance"
        ],
        "symptoms_mr": [
            "पानांवर २-३ मिमी आकाराचे लहान काळे-तपकिरी तेलकट ठिपके दिसतात",
            "ठिपक्यांभोवती पिवळसर वर्तुळ दिसते",
            "गंभीर अवस्थेत ठिपके वाळून गळतात व पानावरील छिद्रांसारखे दिसतात"
        ],
        "favorable_conditions_en": "Warm temperatures (25-32°C), driving wind-blown rain, overhead irrigation, and sand injury.",
        "favorable_conditions_mr": "उष्ण आणि दमट हवामान, २५-३२ अंश तापमान आणि सोसाट्याचा पाऊस.",
        "chemical_treatments": [
            {
                "name": "Streptocycline (Streptomycin Sulphate 90% + Tetracycline 10%)",
                "dosage": "1.0 g per 10 litres of water (20 g per 200 L water tank)",
                "application_schedule": "Tank mix always with Copper Oxychloride (25 g per 10 L water).",
                "phi_days": 15,
                "cost_range_inr": "₹80 - ₹120 per 6g pouch"
            },
            {
                "name": "Blitox 50 (Copper Oxychloride 50% WP)",
                "dosage": "2.5 g per litre of water",
                "application_schedule": "Bactericidal copper barrier spray applied every 7-10 days.",
                "phi_days": 10,
                "cost_range_inr": "₹280 - ₹380 per 500g"
            },
            {
                "name": "Kasugamycin 3% SL (Kasu-B)",
                "dosage": "2.0 ml per litre of water",
                "application_schedule": "Systemic antibiotic spray for severe bacterial flaring.",
                "phi_days": 12,
                "cost_range_inr": "₹450 - ₹620 per 250ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Pseudomonas fluorescens + Bacillus subtilis Consortium",
                "dosage": "5.0 g per litre of water",
                "cost_range_inr": "₹180 - ₹260 per kg",
                "prep_instructions": "Produces competitive bactericidal lipopeptides that eliminate Xanthomonas."
            },
            {
                "name": "Sour Buttermilk (ताक) Spray",
                "dosage": "50 ml sour churned buttermilk per litre of water",
                "cost_range_inr": "₹20 - ₹40 per litre",
                "prep_instructions": "Lactic acid bacteria suppress foliar bacterial pathogens effectively."
            }
        ],
        "preventive_measures_en": [
            "Use certified pathogen-free treated nursery seeds or drench seedlings with Trichoderma",
            "Avoid handling or weeding wet tomato foliage to prevent mechanical bacterial dissemination",
            "Dip stakes in copper solution before re-staking beds"
        ],
        "preventive_measures_mr": [
            "रोपवाटिकेतून आणलेली रोपे ट्रायकोडर्मामध्ये बुडवून लावा",
            "झाडाची पाने ओली असताना शेतात काम किंवा निंदणी करणे टाळा",
            "बांबूच्या काठ्या निर्जंतुक करून पुन्हा वापरा"
        ],
        "maharashtra_zone_notes": "Common in Pune, Ahmednagar, and Nashik tomato nurseries and during post-transplanting rains.",
        "disclaimer": "Do not overdose Streptocycline; strictly observe prescribed 1g/10L dosage to avoid plant stunting."
    },

    # =========================================================================
    # SOYBEAN (सोयाबीन)
    # =========================================================================
    "Soybean___healthy": {
        "crop": "Soybean",
        "crop_mr": "सोयाबीन",
        "display_name_en": "Healthy Soybean Leaf",
        "display_name_mr": "निरोगी सोयाबीन पान",
        "causal_organism": "None (Healthy)",
        "pathogen_type": "None",
        "description_en": "Healthy trifoliate soybean leaves with clear chlorophyll pigmentation, robust nodulation, and pod development.",
        "description_mr": "सोयाबीनचे पान पूर्णपणे निरोगी, हिरवेगार असून पानावर तांबेरा किंवा करप्याचे कोणतेही डाग नाहीत.",
        "symptoms_en": [
            "Intact green trifoliate leaflets",
            "Strong petiole support and no leaf chlorosis",
            "No rust pustules or bacterial streaks"
        ],
        "symptoms_mr": [
            "हिरवेगार तजेलदार तिहेरी पान",
            "पानांवर कोणत्याही प्रकारचे तांबूस किंवा काळे डाग नाहीत",
            "पाने सुकलेली किंवा गळलेली नाहीत"
        ],
        "favorable_conditions_en": "Adequate soil moisture, rhizobium-inoculated root system, and sunny weather.",
        "favorable_conditions_mr": "जमिनीत योग्य ओलावा, जिवाणू खतांची बीजप्रक्रिया आणि अनुकूल सूर्यप्रकाश.",
        "chemical_treatments": [
            {
                "name": "00:52:34 (Monopotassium Phosphate) + Boron Foliar Spray",
                "dosage": "5.0 g per litre of water",
                "application_schedule": "Apply at flowering and pod filling stage for high yield.",
                "phi_days": 0,
                "cost_range_inr": "₹160 - ₹240 per 1 kg"
            }
        ],
        "organic_treatments": [
            {
                "name": "Neem Seed Kernel Extract (NSKE 5%) / निंबोळी अर्क",
                "dosage": "50 ml per litre of water",
                "cost_range_inr": "₹60 - ₹120 per litre prep",
                "prep_instructions": "Provides natural repellent barrier against spodoptera defoliators and sucking vectors."
            }
        ],
        "preventive_measures_en": [
            "Treat seed before sowing with Rhizobium and PSB culture @ 250g per 10kg seed",
            "Maintain 45 cm x 5 cm row spacing to ensure field ventilation",
            "Install yellow sticky traps (10 per acre) for sucking pest management"
        ],
        "preventive_measures_mr": [
            "पेरणीपूर्वी रायझोबियम व पीएसबी जिवाणू संवर्धकाची बीजप्रक्रिया करा",
            "दोन ओळींत ४५ सेंमी अंतर ठेवा जेणेकरून शेतात हवा खेळती राहील",
            "किडींच्या नियंत्रणासाठी एकरी १० पिवळे चिकट सापळे लावा"
        ],
        "maharashtra_zone_notes": "Benchmark condition for prime soybean fields in Kolhapur, Sangli, Latur, and Pune plains.",
        "disclaimer": "Regularly monitor underside of lower leaves during pod development stage."
    },

    "Soybean___Rust": {
        "crop": "Soybean",
        "crop_mr": "सोयाबीन",
        "display_name_en": "Soybean Rust (Tambera)",
        "display_name_mr": "सोयाबीन तांबेरा / रस्ट",
        "causal_organism": "Phakopsora pachyrhizi",
        "pathogen_type": "Fungal",
        "description_en": "The most catastrophic foliar disease for Maharashtra soybean farmers. Spores travel on wind and cause total premature leaf drop.",
        "description_mr": "महाराष्ट्रातील सोयाबीनचे सर्वात जास्त नुकसान करणारा रोग. पानाच्या पाठीमागे तांबूस रंगाचे लहान पुरळ येतात व झाड वाळून जाते.",
        "symptoms_en": [
            "Tiny pinhead-sized raised brown/reddish pustules (uredinia) on the underside of lower leaves",
            "Foliage appears rusty brown or bronzed when viewed across the field",
            "Rapid defoliation leading to unfilled, shriveled pods and up to 80% yield collapse"
        ],
        "symptoms_mr": [
            "पानांच्या खालच्या बाजूला सुईच्या टोकासारखे तांबूस-तपकिरी रंगाचे बारीक फोड (पुरळ) येतात",
            "संपूर्ण शेतात पीक तांबूस-पिवळे किंवा गंजल्यासारखे दिसते",
            "तीव्र प्रादुर्भावात पाने गळून पडतात, शेंगा भरत नाहीत व उत्पादनात ८०% पर्यंत घट होते"
        ],
        "favorable_conditions_en": "Frequent monsoon showers, temperature 18-28°C, relative humidity > 80%, and continuous cloudiness.",
        "favorable_conditions_mr": "सततचा पाऊस, हवेतील आर्द्रता ८०% पेक्षा जास्त, १८-२८ अंश तापमान आणि ढगाळ हवामान.",
        "chemical_treatments": [
            {
                "name": "Contaf (Hexaconazole 5% EC)",
                "dosage": "1.0 - 1.25 ml per litre of water (200 - 250 ml per 200 L water/acre)",
                "application_schedule": "Spray immediately upon first notification of rust spores in the taluka.",
                "phi_days": 30,
                "cost_range_inr": "₹280 - ₹420 per 250ml"
            },
            {
                "name": "Tilt (Propiconazole 25% EC)",
                "dosage": "1.0 ml per litre of water",
                "application_schedule": "Systemic triazole fungicide with powerful curative anti-sporulation effect.",
                "phi_days": 30,
                "cost_range_inr": "₹450 - ₹620 per 250ml"
            },
            {
                "name": "Folicur (Tebuconazole 25.9% m/m EC)",
                "dosage": "1.25 ml per litre of water",
                "application_schedule": "Highly effective preventative and early-curative spray.",
                "phi_days": 30,
                "cost_range_inr": "₹520 - ₹750 per 250ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Trichoderma viride Liquid Formulation",
                "dosage": "5.0 ml per litre of water",
                "cost_range_inr": "₹160 - ₹250 per litre",
                "prep_instructions": "Spray in early evening on lower leaves to establish biological antagonism."
            },
            {
                "name": "Dashparni Ark + Hing (Asafoetida) Solution",
                "dosage": "25 ml Dashparni Ark + 1 g Hing per litre water",
                "cost_range_inr": "₹100 - ₹180 per acre prep",
                "prep_instructions": "Traditional bioprotective concoction used in organic farming clusters."
            }
        ],
        "preventive_measures_en": [
            "Sow rust-tolerant certified varieties recommended by MPKV Rahuri (e.g., KDS-344 / Phule Sangam, KDS-726 / Phule Kimaya)",
            "Do not delay spraying: once 40% canopy shows pustules, chemical control efficiency drops sharply",
            "Monitor southern winds from Western Ghats (Satara/Kolhapur border)"
        ],
        "preventive_measures_mr": [
            "फुले संगम (KDS-344) किंवा फुले किमया (KDS-726) या तांबेरा-प्रतिकारक्षम वाणांची पेरणी करा",
            "रोगाची पहिली लक्षणे दिसताच तात्काळ फवारणी करा, उशीर झाल्यास नियंत्रण कठीण होते",
            "सातारा, सांगली, कोल्हापूर सीमावर्ती भागातील हवामानावर लक्ष ठेवा"
        ],
        "maharashtra_zone_notes": "Critical epidemic vulnerability in Kolhapur (Karveer/Radhanagari), Sangli (Walwa/Shirala), and Pune (Bhor/Velhe).",
        "disclaimer": "Do not harvest green fodder for dairy cattle within 25 days of triazole spray."
    },

    "Soybean___Bacterial_blight": {
        "crop": "Soybean",
        "crop_mr": "सोयाबीन",
        "display_name_en": "Soybean Bacterial Blight (Jivanujanya Karpa)",
        "display_name_mr": "सोयाबीन जिवाणूजन्य करपा / बॅक्टेरियल ब्लाइट",
        "causal_organism": "Pseudomonas savastanoi pv. glycinea",
        "pathogen_type": "Bacterial",
        "description_en": "Common cool-weather bacterial disease causing angular water-soaked leaf spots that tear and shred in heavy wind.",
        "description_mr": "थंड आणि दमट हवामानात येणारा रोग. पानांवर कोनीय तपकिरी डाग पडतात आणि पाने फाटून चाळणीसारखी होतात.",
        "symptoms_en": [
            "Small, angular water-soaked leaf spots turning translucent yellow then brown",
            "Prominent chlorotic halos surrounding lesions",
            "Centers dry out and drop out, giving leaves a ragged wind-shredded appearance"
        ],
        "symptoms_mr": [
            "पानांच्या शिरांच्या मधे कोनीय लहान डाग पडतात",
            "डागांच्या भोवती पिवळसर कडा असते व मध्यभाग सुकून गळतो",
            "तीव्र वाऱ्यामुळे पाने फाटतात आणि पानांना छिद्रे पडतात"
        ],
        "favorable_conditions_en": "Cool rainy weather (22-26°C), stormy winds that injure leaf epidermis, and splashing rain.",
        "favorable_conditions_mr": "थंड व पावसाळी हवामान (२२-२६ अंश), जोराचे वारे आणि पानांवर उडणारे पावसाचे पाणी.",
        "chemical_treatments": [
            {
                "name": "Streptocycline + Copper Oxychloride Combo",
                "dosage": "1.0 g Streptocycline per 10 L water + 25 g Blitox (COC) per 10 L water",
                "application_schedule": "Apply after rainstorms causing mechanical leaf bruising.",
                "phi_days": 21,
                "cost_range_inr": "₹120 - ₹180 per acre"
            }
        ],
        "organic_treatments": [
            {
                "name": "Pseudomonas fluorescens 1% WP",
                "dosage": "5.0 g per litre of water",
                "cost_range_inr": "₹160 - ₹240 per kg",
                "prep_instructions": "Foliar spray to introduce competing bacterial antagonistic microflora."
            }
        ],
        "preventive_measures_en": [
            "Avoid cultivating or moving machinery through soybean rows while leaves are wet",
            "Incorporate crop residues deeply during summer deep ploughing",
            "Use certified clean seed stock"
        ],
        "preventive_measures_mr": [
            "पाने ओली असताना शेतात कोळपणी किंवा काम करणे टाळा",
            "उन्हाळ्यात शेताची खोल नांगरट करा जेणेकरून अवशेष गाडले जातील",
            "प्रमाणित निरोगी बियाणे वापरा"
        ],
        "maharashtra_zone_notes": "Occurs in northern Maharashtra and Marathwada zones following turbulent cyclonic showers.",
        "disclaimer": "Wear face mask and rubber boots when mixing copper-streptocycline slurry."
    },

    "Soybean___Cercospora_leaf_blight": {
        "crop": "Soybean",
        "crop_mr": "सोयाबीन",
        "display_name_en": "Soybean Cercospora Leaf Blight (Jambla Karpa)",
        "display_name_mr": "सोयाबीन जांभळा करपा / सर्कोस्पोरा ब्लाइट",
        "causal_organism": "Cercospora kikuchii",
        "pathogen_type": "Fungal",
        "description_en": "Fungal pathogen causing purple-bronze foliar discoloration, leathery leaf texture, and purple seed stain in pods.",
        "description_mr": "पानांवर जांभळट-तपकिरी चकाकी येऊन पाने चामड्यासारखी जाड होतात आणि दाण्यांवर जांभळा डाग पडतो.",
        "symptoms_en": [
            "Upper canopy leaves develop bronze-to-purplish discoloration on exposed surface",
            "Foliage becomes thickened, leathery, and wrinkled",
            "Produces characteristic purple stain on harvested soybean seeds"
        ],
        "symptoms_mr": [
            "झाडाच्या वरच्या बाजूच्या पानांवर जांभळट-तांबूस चकाकणारे डाग दिसतात",
            "पाने चामड्यासारखी कडक आणि सुरकुतलेली होतात",
            "कापणीच्या वेळी बियाण्यावर जांभळे डाग पडतात ज्यामुळे बाजारात कमी भाव मिळतो"
        ],
        "favorable_conditions_en": "High temperatures (27-32°C), long dew periods, and high humidity during pod fill.",
        "favorable_conditions_mr": "उबदार व दमट हवामान (२७-३२ अंश) आणि शेंगा भरताना पडणारे दव.",
        "chemical_treatments": [
            {
                "name": "Saaf (Carbendazim 12% + Mancozeb 63% WP)",
                "dosage": "2.0 g per litre of water (400 g per 200 L water/acre)",
                "application_schedule": "Apply at R3 (early pod development) stage.",
                "phi_days": 21,
                "cost_range_inr": "₹280 - ₹390 per 500g"
            },
            {
                "name": "Custodia (Azoxystrobin 11% + Tebuconazole 18.3% w/w SC)",
                "dosage": "1.5 ml per litre of water",
                "application_schedule": "Dual-action systemic fungicide for late-season canopy protection.",
                "phi_days": 25,
                "cost_range_inr": "₹750 - ₹1,050 per 250ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Neem Oil 10,000 PPM + Cow Dung Slurry Filtrate",
                "dosage": "3.0 ml Neem Oil per litre of water",
                "cost_range_inr": "₹140 - ₹220 per litre",
                "prep_instructions": "Foliar application to suppress Cercosporin fungal toxins."
            }
        ],
        "preventive_measures_en": [
            "Rotate crops annually with jowar, bajra, or cotton",
            "Ensure certified seed germination and grading to discard discolored seeds",
            "Harvest promptly once pods mature to avoid seed coat weathering"
        ],
        "preventive_measures_mr": [
            "सोयाबीननंतर ज्वारी, बाजरी किंवा कपाशी पिकाची फेरपालट करा",
            "पेरणीपूर्वी जांभळे डाग असलेले बियाणे निवडून बाजूला काढा",
            "पीक पक्व झाल्यावर काढणीस विलंब करू नका"
        ],
        "maharashtra_zone_notes": "Frequently reported across Vidarbha and Marathwada during late kharif pod maturation.",
        "disclaimer": "Do not reuse purple-stained harvested seed for next season sowing."
    },

    # =========================================================================
    # TOMATO - EXTENDED CONDITIONS
    # =========================================================================
    "Tomato___Septoria_leaf_spot": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Septoria Leaf Spot",
        "display_name_mr": "टोमॅटोवरील सेप्टोरिया करपा / पानावरील ठिपके",
        "causal_organism": "Septoria lycopersici (Fungus)",
        "pathogen_type": "Fungal",
        "pathogen_type_mr": "बुरशीजन्य रोग 🍄",
        "what_happened_en": "Fungal leaf spot disease has attacked your tomato foliage. Numerous small circular spots with dark borders are actively spreading on leaves, reducing photosynthesis.",
        "what_happened_mr": "तुमच्या टोमॅटो पिकावर सेप्टोरिया करपा बुरशीचा प्रादुर्भाव झाला आहे. पानांवर गोलाकार काळे-तपकिरी ठिपके पडले असून झाडाची अन्न तयार करण्याची क्षमता मंदावली आहे.",
        "why_it_happened_en": "Prolonged leaf wetness, high humidity (> 75%), cloudy weather, and rain splashes from bare soil allowed fungal spores (Septoria lycopersici) to germinate on lower leaves.",
        "why_it_happened_mr": "पावसाची सततची रिमझिम, पानांवर जास्त वेळ राहिलेला ओलावा, हवेतील आर्द्रता (> ७५%) आणि मातीचे उडालेले थेंब यामुळे बुरशीच्या बीजाणूंची वाढ झाली आहे.",
        "how_it_spreads_en": "Spreads upward from lower leaves via splashing rainwater, sprinkler irrigation, wind gusts, contaminated hands, and pruning shears.",
        "how_it_spreads_mr": "पावसाचे उडणारे थेंब, तुषार सिंचन, वारा आणि छाटणीच्या अवजारांद्वारे खालच्या जुन्या पानांवरून वरच्या नवीन पानांवर वेगाने पसरतो.",
        "risk_if_neglected_en": "If neglected, leaves yellow rapidly, dry up, and drop off (heavy defoliation). Exposed tomatoes suffer severe sunscald (sunburn) causing 30% to 50% loss in marketable yield.",
        "risk_if_neglected_mr": "वेळेवर फवारणी न केल्यास तीव्र पानगळ होते, फळे उघडी पडून उन्हाने भाजतात आणि उत्पादनात ३०% ते ५०% पर्यंत मोठी घट होऊ शकते.",
        "description_en": "Septoria leaf spot is a severe fungal disease of tomato. It produces numerous small (1-3mm) circular spots with dark brown margins and gray centers on older leaves first.",
        "description_mr": "सेप्टोरिया हा टोमॅटोवरील एक गंभीर बुरशीजन्य रोग आहे. झाडाच्या खालच्या पानांवर बारीक गोलाकार राखाडी-तपकिरी रंगाचे काळी कडा असलेले ठिपके पडतात.",
        "symptoms_en": [
            "Numerous small, circular spots (1-3 mm) with dark brown margins and grayish-tan centers",
            "Tiny black specks (pycnidia fruiting bodies) visible inside the center of mature spots",
            "Infection starts strictly on older lower foliage near soil and progresses upward",
            "Severe leaf yellowing (chlorosis) around spots followed by premature leaf drop"
        ],
        "symptoms_mr": [
            "पानांवर १ ते ३ मिमी आकाराचे गोलाकार डाग ज्यांची कडा गडद तपकिरी व मध्यभाग राखाडी असतो",
            "डागांच्या मध्यभागी बारीक काळ्या मोहरीसारखे बुरशीचे ठिपके (पिक्निडिया) दिसतात",
            "सुरुवातीला जमिनीलगतच्या खालच्या जुन्या पानांवर प्रादुर्भाव होतो आणि नंतर वर पसरतो",
            "डागांच्या भोवती पान पिवळे पडून कालांतराने वाळून गळते"
        ],
        "favorable_conditions_en": "Warm temperatures (20-26°C), persistent humidity over 80%, and wet foliage for 6+ hours.",
        "favorable_conditions_mr": "२० ते २६ अंश सेल्सिअस तापमान, ८०% पेक्षा जास्त आर्द्रता आणि पानांवर सलग ६ तास राहिलेला ओलावा.",
        "chemical_treatments": [
            {
                "name": "Mancozeb 75% WP (Indofil M-45 / Dithane M-45)",
                "commercial_name": "Mancozeb 75% WP (Indofil M-45 / Dithane M-45)",
                "chemical_name": "Mancozeb 75% WP",
                "dosage": "2.0 g - 2.5 g per litre of water",
                "dosage_per_liter": 2.0,
                "dose_15l_pump": "30g to 35g per 15L Pump (१५ लिटर पंपासाठी ३०-३५ ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader (१० मिली स्टीकर)",
                "timing": "Early morning before 9 AM or evening after 4 PM (शांत हवेत)",
                "application_schedule": "Spray immediately upon spotting lower leaf lesions. Repeat after 7-10 days if cloudy.",
                "phi_days": 7,
                "cost_range_inr": "₹280 - ₹360 per 500g"
            },
            {
                "name": "Kavach (Chlorothalonil 75% WP)",
                "commercial_name": "Kavach (Chlorothalonil 75% WP)",
                "chemical_name": "Chlorothalonil 75% WP",
                "dosage": "2.0 g per litre of water",
                "dosage_per_liter": 2.0,
                "dose_15l_pump": "30g per 15L Pump (१५ लिटर पंपासाठी ३० ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Morning before 9 AM or evening",
                "application_schedule": "Broad-spectrum contact fungicide to halt secondary spore sporulation.",
                "phi_days": 7,
                "cost_range_inr": "₹420 - ₹580 per 500g"
            },
            {
                "name": "Custodia (Azoxystrobin 11% + Tebuconazole 18.3% SC)",
                "commercial_name": "Custodia (Azoxystrobin + Tebuconazole)",
                "chemical_name": "Azoxystrobin 11% + Tebuconazole 18.3% SC",
                "dosage": "1.5 ml per litre of water",
                "dosage_per_liter": 1.5,
                "dose_15l_pump": "22 ml per 15L Pump (१५ लिटर पंपासाठी २२ मिली)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Early morning",
                "application_schedule": "Curative systemic dual-action spray for rapid disease control.",
                "phi_days": 10,
                "cost_range_inr": "₹750 - ₹950 per 250ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Trichoderma viride 1% WP (ट्रायकोडर्मा विरिडी जैव बुरशीनाशक)",
                "dosage": "5.0 g per litre of water",
                "dosage_per_liter": 5.0,
                "dose_15l_pump": "75g per 15L Pump (१५ लिटर पंपासाठी ७५ ग्रॅम)",
                "cost_range_inr": "₹160 - ₹240 per 1 kg",
                "prep_instructions": "Mix with water and 50g jaggery, spray on leaves. Eliminates fungal spores with zero chemical residue."
            },
            {
                "name": "Cold-pressed Neem Oil (10,000 PPM) + Cow Urine",
                "dosage": "3.0 ml Neem Oil + 10 ml Cow Urine per litre of water",
                "dosage_per_liter": 3.0,
                "dose_15l_pump": "45 ml Neem Oil per 15L Pump (१५ लिटर पंपासाठी ४५ मिली)",
                "cost_range_inr": "₹150 - ₹220 per 500ml",
                "prep_instructions": "Organic anti-fungal repellent spray; completely safe with 0-day Pre-Harvest Interval."
            }
        ],
        "sanitation_steps_en": [
            "Pluck heavily spotted bottom leaves and burn or bury them far away from the field (do not compost).",
            "Stop overhead sprinkler watering immediately; switch to drip irrigation to keep foliage dry.",
            "Apply straw or silver-black mulch on beds to prevent raindrops from splashing soil spores onto leaves."
        ],
        "sanitation_steps_mr": [
            "रोगाने पिवळी पडलेली खालची पाने हाताने खुडून शेताबाहेर नेऊन जाळून किंवा जमिनीत गाडून टाका.",
            "पानांवर पाणी उडवणे (तुषार सिंचन) पूर्णपणे बंद करा; फक्त ठिबक सिंचनाने मुळाशी पाणी द्या.",
            "जमिनीवर गवताचे किंवा मल्चिंग पेपरचे आच्छादन करा जेणेकरून पावसाचे पाणी मातीतून पानांवर उडणार नाही."
        ],
        "preventive_measures_en": [
            "Maintain 60 cm row spacing and stake plants on wires/bamboos to improve aeration",
            "Sanitize pruning scissors and hands before touching uninfected tomato plants",
            "Follow 2-year crop rotation without potatoes, eggplants, or peppers in the same bed"
        ],
        "preventive_measures_mr": [
            "दोन झाडांत ६० सेंमी अंतर ठेवा आणि बांबूने झाडे बांधा जेणेकरून शेतात हवा खेळती राहील",
            "छाटणी करताना कात्री निर्जंतुक करून वापरा जेणेकरून निरोगी झाडांवर रोग पसरणार नाही",
            "टोमॅटोनंतर बटाटा, वांगी न लावता मका, झेंडू किंवा कडधान्य पिकांची फेरपालट करा"
        ],
        "maharashtra_zone_notes": "Very common in Narayangaon, Junnar, Nashik, and Sangli tomato clusters during overcast monsoon.",
        "disclaimer": "Do not leave diseased foliage on the ground as spores can survive for over 12 months in soil residue."
    },

    "Tomato___Leaf_Mold": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Leaf Mold",
        "display_name_mr": "टोमॅटो पानावरील बुरशी / लीफ मोल्ड",
        "causal_organism": "Passalora fulva (Fungus)",
        "pathogen_type": "Fungal",
        "pathogen_type_mr": "बुरशीजन्य रोग 🍄",
        "what_happened_en": "High greenhouse humidity has triggered velvety fungal mold growth on tomato foliage.",
        "what_happened_mr": "जास्त आर्द्रतेमुळे टोमॅटोच्या पानाच्या खालच्या बाजूला मखमली जांभळट-तपकिरी बुरशीचा थर वाढला आहे.",
        "why_it_happened_en": "Relative humidity exceeding 85% with warm greenhouse temperatures (21-24°C) without adequate ventilation.",
        "why_it_happened_mr": "हवेतील आर्द्रता ८५% पेक्षा जास्त राहिल्याने आणि शेडनेट/पॉलीहाऊसमध्ये हवा बंदिस्त झाल्याने बुरशी वाढली.",
        "how_it_spreads_en": "Air currents and ventilation fans carry millions of microscopic conidia across the canopy.",
        "how_it_spreads_mr": "हवेचा प्रवाह आणि फॅनद्वारे बुरशीचे लाखो बीजाणू हवेत उडून इतर झाडांवर पसरतात.",
        "risk_if_neglected_en": "Rapid leaf withering, defoliation, and fruit yield drop by up to 35%.",
        "risk_if_neglected_mr": "पाने वाळून चुरगळतात, गळतात आणि टोमॅटो उत्पादनात ३५% पर्यंत घट होते.",
        "description_en": "Leaf mold primarily affects tomato leaves, creating pale green to yellow spots on the upper leaf surface and olive-green velvety mold underneath.",
        "description_mr": "पानाच्या वरच्या बाजूला पिवळे डाग आणि खालच्या बाजूला ऑलिव्ह-हिरवी मखमली बुरशी तयार करणारा रोग.",
        "symptoms_en": [
            "Pale yellow spots on the upper leaf surface with indefinite borders",
            "Dense olive-green to grayish-brown velvety mold on the corresponding lower leaf surface",
            "Infected leaves curl, wither, and drop prematurely"
        ],
        "symptoms_mr": [
            "पानाच्या वरच्या बाजूला फिकट पिवळे डाग पडतात",
            "पानाच्या खालच्या बाजूला मखमली ऑलिव्ह-हिरवी किंवा करडी बुरशी वाढते",
            "पाने आकसतात, सुकतात आणि गळून पडतात"
        ],
        "favorable_conditions_en": "Relative humidity > 85%, stagnant air, and temperatures between 22-26°C.",
        "favorable_conditions_mr": "८५% पेक्षा जास्त आर्द्रता, बंदिस्त हवा आणि २२-२६ अंश तापमान.",
        "chemical_treatments": [
            {
                "name": "Copper Oxychloride 50% WP (Blitox 50)",
                "commercial_name": "Blitox 50 (Copper Oxychloride 50% WP)",
                "chemical_name": "Copper Oxychloride 50% WP",
                "dosage": "2.5 g per litre of water",
                "dosage_per_liter": 2.5,
                "dose_15l_pump": "37g per 15L Pump (१५ लिटर पंपासाठी ३५-४० ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Early morning or late afternoon",
                "application_schedule": "Spray undersides of leaves thoroughly.",
                "phi_days": 5,
                "cost_range_inr": "₹280 - ₹380 per 500g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Bordeaux Mixture 1% (बोर्डो मिश्रण १%)",
                "dosage": "10 g Copper Sulfate + 10 g Lime per litre",
                "dosage_per_liter": 10.0,
                "dose_15l_pump": "150g CuSO4 + 150g Lime per 15L Pump",
                "cost_range_inr": "₹120 - ₹180 per prep",
                "prep_instructions": "Freshly prepare neutralized 1% Bordeaux mixture and spray."
            }
        ],
        "sanitation_steps_en": [
            "Increase greenhouse side curtain ventilation immediately to drop humidity below 80%.",
            "Prune bottom sucker leaves to allow air movement through the lower canopy.",
            "Avoid late evening watering that leaves the canopy wet overnight."
        ],
        "sanitation_steps_mr": [
            "पॉलीहाऊस/शेडनेटचे पडदे उघडून हवा खेळती ठेवा जेणेकरून आर्द्रता ८०% च्या खाली येईल.",
            "खालची रोगट व दाट पाने छाटून टाका जेणेकरून खाली सूर्यप्रकाश पोहोचेल.",
            "संध्याकाळी उशिरा पाणी देणे टाळा जेणेकरून रात्रभर पाने ओली राहणार नाहीत."
        ],
        "preventive_measures_en": [
            "Select leaf-mold resistant hybrid varieties (Cf genes)",
            "Space plants at least 50 cm apart",
            "Sanitize greenhouse structure between crop cycles"
        ],
        "preventive_measures_mr": [
            "लीफ मोल्ड प्रतिकारक वाण निवडा",
            "दोन झाडांत पुरेसे अंतर ठेवा",
            "हंगाम संपल्यावर शेडनेट निर्जंतुक करा"
        ]
    },

    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Two-Spotted Spider Mites (Red Mites)",
        "display_name_mr": "टोमॅटोवरील लाल कोळी (स्पायडर माइट्स)",
        "causal_organism": "Tetranychus urticae (Microscopic Mite)",
        "pathogen_type": "Pest/Mite",
        "pathogen_type_mr": "कीटक/कोळी प्रादुर्भाव 🕷️",
        "what_happened_en": "Microscopic spider mites are piercing plant leaf cells and sucking sap from the underside of foliage.",
        "what_happened_mr": "अतिसूक्ष्म लाल कोळ्यांनी पानाच्या खालच्या बाजूने रस शोषण्यास सुरुवात केली असून पानाच्या वर बारीक जाळे तयार झाले आहे.",
        "why_it_happened_en": "Hot, dry, and dusty weather (temperature > 30°C, humidity < 50%) promotes explosive mite reproduction.",
        "why_it_happened_mr": "उष्ण, कोरडे आणि धुळीचे हवामान (३०° पेक्षा जास्त तापमान व कमी आर्द्रता) यामुळे कोळ्यांची संख्या झपाट्याने वाढते.",
        "how_it_spreads_en": "Carried by wind currents on fine webbing filaments, clothing, and farm tools.",
        "how_it_spreads_mr": "हवेच्या प्रवाहाने, जाळ्याच्या बारीक धाग्यांनी आणि कपड्यांद्वारे शेतात एका झाडावरून दुसऱ्या झाडावर पसरतात.",
        "risk_if_neglected_en": "Leaves bronze, dry like paper, and drop. Fruit turns small and sunburned; up to 60% crop loss in dry seasons.",
        "risk_if_neglected_mr": "पाने चॉकलेटी पडून कागदासारखी वाळतात व गळतात. फळे लहान राहतात आणि उन्हाळ्यात ६०% पर्यंत नुकसान होते.",
        "description_en": "Spider mites are tiny arachnids that feed on plant sap, causing yellow stippling and producing fine silk webbing on leaf undersides.",
        "description_mr": "पानाच्या खालून रस शोषून बारीक जाळे विणणारे अतिसूक्ष्म लाल कीटक ज्यामुळे पाने वाळतात.",
        "symptoms_en": [
            "Fine yellow or white stippling (speckling) on the upper surface of leaves",
            "Fine webbing visible between leaf veins and growing tips under sunlight",
            "Leaves turn bronze, brown, brittle, and drop off in severe infestations"
        ],
        "symptoms_mr": [
            "पानांच्या वरच्या बाजूला पिवळसर बारीक ठिपके (स्टिपलिंग) दिसतात",
            "पानाच्या खालच्या बाजूला व शेंड्यांवर बारीक कोळ्याचे जाळे दिसते",
            "तीव्र प्रादुर्भावात पाने तांबूस-चॉकलेटी होऊन वाळतात"
        ],
        "favorable_conditions_en": "Hot, dry, dusty conditions with temperatures 30-38°C and low humidity.",
        "favorable_conditions_mr": "उष्ण, कोरडे आणि धुळीचे हवामान, ३० ते ३८ अंश तापमान.",
        "chemical_treatments": [
            {
                "name": "Oberon (Spiromesifen 22.9% SC)",
                "commercial_name": "Oberon (Spiromesifen 22.9% SC)",
                "chemical_name": "Spiromesifen 22.9% SC",
                "dosage": "1.0 ml per litre of water",
                "dosage_per_liter": 1.0,
                "dose_15l_pump": "15 ml per 15L Pump (१५ लिटर पंपासाठी १५ मिली)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Evening spray with high pressure targeting leaf undersides",
                "application_schedule": "Specialized miticide that sterilizes female mites and kills eggs.",
                "phi_days": 5,
                "cost_range_inr": "₹480 - ₹680 per 100ml"
            },
            {
                "name": "Omite (Propargite 57% EC)",
                "commercial_name": "Omite (Propargite 57% EC)",
                "chemical_name": "Propargite 57% EC",
                "dosage": "2.0 ml per litre of water",
                "dosage_per_liter": 2.0,
                "dose_15l_pump": "30 ml per 15L Pump (१५ लिटर पंपासाठी ३० मिली)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Evening spray",
                "application_schedule": "Contact miticide with quick knockdown action.",
                "phi_days": 7,
                "cost_range_inr": "₹380 - ₹520 per 250ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Cold-pressed Neem Oil (10,000 PPM) + Liquid Soap",
                "dosage": "5.0 ml Neem Oil + 1 ml Liquid Soap per litre",
                "dosage_per_liter": 5.0,
                "dose_15l_pump": "75 ml Neem Oil per 15L Pump (१५ लिटर पंपासाठी ७५ मिली)",
                "cost_range_inr": "₹180 - ₹260 per 500ml",
                "prep_instructions": "Soap emulsifies neem oil, which suffocates mites and disrupts breeding."
            },
            {
                "name": "Wettable Sulfur 80% WDG (सल्फर ८०%)",
                "dosage": "2.5 g per litre of water",
                "dosage_per_liter": 2.5,
                "dose_15l_pump": "35g per 15L Pump (१५ लिटर पंपासाठी ३५ ग्रॅम)",
                "cost_range_inr": "₹160 - ₹240 per 1 kg",
                "prep_instructions": "Suppresses both mites and powdery mildew naturally. Do not spray in extreme heat (>35°C)."
            }
        ],
        "sanitation_steps_en": [
            "Wash dusty field roads around the tomato field to suppress dust that helps mites.",
            "Spray clear water mist on foliage under high pressure to dislodge mite webbing.",
            "Remove and destroy severely webbed infested branches immediately."
        ],
        "sanitation_steps_mr": [
            "शेताभोवतालच्या रस्त्यावर पाणी मारून धूळ कमी करा, कारण धुळीमुळे कोळी वेगाने वाढतात.",
            "पानाच्या खालच्या बाजूवर पाण्याच्या फवाऱ्याने दाबाने फवारणी करून जाळे धुवून काढा.",
            "जाळे लागलेल्या जास्त प्रादुर्भावाच्या फांद्या छाटून नष्ट करा."
        ],
        "preventive_measures_en": [
            "Avoid broad-spectrum pyrethroid insecticides which kill natural predatory ladybird beetles",
            "Maintain soil moisture to keep plants hydrated and resilient",
            "Monitor undersides of leaves weekly with a 10x hand lens"
        ],
        "preventive_measures_mr": [
            "मित्रकिडी मारणारी कीटकनाशके टाळा जेणेकरून निसर्गतः कोळ्यांचा नायनाट होईल",
            "जमिनीत पुरेसा ओलावा ठेवा जेणेकरून झाडांवर पाण्याचा ताण पडणार नाही",
            "दर आठवड्याला पानाच्या खालच्या बाजूचे बारकाईने निरीक्षण करा"
        ]
    },

    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop": "Tomato",
        "crop_mr": "टोमॅटो",
        "display_name_en": "Tomato Yellow Leaf Curl Virus (Chuda-Buda)",
        "display_name_mr": "टोमॅटो पिवळा पर्णगुच्छ रोग / चुरडा-मुरडा (TYLCV)",
        "causal_organism": "Tomato Yellow Leaf Curl Begomovirus (Vectored by Whitefly)",
        "pathogen_type": "Viral",
        "pathogen_type_mr": "विषाणूजन्य रोग 🧬",
        "what_happened_en": "Whitefly sucking pests have transmitted the Tomato Yellow Leaf Curl Virus into your tomato plants.",
        "what_happened_mr": "पांढऱ्या माशीने रस शोषून विषाणूचा संसर्ग केला आहे, ज्यामुळे झाडाची पाने पिवळी पडून आकसली व वाकडी झाली आहेत.",
        "why_it_happened_en": "High population of Bemisia tabaci (whitefly vector) feeding on young vegetative shoots during dry warm spells.",
        "why_it_happened_mr": "शेतात पांढऱ्या माशीचा (व्हाईटफ्लाय) प्रादुर्भाव झाल्यामुळे या विषाणूचा वेगाने प्रसार झाला आहे.",
        "how_it_spreads_en": "Transmitted exclusively by silverleaf whiteflies (Bemisia tabaci). Not spread by seed or mechanical touch.",
        "how_it_spreads_mr": "हा रोग केवळ पांढऱ्या माशीद्वारे एका झाडावरून दुसऱ्या झाडावर पसरतो. स्पर्श किंवा बियाण्याने पसरत नाही.",
        "risk_if_neglected_en": "Severe stunting, flower drop, and zero marketable fruit set. Total crop failure if infected before flowering.",
        "risk_if_neglected_mr": "झाडांची वाढ पूर्णपणे खुंटते, फुले गळतात आणि फळधारणा होत नाही. फुलोऱ्यापूर्वी रोग झाल्यास १००% नुकसान होते.",
        "description_en": "TYLCV is a devastating viral disease caused by a Begomovirus and vectored by whiteflies. Plants become stunted and bushy with upward-curled yellow leaves.",
        "description_mr": "टोमॅटोवरील अत्यंत विनाशकारी विषाणूजन्य रोग. पाने पिवळी पडून वाटीसारखी वर वळतात आणि झाड खुंटते.",
        "symptoms_en": [
            "Severe upward leaf curling and cupping of leaflets into a spoon shape",
            "Marked yellowing (chlorosis) of leaf margins and interveinal spaces",
            "Stunted plant growth with shortened internodes giving a bushy appearance",
            "Flower bud abortion and heavy premature flower drop"
        ],
        "symptoms_mr": [
            "पाने वाटीसारखी किंवा चमच्यासारखी वरच्या बाजूला वळतात (चुरडा-मुरडा)",
            "पानांच्या कडा आणि शिरांमधील भाग ठळक पिवळा पडतो",
            "झाडाची उंची खुंटून झाड झुडपासारखे गुच्छात वाढते",
            "फुलगळ होते आणि लागलेली फळे लहान व खडबडीत होतात"
        ],
        "favorable_conditions_en": "Warm dry weather favoring whitefly proliferation (28-35°C).",
        "favorable_conditions_mr": "उष्ण व कोरडे हवामान ज्यामध्ये पांढरी माशी वेगाने अंडी घालते.",
        "chemical_treatments": [
            {
                "name": "Actara (Thiamethoxam 25% WG) - Vector Control",
                "commercial_name": "Actara (Thiamethoxam 25% WG)",
                "chemical_name": "Thiamethoxam 25% WG",
                "dosage": "0.5 g per litre of water",
                "dosage_per_liter": 0.5,
                "dose_15l_pump": "8g per 15L Pump (१५ लिटर पंपासाठी ८ ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Early morning spray",
                "application_schedule": "Systemic insecticide to eliminate whitefly vectors transmitting the virus.",
                "phi_days": 5,
                "cost_range_inr": "₹280 - ₹380 per 100g"
            },
            {
                "name": "Confidor (Imidacloprid 17.8% SL) - Vector Control",
                "commercial_name": "Confidor (Imidacloprid 17.8% SL)",
                "chemical_name": "Imidacloprid 17.8% SL",
                "dosage": "0.5 ml per litre of water",
                "dosage_per_liter": 0.5,
                "dose_15l_pump": "8 ml per 15L Pump (१५ लिटर पंपासाठी ८ मिली)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Morning spray",
                "application_schedule": "Systemic neonicotinoid targeting sucking nymphs and adults.",
                "phi_days": 7,
                "cost_range_inr": "₹320 - ₹450 per 100ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Yellow Sticky Traps (पिवळे चिकट सापळे) + Neem Spray",
                "dosage": "Install 25-30 Yellow Sticky Traps per Acre",
                "dosage_per_liter": 5.0,
                "dose_15l_pump": "75 ml Neem Oil (10,000 PPM) per 15L Pump",
                "cost_range_inr": "₹250 - ₹350 per acre kit",
                "prep_instructions": "Whiteflies are strongly attracted to bright yellow sticky sheets and get trapped instantly."
            }
        ],
        "sanitation_steps_en": [
            "Rogue out and destroy infected viral plants immediately to eliminate the infection source.",
            "Install 25 yellow sticky traps per acre at canopy height to capture adult whiteflies.",
            "Surround fields with a dense barrier crop of maize or jowar (2-3 border rows) to block incoming whitefly swarms."
        ],
        "sanitation_steps_mr": [
            "रोगाने ग्रासलेली झाडे उपटून त्वरित शेताबाहेर खड्ड्यात गाडून नष्ट करा जेणेकरून निरोगी झाडे वाचतील.",
            "शेतात एकरी २५ ते ३० पिवळे चिकट सापळे पिकाच्या उंचीवर लावा जेणेकरून पांढरी माशी अडकेल.",
            "शेताच्या चारी बाजूंनी मका किंवा ज्वारीच्या २ ते ३ दाट ओळी लावा जेणेकरून पांढरी माशी रोखली जाईल."
        ],
        "preventive_measures_en": [
            "Use TYLCV-tolerant tomato hybrids (e.g., US-440, Abhinav, Saaho)",
            "Cover nursery beds with 40-mesh insect-proof netting for the first 30 days",
            "Drench seedling roots with imidacloprid prior to transplanting"
        ],
        "preventive_measures_mr": [
            "व्हायरस प्रतिबंधक टोमॅटो वाण (उदा. साहू, अभिनव) लावा",
            "रोपवाटिकेत रोपे ४० मेशच्या कीटक प्रतिबंधक जाळीखाली तयार करा",
            "लागवडीपूर्वी रोपांची मुळे कीटकनाशकात बुडवून लावा"
        ]
    },

    "Potato___Early_blight": {
        "crop": "Potato",
        "crop_mr": "बटाटा",
        "display_name_en": "Potato Early Blight (Karpa)",
        "display_name_mr": "बटाटा करपा / अर्ली ब्लाइट",
        "causal_organism": "Alternaria solani (Fungus)",
        "pathogen_type": "Fungal",
        "pathogen_type_mr": "बुरशीजन्य रोग 🍄",
        "what_happened_en": "Early blight fungal infection has developed concentric target-board lesions on older potato leaves.",
        "what_happened_mr": "बटाट्याच्या पानांवर अल्टरनेरिया करप्याचा प्रादुर्भाव झाला असून गोलाकार वळ्यांचे डाग पडले आहेत.",
        "why_it_happened_en": "Alternating wet and dry periods, warm temperatures (24-28°C), and aging foliage under stress.",
        "why_it_happened_mr": "उष्ण व दमट हवामान, सकाळी पडणारे दव आणि पाण्याचा ताण यामुळे बुरशीची वाढ झाली आहे.",
        "how_it_spreads_en": "Windblown airborne spores and splashing irrigation droplets.",
        "how_it_spreads_mr": "वाऱ्याने उडणारे बीजाणू आणि पाण्याच्या थेंबांमुळे शेतात रोग पसरतो.",
        "risk_if_neglected_en": "Premature vine death, small undersized tubers, and 20% to 40% reduction in tuber yield.",
        "risk_if_neglected_mr": "बटाट्याचे वेल वेळेपूर्वी वाळतात, बटाटे बारीक राहतात आणि २० ते ४० टक्के नुकसान होते.",
        "description_en": "Early blight causes dark brown circular spots with concentric target-board rings surrounded by yellow halos on potato foliage.",
        "description_mr": "बटाट्याच्या पानांवर गोलाकार एकाआड एक वळ्यांचे काळे-तपकिरी डाग पाडणारा बुरशीजन्य रोग.",
        "symptoms_en": [
            "Dark brown to black lesions with concentric rings resembling a target board",
            "Yellow chlorotic tissue surrounding individual lesions",
            "Starts on bottom older foliage and moves upward toward plant apex"
        ],
        "symptoms_mr": [
            "पानांवर टार्गेट बोर्डसारखे गोलाकार वळ्यांचे तपकिरी डाग पडतात",
            "डागांच्या भोवती पिवळसर कडा तयार होते",
            "खालच्या जुन्या पानांवरून सुरु होऊन वरच्या पानांवर पसरतो"
        ],
        "favorable_conditions_en": "Warm days with heavy dew at night, temperatures between 24-29°C.",
        "favorable_conditions_mr": "उबदार दिवस आणि रात्री पडणारे दाट दव, २४ ते २९ अंश सेल्सिअस तापमान.",
        "chemical_treatments": [
            {
                "name": "Mancozeb 75% WP (Indofil M-45)",
                "commercial_name": "Mancozeb 75% WP (Indofil M-45)",
                "chemical_name": "Mancozeb 75% WP",
                "dosage": "2.5 g per litre of water",
                "dosage_per_liter": 2.5,
                "dose_15l_pump": "35g per 15L Pump (१५ लिटर पंपासाठी ३५ ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Morning spray",
                "application_schedule": "Prophylactic and early curative contact spray.",
                "phi_days": 14,
                "cost_range_inr": "₹280 - ₹350 per 500g"
            }
        ],
        "organic_treatments": [
            {
                "name": "Trichoderma viride + Cold-pressed Neem Oil",
                "dosage": "5.0 g Trichoderma + 3 ml Neem Oil per litre",
                "dosage_per_liter": 5.0,
                "dose_15l_pump": "75g Trichoderma + 45 ml Neem Oil per 15L Pump",
                "cost_range_inr": "₹160 - ₹240 per kg",
                "prep_instructions": "Biological foliar spray to suppress Alternaria spores safely."
            }
        ],
        "sanitation_steps_en": [
            "Ensure proper earthing-up (hilling) of potato ridges to keep tubers buried deep.",
            "Avoid overhead irrigation in late afternoon.",
            "Destroy diseased crop vines after harvest."
        ],
        "sanitation_steps_mr": [
            "बटाट्याच्या रोपांना चांगली मातीची भर द्या जेणेकरून कंद उघडे पडणार नाहीत.",
            "संध्याकाळी पाणी देणे टाळा जेणेकरून पाने रात्रभर ओली राहणार नाहीत.",
            "काढणीनंतर शेतातील वाळलेले अवशेष जाळून नष्ट करा."
        ],
        "preventive_measures_en": [
            "Use certified disease-free seed tubers",
            "Maintain balanced potassium and nitrogen fertilization",
            "Rotate crops with non-solanaceous legumes or cereals"
        ],
        "preventive_measures_mr": [
            "प्रमाणित निरोगी बटाटा बियाणे वापरा",
            "संतुलित खते द्या, नत्राचा अतिवापर टाळा",
            "डाळवर्गीय किंवा तृणधान्य पिकांची फेरपालट करा"
        ]
    },

    "Potato___Late_blight": {
        "crop": "Potato",
        "crop_mr": "बटाटा",
        "display_name_en": "Potato Late Blight (Tambera Karpa)",
        "display_name_mr": "बटाटा लेट ब्लाइट / तांबेरा करपा",
        "causal_organism": "Phytophthora infestans (Oomycete)",
        "pathogen_type": "Fungal/Oomycete",
        "pathogen_type_mr": "बुरशीजन्य रोग 🍄",
        "what_happened_en": "Dangerous late blight pathogen has attacked potato foliage, producing water-soaked dark lesions and white sporulation.",
        "what_happened_mr": "बटाट्यावर अत्यंत घातक लेट ब्लाइट रोगाचा प्रादुर्भाव झाला असून पाने पाणीदार काळी पडून कुजत आहेत.",
        "why_it_happened_en": "Continuous overcast, drizzly, cold weather (temperature 15-20°C) with humidity over 90%.",
        "why_it_happened_mr": "ढगाळ व थंड हवामान (१५-२०° तापमान) आणि हवेत ९०% पेक्षा जास्त आर्द्रता असल्यामुळे रोग उद्भवला आहे.",
        "how_it_spreads_en": "Windborne sporangia travel miles in cool humid breezes and wash into soil during rains.",
        "how_it_spreads_mr": "वाऱ्याच्या थंड प्रवाहाने बीजाणू मैलोनमैल पसरतात आणि पावसाच्या पाण्याने जमिनीत कंदांपर्यंत पोहोचतात.",
        "risk_if_neglected_en": "Complete collapse of entire field within 4-7 days; tuber rot in storage causing 80% to 100% loss.",
        "risk_if_neglected_mr": "संपूर्ण शेत ४ ते ७ दिवसांत जळून नष्ट होते आणि बटाटे साठवणीत सडतात (८० ते १००% नुकसान).",
        "description_en": "Late blight is the most destructive potato disease globally, capable of wiping out entire fields within a few days under wet weather.",
        "description_mr": "बटाट्यावरील जगातील सर्वात विनाशकारी रोग, जो दमट हवामानात संपूर्ण पीक काही दिवसांत जाळून नष्ट करतो.",
        "symptoms_en": [
            "Large, irregular water-soaked pale to dark green lesions turning rapidly dark brown to black",
            "Delicate white fungal-like downy mold on the undersides of leaves during humid mornings",
            "Stems develop water-soaked dark brown streaks and collapse easily",
            "Distinct foul odor emitted from rapidly rotting foliage"
        ],
        "symptoms_mr": [
            "पानांवर मोठे, पाणीदार, अनियमित काळे-तपकिरी डाग पडतात जे वेगाने पसरतात",
            "सकाळी दमट वातावरणात पानाच्या खालच्या बाजूला पांढरी बुरशी दिसते",
            "खोडावर काळे पाणीदार चट्टे पडून खोड मऊ पडून मोडते",
            "सडलेल्या पानांमधून विशिष्ट कुजट आंबट वास येतो"
        ],
        "favorable_conditions_en": "Cool temperatures (15-21°C), relative humidity > 90%, and persistent fog or rain.",
        "favorable_conditions_mr": "थंड हवामान (१५ ते २१ अंश), हवेतील आर्द्रता ९०% पेक्षा जास्त आणि सततचे धुके किंवा रिमझिम पाऊस.",
        "chemical_treatments": [
            {
                "name": "Ridomil Gold (Metalaxyl-M 4% + Mancozeb 64% WP)",
                "commercial_name": "Ridomil Gold (Metalaxyl-M + Mancozeb)",
                "chemical_name": "Metalaxyl-M 4% + Mancozeb 64% WP",
                "dosage": "2.5 g per litre of water",
                "dosage_per_liter": 2.5,
                "dose_15l_pump": "38g per 15L Pump (१५ लिटर पंपासाठी ३५-४० ग्रॅम)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Immediate spray within 24 hours of first symptom",
                "application_schedule": "Systemic protective and curative fungicide.",
                "phi_days": 14,
                "cost_range_inr": "₹450 - ₹620 per 500g"
            },
            {
                "name": "Revus (Mandipropamid 23.4% SC)",
                "commercial_name": "Revus (Mandipropamid 23.4% SC)",
                "chemical_name": "Mandipropamid 23.4% SC",
                "dosage": "1.0 ml per litre of water",
                "dosage_per_liter": 1.0,
                "dose_15l_pump": "15 ml per 15L Pump (१५ लिटर पंपासाठी १५ मिली)",
                "spreader_15l": "10 ml Silicon Spreader",
                "timing": "Early morning",
                "application_schedule": "Rainfast translaminar fungicide with exceptional late blight control.",
                "phi_days": 7,
                "cost_range_inr": "₹650 - ₹850 per 200ml"
            }
        ],
        "organic_treatments": [
            {
                "name": "Bordeaux Mixture 1% (१% बोर्डो मिश्रण)",
                "dosage": "10 g Copper Sulfate + 10 g Slaked Lime per litre",
                "dosage_per_liter": 10.0,
                "dose_15l_pump": "150g CuSO4 + 150g Lime per 15L Pump",
                "cost_range_inr": "₹120 - ₹180 per prep",
                "prep_instructions": "Apply preventive copper film over foliage before rainy spell."
            }
        ],
        "sanitation_steps_en": [
            "Cut and burn potato vines 10 days before harvest (dehaulming) to prevent tuber contamination.",
            "Never throw infected tubers into cull piles near the field.",
            "Avoid walking through wet infected fields to prevent spreading spores on boots."
        ],
        "sanitation_steps_mr": [
            "काढणीच्या १० दिवस आधी बटाट्याचे वेल कापून टाका (डिहॉमिंग) जेणेकरून जमिनीत कंदाला संसर्ग होणार नाही.",
            "रोगट बटाटे शेताजवळ उघड्यावर टाकू नका, खोल खड्ड्यात पुरा.",
            "ओल्या शेतातून चालणे टाळा जेणेकरून पायाद्वारे रोग इतरत्र पसरणार नाही."
        ],
        "preventive_measures_en": [
            "Plant resistant cultivars (e.g., Kufri Girdhari, Kufri Himalini)",
            "Hill up rows tightly with high soil ridges",
            "Monitor regional late blight forecasting warnings"
        ],
        "preventive_measures_mr": [
            "लेट ब्लाइट प्रतिकारक वाण (उदा. कुफरी गिरधारी) निवडा",
            "बटाट्याला चांगली मातीची उंच भर लावा",
            "हवामान विभागाच्या इशाऱ्यांवर लक्ष ठेवा"
        ]
    },

    "Potato___healthy": {
        "crop": "Potato",
        "crop_mr": "बटाटा",
        "display_name_en": "Healthy Potato Leaf",
        "display_name_mr": "निरोगी बटाटा पान",
        "causal_organism": "None (Healthy)",
        "pathogen_type": "None",
        "pathogen_type_mr": "निरोगी पीक 🌿",
        "what_happened_en": "Your potato plant is completely healthy, displaying strong green canopy and active tuber development.",
        "what_happened_mr": "तुमचे बटाटा पीक पूर्णपणे निरोगी आणि सशक्त असून पानांवर कोणताही करपा किंवा डाग नाही.",
        "why_it_happened_en": "Balanced nutrition, good drainage, and proactive crop care.",
        "why_it_happened_mr": "चांगले व्यवस्थापन, निचरा असलेली जमीन आणि योग्य निगा राखल्यामुळे पीक निरोगी आहे.",
        "how_it_spreads_en": "Not applicable (Crop is healthy).",
        "how_it_spreads_mr": "लागू नाही (पीक निरोगी आहे).",
        "risk_if_neglected_en": "No disease present; maintain preventive scouting during overcast humid days.",
        "risk_if_neglected_mr": "सध्या कोणताही धोका नाही; दमट हवामानात शेताची नियमित पाहणी ठेवा.",
        "description_en": "The potato foliage exhibits healthy dark-green leaflets with crisp texture and robust vine growth.",
        "description_mr": "बटाट्याचे पान पूर्णपणे निरोगी, तजेलदार आणि हिरवेगार आहे.",
        "symptoms_en": [
            "Uniform green leaf pigmentation without target spots or water-soaked margins",
            "No mold on undersides of leaves and no stem discoloration"
        ],
        "symptoms_mr": [
            "हिरवेगार तजेलदार पान",
            "कोणताही डाग, करपा किंवा बुरशी आढळलेली नाही"
        ],
        "favorable_conditions_en": "Optimal sunshine, fertile soil, and controlled drip irrigation.",
        "favorable_conditions_mr": "योग्य सूर्यप्रकाश, सुपिक जमीन आणि ठिबक सिंचन.",
        "chemical_treatments": [
            {
                "name": "Preventive Micronutrient Foliar Spray (00:52:34)",
                "commercial_name": "19:19:19 or 00:52:34 NPK",
                "chemical_name": "Water-soluble fertilizer",
                "dosage": "4.0 g per litre of water",
                "dosage_per_liter": 4.0,
                "dose_15l_pump": "60g per 15L Pump",
                "spreader_15l": "10 ml Spreader",
                "timing": "Morning",
                "application_schedule": "Foliar spray to support tuber bulking stage.",
                "phi_days": 0,
                "cost_range_inr": "₹160 - ₹240 per 1 kg"
            }
        ],
        "organic_treatments": [
            {
                "name": "Neem Oil 10,000 PPM (कडुनिंब तेल)",
                "dosage": "2.0 ml per litre of water",
                "dosage_per_liter": 2.0,
                "dose_15l_pump": "30 ml per 15L Pump",
                "cost_range_inr": "₹150 - ₹220 per 500ml",
                "prep_instructions": "Prophylactic bio-spray to keep aphids and sucking pests away."
            }
        ],
        "sanitation_steps_en": [
            "Keep ridges weed-free and inspect foliage every 3 days.",
            "Ensure tubers remain well-covered with soil to avoid greening."
        ],
        "sanitation_steps_mr": [
            "शेतात तण नियंत्रण ठेवा आणि दर ३ दिवसांनी पाहणी करा.",
            "कंद उघडे पडणार नाहीत याची काळजी घ्या."
        ],
        "preventive_measures_en": [
            "Maintain proper earthing-up",
            "Monitor weather for sudden late blight risk alerts"
        ],
        "preventive_measures_mr": [
            "वेळेवर मातीची भर द्या",
            "धुके किंवा सतत पाऊस असल्यास वेळेवर प्रतिबंधक फवारणी करा"
        ]
    },
}


# =============================================================================
# Helper Utilities
# =============================================================================

CROP_MAPPING = {
    "Grapes": {
        "en": "Grapes",
        "mr": "द्राक्ष",
        "keys": [
            "Grape___healthy",
            "Grape___Downy_mildew",
            "Grape___Powdery_mildew",
            "Grape___Black_rot",
        ]
    },
    "Tomato": {
        "en": "Tomato",
        "mr": "टोमॅटो",
        "keys": [
            "Tomato___healthy",
            "Tomato___Early_blight",
            "Tomato___Late_blight",
            "Tomato___Bacterial_spot",
        ]
    },
    "Soybean": {
        "en": "Soybean",
        "mr": "सोयाबीन",
        "keys": [
            "Soybean___healthy",
            "Soybean___Rust",
            "Soybean___Bacterial_blight",
            "Soybean___Cercospora_leaf_blight",
        ]
    }
}


def get_treatment_for_disease(disease_key: str) -> dict:
    """Retrieve localized treatment entry by disease class key with complete plain explanations."""
    result = None
    if disease_key in TREATMENTS_DATABASE:
        result = dict(TREATMENTS_DATABASE[disease_key])
    else:
        # Fuzzy fallback match in TREATMENTS_DATABASE
        clean_key = disease_key.replace(" ", "_")
        for k, v in TREATMENTS_DATABASE.items():
            if k.lower() in clean_key.lower() or clean_key.lower() in k.lower():
                result = dict(v)
                break

    # Check disease_info.json for all expanded classes with Marathi support
    if not result:
        try:
            from pathlib import Path
            import json
            info_path = Path(__file__).resolve().parent.parent.parent / "app" / "disease_info.json"
            if info_path.exists():
                with open(info_path, "r", encoding="utf-8") as f:
                    d_info = json.load(f)
                
                matched_entry = None
                if disease_key in d_info:
                    matched_entry = d_info[disease_key]
                else:
                    for dk, entry in d_info.items():
                        if dk.lower() in clean_key.lower() or clean_key.lower() in dk.lower():
                            matched_entry = entry
                            break

                if matched_entry:
                    result = {
                        "crop": matched_entry.get("plant", "Crop"),
                        "crop_mr": matched_entry.get("plant_mr", "पीक"),
                        "display_name_en": f"{matched_entry.get('plant', '')} {matched_entry.get('disease', '')}".strip(),
                        "display_name_mr": f"{matched_entry.get('plant_mr', '')} {matched_entry.get('disease_mr', '')}".strip(),
                        "causal_organism": matched_entry.get("disease", "Pathogen"),
                        "pathogen_type": "Fungal/Bacterial/Viral",
                        "description_en": matched_entry.get("description", ""),
                        "description_mr": matched_entry.get("description_mr", ""),
                        "symptoms_en": matched_entry.get("symptoms", []),
                        "symptoms_mr": matched_entry.get("symptoms_mr", []),
                        "chemical_treatments": [
                            {
                                "name": "Mancozeb 75% WP / Recommended Protective Spray",
                                "commercial_name": "Mancozeb 75% WP (Indofil M-45)",
                                "chemical_name": "Mancozeb 75% WP",
                                "dosage": "2.0 g/L",
                                "dose_15l_pump": "30g to 35g per 15L Pump (१५ लिटर पंपासाठी ३० ग्रॅम)",
                                "spreader_15l": "10 ml Silicon Spreader (१० मिली स्टीकर)",
                                "timing": "Early morning before 9 AM or evening after 4 PM",
                                "cost_range_inr": "₹280 - ₹380 per 500g",
                                "phi_days": 7,
                                "application_schedule": "Foliar spray on affected leaves"
                            }
                        ],
                        "organic_treatments": [
                            {
                                "name": "Cold-pressed Neem Oil (10,000 PPM) + Bio-control",
                                "dosage": "3 ml/L",
                                "dose_15l_pump": "45 ml per 15L Pump (१५ लिटर पंपासाठी ४५ मिली)",
                                "cost_range_inr": "₹150 - ₹250 per 500ml",
                                "prep_instructions": "Eco-safe foliar spray with 0-day harvest interval"
                            }
                        ],
                        "preventive_measures_en": matched_entry.get("prevention", []),
                        "preventive_measures_mr": matched_entry.get("prevention_mr", []),
                    }
        except Exception:
            pass
            
    if not result:
        result = dict(TREATMENTS_DATABASE.get("Tomato___Early_blight", {}))

    # Guarantee complete plain-language explanation fields
    plant_en = result.get("crop") or disease_key.split("___")[0].replace("_", " ")
    plant_mr = result.get("crop_mr") or plant_en
    dis_en = result.get("display_name_en") or disease_key.split("___")[-1].replace("_", " ")
    dis_mr = result.get("display_name_mr") or dis_en
    is_healthy = "healthy" in disease_key.lower()

    if is_healthy:
        result.setdefault("what_happened_en", f"Your {plant_en} crop is completely healthy, displaying strong green foliage and vigorous growth.")
        result.setdefault("what_happened_mr", f"तुमचे {plant_mr} पीक पूर्णपणे निरोगी आणि सशक्त असून पानांवर कोणताही रोग आढळलेला नाही.")
        result.setdefault("why_it_happened_en", "Optimal sunlight, balanced fertilization, and good cultural management.")
        result.setdefault("why_it_happened_mr", "योग्य सूर्यप्रकाश, संतुलित खत व्यवस्थापन आणि योग्य निगा राखल्यामुळे पीक निरोगी आहे.")
        result.setdefault("how_it_spreads_en", "Not applicable (Crop is healthy).")
        result.setdefault("how_it_spreads_mr", "लागू नाही (पीक निरोगी आहे).")
        result.setdefault("risk_if_neglected_en", "No immediate disease risk; maintain preventive field scouting.")
        result.setdefault("risk_if_neglected_mr", "सध्या कोणताही धोका नाही; शेताचे नियमित निरीक्षण ठेवा.")
        result.setdefault("pathogen_type", "None (Healthy)")
        result.setdefault("pathogen_type_mr", "निरोगी पीक 🌿")
    else:
        pathogen = result.get("pathogen_type", "Fungal")
        path_mr = "बुरशीजन्य रोग 🍄" if "fung" in pathogen.lower() else "जीवाणूजन्य रोग 🦠" if "bact" in pathogen.lower() else "विषाणूजन्य रोग 🧬" if "vir" in pathogen.lower() else "कीटक/कोळी प्रादुर्भाव 🕷️"
        result.setdefault("pathogen_type_mr", path_mr)
        result.setdefault("what_happened_en", f"Foliar infection identified on {plant_en}. Leaf tissue is showing symptoms of {dis_en}, which reduces photosynthetic efficiency.")
        result.setdefault("what_happened_mr", f"{plant_mr} पिकावर {dis_mr} रोगाचा प्रादुर्भाव आढळला आहे, ज्यामुळे पानांची अन्न तयार करण्याची क्षमता मंदावली आहे.")
        result.setdefault("why_it_happened_en", "Recent high humidity, cloudy skies, prolonged leaf wetness, or water droplets created ideal conditions for pathogen activation.")
        result.setdefault("why_it_happened_mr", "हवेतील जास्त ओलावा, आर्द्रता, पावसाची रिमझिम किंवा पानांवर राहिलेल्या पाण्यामुळे या रोगाची सुरुवात झाली आहे.")
        result.setdefault("how_it_spreads_en", "Spreads via rain splash droplets, wind currents, farm tools, and brushing against wet foliage.")
        result.setdefault("how_it_spreads_mr", "पावसाचे उडणारे थेंब, वारा, छाटणीची अवजारे आणि ओल्या पानांच्या संपर्काद्वारे रोग इतर झाडांवर पसरतो.")
        result.setdefault("risk_if_neglected_en", "If neglected, leaves yellow and drop off (defoliation), leading to sunscald and a 20% to 45% loss in crop yield.")
        result.setdefault("risk_if_neglected_mr", "वेळेवर नियंत्रण न केल्यास तीव्र पानगळ होऊन उत्पादनात २०% ते ४५% घट होण्याची दाट शक्यता आहे.")

    # Ensure chemical dose_15l_pump exists
    for chem in result.get("chemical_treatments", []):
        if "dose_15l_pump" not in chem:
            dose_val = chem.get("dosage", "2.0 g/L")
            chem["dose_15l_pump"] = "30g to 35g per 15L Pump (१५ लिटर पंपासाठी ३० ग्रॅम)"
        if "spreader_15l" not in chem:
            chem["spreader_15l"] = "10 ml Silicon Spreader (१० मिली स्टीकर)"
        if "timing" not in chem:
            chem["timing"] = "Early morning before 9 AM or evening after 4 PM"

    # Ensure organic dose_15l_pump exists
    for org in result.get("organic_treatments", []):
        if "dose_15l_pump" not in org:
            org["dose_15l_pump"] = "45 ml / 75 g per 15L Pump (१५ लिटर पंपासाठी)"

    # Ensure sanitation steps exist
    if "sanitation_steps_en" not in result or not result["sanitation_steps_en"]:
        if is_healthy:
            result["sanitation_steps_en"] = [
                "Keep rows weed-free to maximize sunlight and airflow.",
                "Ensure proper drainage in the field to avoid water stagnation.",
                "Scout the underside of leaves twice a week for early signs of pests."
            ]
            result["sanitation_steps_mr"] = [
                "शेतात तण नियंत्रण ठेवा जेणेकरून सूर्यप्रकाश व हवा खेळती राहील.",
                "शेतात पाणी साचणार नाही यासाठी पाण्याचा चांगला निचरा ठेवा.",
                "आठवड्यातून दोनदा पानाच्या खालच्या बाजूचे नियमित निरीक्षण करा."
            ]
        else:
            result["sanitation_steps_en"] = [
                "Pluck and collect heavily infected fallen leaves, then bury or burn them outside the field.",
                "Avoid overhead sprinkler irrigation; irrigate strictly at the soil base using drip lines.",
                "Apply mulch around plant bases to prevent rain from splashing soil-borne spores onto leaves."
            ]
            result["sanitation_steps_mr"] = [
                "रोगाने जास्त बाधित झालेली पाने खुडून शेताबाहेर नेऊन जाळून किंवा खड्ड्यात गाडून नष्ट करा.",
                "तुषार सिंचनाने पानांवर पाणी उडवणे टाळा; फक्त ठिबक सिंचनाने मुळाशी पाणी द्या.",
                "पावसाचे पाणी मातीतून पानांवर उडू नये म्हणून झाडाच्या बुंध्याशी आच्छादन (मल्चिंग) करा."
            ]

    return result


def get_diseases_for_crop(crop_name: str) -> list:
    """Return all supported disease keys for the selected crop."""
    crop_info = CROP_MAPPING.get(crop_name)
    if crop_info:
        return crop_info["keys"]
    return list(TREATMENTS_DATABASE.keys())
