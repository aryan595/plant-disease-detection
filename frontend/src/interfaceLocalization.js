const COPY = {
  en: {
    farmerInfo: "Farmer-friendly mode: direct dose and WhatsApp guidance", expertInfo: "Expert mode: visual guide and insurance details",
    farmer: "Farmer Mode", expert: "Expert Mode", voiceTitle: "Listen to Spoken Agronomic Advisory", voiceDescription: "Hear the diagnosis, severity and 15L pump dose in your language.", play: "Play Voice", stop: "Stop",
    doseTitle: "15L Knapsack Pump Direct Prescription:", hold: "Prescription on hold due to low confidence. Please re-scan the leaf with a clear close-up.", healthy: "Crop is healthy. No chemical spray is needed.", dose: (amount, name) => `Mix ${amount}g/ml of ${name} + 10ml wetting sticker per 15-liter knapsack tank.`, ideal: "Ideal spray time: calm morning before 9 AM or evening after 4 PM.",
    tank: "Check Spray Tank Mix", forecast: "View 7-Day Weather Risk", kendras: "Find Krishi Kendras", guide: "View Leaf Guide & Insurance Claim",
    marketBadge: "APMC MARKET RATES", marketName: "Pune Gultekdi Market Yard", modalRate: "Modal rate", range: "Price range", quintal: "quintal", kg: "kg", arrivals: "Arrivals",
    adviceTitle: "Need Advice? Consult AI Plant Doctor", adviceText: "Get instant answers on dosage, safety intervals, and crop management.", openChat: "Open AI Chat",
    forecastTitle: (district) => `7-Day Weather & Epidemic Forecast (${district})`, forecastText: "Daily forecast of fungal infection pressure, rain wash-off risks, and optimal spray windows.", loadingForecast: "Loading 7-day forecast…", day: "Day", optimal: "Optimal for spraying",
    mixTitle: "Chemical Tank-Mix & Spray Safety Checker", mixText: "Verify whether two chemicals or foliar fertilizers can be mixed safely in the same spray tank.", product1: "Product 1", product2: "Product 2", checkMix: "Check Mix",
    helpline: "Kisan Support & Agronomy Helplines (Maharashtra)", callCentre: "Kisan Call Centre (Toll-Free)", stateHelpline: "Maharashtra Agriculture Helpline", university: "MPKV Rahuri Agronomy Cell", kvk: "Krishi Vigyan Kendra (KVK)",
  },
  hi: {
    farmerInfo: "किसान मोड: सीधी खुराक और व्हाट्सऐप मार्गदर्शन", expertInfo: "विशेषज्ञ मोड: दृश्य मार्गदर्शक और बीमा विवरण", farmer: "किसान मोड", expert: "विशेषज्ञ मोड", voiceTitle: "कृषि सलाह आवाज़ में सुनें", voiceDescription: "निदान, तीव्रता और 15L पंप की खुराक अपनी भाषा में सुनें।", play: "आवाज़ में सुनें", stop: "रोकें", doseTitle: "15 लीटर पंप के लिए सीधी खुराक:", hold: "कम विश्वास स्तर के कारण सलाह रोकी गई है। कृपया पत्ते का स्पष्ट नज़दीकी फोटो लेकर फिर जाँच करें।", healthy: "फसल स्वस्थ है। रासायनिक स्प्रे की आवश्यकता नहीं है।", dose: (amount, name) => `15 लीटर पंप में ${name} की ${amount}g/ml मात्रा और 10ml स्टिकर मिलाएँ।`, ideal: "स्प्रे का सही समय: सुबह 9 बजे से पहले या शाम 4 बजे के बाद शांत मौसम में।", tank: "टैंक मिश्रण जाँचें", forecast: "7-दिन मौसम जोखिम देखें", kendras: "कृषि केंद्र खोजें", guide: "पत्ती गाइड और बीमा दावा देखें", marketBadge: "एपीएमसी बाजार भाव", marketName: "पुणे गुलटेकडी बाजार यार्ड", modalRate: "औसत भाव", range: "मूल्य सीमा", quintal: "क्विंटल", kg: "किलो", arrivals: "आवक", adviceTitle: "सलाह चाहिए? AI कृषि डॉक्टर से पूछें", adviceText: "खुराक, सुरक्षा अंतराल और फसल प्रबंधन पर तुरंत जानकारी पाएँ।", openChat: "AI चैट खोलें", forecastTitle: (district) => `7-दिन मौसम और रोग जोखिम पूर्वानुमान (${district})`, forecastText: "फफूंद संक्रमण दबाव, बारिश से धुलने के जोखिम और स्प्रे के उपयुक्त समय का दैनिक पूर्वानुमान।", loadingForecast: "7-दिन का पूर्वानुमान लोड हो रहा है…", day: "दिन", optimal: "स्प्रे के लिए अनुकूल", mixTitle: "रासायनिक टैंक-मिश्रण और स्प्रे सुरक्षा जाँच", mixText: "दो रसायनों या पर्ण उर्वरकों को एक ही टैंक में सुरक्षित रूप से मिलाने की जाँच करें।", product1: "उत्पाद 1", product2: "उत्पाद 2", checkMix: "मिश्रण जाँचें", helpline: "किसान सहायता एवं कृषि हेल्पलाइन (महाराष्ट्र)", callCentre: "किसान कॉल सेंटर (टोल-फ्री)", stateHelpline: "महाराष्ट्र कृषि हेल्पलाइन", university: "एमपीकेवी राहुरी कृषि प्रकोष्ठ", kvk: "कृषि विज्ञान केंद्र (KVK)",
  },
  mr: {
    farmerInfo: "शेतकरी सोपा मोड: थेट औषध प्रमाण व व्हॉट्सॲप मार्गदर्शन", expertInfo: "तज्ज्ञ मोड: पान मार्गदर्शक व विमा तपशील", farmer: "शेतकरी मोड", expert: "तज्ज्ञ मोड", voiceTitle: "AI डॉक्टरांचा सल्ला आवाजात ऐका", voiceDescription: "निदान, तीव्रता व १५L पंपाचे फवारणी प्रमाण ऐका.", play: "आवाजात ऐका", stop: "थांबवा", doseTitle: "१५ लिटर पंपासाठी थेट औषध प्रमाण:", hold: "विश्वास स्तर कमी असल्याने फवारणीची शिफारस थांबवली आहे. स्पष्ट जवळचा फोटो घेऊन पुनर्परीक्षण करा.", healthy: "पीक निरोगी आहे. रासायनिक फवारणीची गरज नाही.", dose: (amount, name) => `१५ लिटर पंपात ${name} चे ${amount} ग्रॅम/मिली आणि १० मिली स्टिकर मिसळा.`, ideal: "फवारणीची योग्य वेळ: सकाळी ९ पूर्वी किंवा संध्याकाळी ४ नंतर शांत हवेत.", tank: "औषध मिश्रण तपासा", forecast: "७-दिवस हवामान धोका पहा", kendras: "कृषी केंद्रे शोधा", guide: "पान मार्गदर्शक व विमा दावा पहा", marketBadge: "एपीएमसी बाजारभाव", marketName: "पुणे गुलटेकडी मार्केट यार्ड", modalRate: "सरासरी भाव", range: "किमान - कमाल भाव", quintal: "क्विंटल", kg: "किलो", arrivals: "आवक", adviceTitle: "सल्ला हवा आहे? AI कृषी डॉक्टरांना विचारा", adviceText: "औषध प्रमाण, सुरक्षा अंतर व पीक व्यवस्थापनाबद्दल तत्काळ माहिती मिळवा.", openChat: "AI चॅट सुरू करा", forecastTitle: (district) => `७ दिवसांचा हवामान व रोग धोका अंदाज (${district})`, forecastText: "बुरशी संसर्गाचा धोका, पावसामुळे धुऊन जाण्याचा धोका आणि योग्य फवारणी वेळेचा दैनिक अंदाज.", loadingForecast: "७ दिवसांचा अंदाज लोड होत आहे…", day: "दिवस", optimal: "फवारणीसाठी उत्तम", mixTitle: "रासायनिक मिश्रण व फवारणी सुरक्षा तपासणी", mixText: "दोन औषधे किंवा पर्णखत एकाच टाकीत सुरक्षितपणे मिसळता येतील का ते तपासा.", product1: "औषध १", product2: "औषध २", checkMix: "मिश्रण तपासा", helpline: "शेतकरी मदत व कृषी हेल्पलाइन (महाराष्ट्र)", callCentre: "किसान कॉल सेंटर (टोल-फ्री)", stateHelpline: "महाराष्ट्र कृषी हेल्पलाइन", university: "एमपीकेव्ही राहुरी कृषी केंद्र", kvk: "कृषी विज्ञान केंद्र (KVK)",
  },
  bn: {
    farmerInfo: "কৃষক মোড: সরাসরি মাত্রা ও নির্দেশনা", expertInfo: "বিশেষজ্ঞ মোড: ভিজ্যুয়াল গাইড ও বীমা তথ্য", farmer: "কৃষক মোড", expert: "বিশেষজ্ঞ মোড", voiceTitle: "কণ্ঠে কৃষি পরামর্শ শুনুন", voiceDescription: "রোগ নির্ণয়, তীব্রতা ও ১৫L পাম্পের মাত্রা নিজের ভাষায় শুনুন।", play: "কণ্ঠে শুনুন", stop: "থামান", doseTitle: "১৫L পাম্পের সরাসরি মাত্রা:", hold: "আত্মবিশ্বাসের মাত্রা কম হওয়ায় পরামর্শ স্থগিত। পাতার পরিষ্কার কাছের ছবি দিয়ে আবার স্ক্যান করুন।", healthy: "ফসল সুস্থ আছে। রাসায়নিক স্প্রে প্রয়োজন নেই।", dose: (amount, name) => `১৫ লিটার পাম্পে ${name} এর ${amount}g/ml ও 10ml স্টিকার মেশান।`, ideal: "স্প্রের সেরা সময়: সকাল ৯টার আগে বা বিকেল ৪টার পরে শান্ত আবহাওয়ায়।", tank: "ট্যাংক মিশ্রণ পরীক্ষা", forecast: "৭ দিনের আবহাওয়া ঝুঁকি", kendras: "কৃষি কেন্দ্র খুঁজুন", guide: "পাতা গাইড ও বীমা দাবি", marketBadge: "এপিএমসি বাজার দর", marketName: "পুনে গুলটেকড়ি বাজার ইয়ার্ড", modalRate: "গড় দর", range: "দরের পরিসর", quintal: "কুইন্টাল", kg: "কেজি", arrivals: "আগত", adviceTitle: "পরামর্শ চান? AI কৃষি ডাক্তারকে জিজ্ঞাসা করুন", adviceText: "মাত্রা, সুরক্ষা বিরতি ও ফসল ব্যবস্থাপনা সম্পর্কে তাৎক্ষণিক উত্তর পান।", openChat: "AI চ্যাট খুলুন", forecastTitle: (district) => `৭ দিনের আবহাওয়া ও রোগ ঝুঁকির পূর্বাভাস (${district})`, forecastText: "ছত্রাক সংক্রমণ, বৃষ্টিতে ধুয়ে যাওয়ার ঝুঁকি এবং স্প্রের উপযুক্ত সময়ের দৈনিক পূর্বাভাস।", loadingForecast: "৭ দিনের পূর্বাভাস লোড হচ্ছে…", day: "দিন", optimal: "স্প্রের জন্য উপযোগী", mixTitle: "রাসায়নিক ট্যাংক মিশ্রণ ও স্প্রে নিরাপত্তা", mixText: "একই ট্যাংকে দুই রাসায়নিক বা পাতার সার নিরাপদে মেশানো যায় কি না পরীক্ষা করুন।", product1: "পণ্য ১", product2: "পণ্য ২", checkMix: "মিশ্রণ পরীক্ষা", helpline: "কৃষক সহায়তা ও কৃষি হেল্পলাইন (মহারাষ্ট্র)", callCentre: "কিষান কল সেন্টার (টোল-ফ্রি)", stateHelpline: "মহারাষ্ট্র কৃষি হেল্পলাইন", university: "এমপিকেভি রাহুরি কৃষি সেল", kvk: "কৃষি বিজ্ঞান কেন্দ্র (KVK)",
  },
  ta: {
    farmerInfo: "விவசாயி முறை: நேரடி அளவு மற்றும் வழிகாட்டல்", expertInfo: "நிபுணர் முறை: காட்சி வழிகாட்டி மற்றும் காப்பீட்டு விவரங்கள்", farmer: "விவசாயி முறை", expert: "நிபுணர் முறை", voiceTitle: "வேளாண் ஆலோசனையை குரலில் கேளுங்கள்", voiceDescription: "நோயறிதல், தீவிரம் மற்றும் 15L பம்ப் அளவை உங்கள் மொழியில் கேளுங்கள்.", play: "குரலில் கேளுங்கள்", stop: "நிறுத்து", doseTitle: "15L பம்பிற்கான நேரடி மருந்தளவு:", hold: "நம்பகத்தன்மை குறைவாக இருப்பதால் ஆலோசனை நிறுத்தப்பட்டுள்ளது. தெளிவான அருகாமைப் படத்துடன் மீண்டும் பரிசோதிக்கவும்.", healthy: "பயிர் ஆரோக்கியமாக உள்ளது. ரசாயனத் தெளிப்பு தேவையில்லை.", dose: (amount, name) => `15 லிட்டர் பம்பில் ${name} ${amount}g/ml மற்றும் 10ml ஒட்டும் திரவம் கலக்கவும்.`, ideal: "தெளிப்பதற்கான சிறந்த நேரம்: காலை 9 மணிக்கு முன் அல்லது மாலை 4 மணிக்குப் பிறகு.", tank: "தொட்டி கலவையைச் சரிபார்க்கவும்", forecast: "7 நாள் வானிலை ஆபத்து", kendras: "வேளாண் மையங்களைக் கண்டறியவும்", guide: "இலை வழிகாட்டி மற்றும் காப்பீட்டு கோரிக்கை", marketBadge: "ஏபிஎம்சி சந்தை விலை", marketName: "புனே குல்டேகடி சந்தை வளாகம்", modalRate: "சராசரி விலை", range: "விலை வரம்பு", quintal: "குவிண்டால்", kg: "கிலோ", arrivals: "வரத்து", adviceTitle: "ஆலோசனை வேண்டுமா? AI பயிர் மருத்துவரிடம் கேளுங்கள்", adviceText: "மருந்தளவு, பாதுகாப்பு இடைவெளி மற்றும் பயிர் மேலாண்மை குறித்த உடனடி பதில்களைப் பெறுங்கள்.", openChat: "AI உரையாடலைத் திற", forecastTitle: (district) => `7 நாள் வானிலை மற்றும் நோய் ஆபத்து முன்னறிவிப்பு (${district})`, forecastText: "பூஞ்சைத் தொற்று, மழையில் கழுவப்படும் ஆபத்து மற்றும் தெளிப்புக்கான சரியான நேரத்தின் தினசரி முன்னறிவிப்பு.", loadingForecast: "7 நாள் முன்னறிவிப்பு ஏற்றப்படுகிறது…", day: "நாள்", optimal: "தெளிப்புக்கு ஏற்றது", mixTitle: "ரசாயனத் தொட்டி கலவை மற்றும் தெளிப்பு பாதுகாப்பு", mixText: "ஒரே தொட்டியில் இரண்டு ரசாயனங்கள் அல்லது இலை உரங்களை பாதுகாப்பாக கலக்க முடியுமா என்பதைச் சரிபார்க்கவும்.", product1: "பொருள் 1", product2: "பொருள் 2", checkMix: "கலவையைச் சரிபார்க்கவும்", helpline: "விவசாயி உதவி மற்றும் வேளாண் உதவி எண்கள் (மகாராஷ்டிரா)", callCentre: "கிசான் அழைப்பு மையம் (கட்டணமில்லை)", stateHelpline: "மகாராஷ்டிரா வேளாண் உதவி எண்", university: "எம்பிகேவி ராகுரி வேளாண் பிரிவு", kvk: "வேளாண் அறிவியல் மையம் (KVK)",
  },
  te: {
    farmerInfo: "రైతు మోడ్: నేరుగా మోతాదు మరియు మార్గదర్శకం", expertInfo: "నిపుణుల మోడ్: దృశ్య మార్గదర్శకం మరియు బీమా వివరాలు", farmer: "రైతు మోడ్", expert: "నిపుణుల మోడ్", voiceTitle: "వ్యవసాయ సలహాను స్వరంలో వినండి", voiceDescription: "వ్యాధి నిర్ధారణ, తీవ్రత మరియు 15L పంపు మోతాదును మీ భాషలో వినండి.", play: "స్వరంలో వినండి", stop: "ఆపండి", doseTitle: "15L పంపు కోసం నేరుగా మోతాదు:", hold: "తక్కువ విశ్వసనీయత కారణంగా సూచన నిలిపివేయబడింది. స్పష్టమైన దగ్గరి చిత్రంతో మళ్లీ స్కాన్ చేయండి.", healthy: "పంట ఆరోగ్యంగా ఉంది. రసాయన స్ప్రే అవసరం లేదు.", dose: (amount, name) => `15 లీటర్ల పంపులో ${name} ${amount}g/ml మరియు 10ml స్టిక్కర్ కలపండి.`, ideal: "స్ప్రేకు ఉత్తమ సమయం: ఉదయం 9 గంటల ముందు లేదా సాయంత్రం 4 తర్వాత ప్రశాంత వాతావరణంలో.", tank: "ట్యాంక్ మిశ్రమాన్ని తనిఖీ చేయండి", forecast: "7 రోజుల వాతావరణ ప్రమాదం", kendras: "వ్యవసాయ కేంద్రాలను కనుగొనండి", guide: "ఆకు మార్గదర్శి మరియు బీమా క్లెయిమ్", marketBadge: "ఏపీఎంసీ మార్కెట్ ధరలు", marketName: "పూణే గుల్టెకడి మార్కెట్ యార్డ్", modalRate: "సగటు ధర", range: "ధర పరిధి", quintal: "క్వింటాల్", kg: "కిలో", arrivals: "రాకలు", adviceTitle: "సలహా కావాలా? AI పంట వైద్యుడిని అడగండి", adviceText: "మోతాదు, భద్రతా విరామం మరియు పంట నిర్వహణపై తక్షణ సమాధానాలు పొందండి.", openChat: "AI చాట్ తెరవండి", forecastTitle: (district) => `7 రోజుల వాతావరణం మరియు వ్యాధి ప్రమాద అంచనా (${district})`, forecastText: "ఫంగల్ ఇన్ఫెక్షన్, వర్షంలో కొట్టుకుపోయే ప్రమాదం మరియు స్ప్రేకు సరైన సమయం యొక్క రోజువారీ అంచనా.", loadingForecast: "7 రోజుల అంచనా లోడ్ అవుతోంది…", day: "రోజు", optimal: "స్ప్రేకు అనుకూలం", mixTitle: "రసాయన ట్యాంక్ మిశ్రమం మరియు స్ప్రే భద్రతా తనిఖీ", mixText: "ఒకే ట్యాంక్‌లో రెండు రసాయనాలు లేదా ఆకు ఎరువులను సురక్షితంగా కలపవచ్చో తనిఖీ చేయండి.", product1: "ఉత్పత్తి 1", product2: "ఉత్పత్తి 2", checkMix: "మిశ్రమాన్ని తనిఖీ చేయండి", helpline: "రైతు సహాయం మరియు వ్యవసాయ హెల్ప్‌లైన్లు (మహారాష్ట్ర)", callCentre: "కిసాన్ కాల్ సెంటర్ (టోల్-ఫ్రీ)", stateHelpline: "మహారాష్ట్ర వ్యవసాయ హెల్ప్‌లైన్", university: "ఎంపీకేవీ రాహురి వ్యవసాయ విభాగం", kvk: "కృషి విజ్ఞాన కేంద్రం (KVK)",
  },
};

// These are the interface strings that were previously embedded directly in
// components. Keeping them here prevents an English fallback from leaking
// into a selected Indian language.
const COMPLETE = {
  en: {
    voiceHeroTitle: "Have questions about your crop? Speak directly to AI!", voiceHeroBody: "Voice-first agronomic advisory powered by local crop intelligence.", voiceHeroCta: "Tap to Speak",
    cropSelector: "Select Crop for Enhanced AI Accuracy:", allCrops: "Show All Crops", original: "Original", sideBySide: "Side-by-Side", sampleLabel: "Or test with a sample leaf:",
    sampleSeptoria: "Tomato Septoria (User Photo)", sampleBlight: "Tomato Early Blight", sampleRot: "Grape Black Rot", sampleRust: "Soybean Rust", sampleHealthy: "Healthy Leaf",
    farmPractical: "Farm Practical", farmArea: "Farm land area", guntha: "Guntha", gunthas: "Gunthas", acre: "Acre", acres: "Acres", prescribedFungicide: "Prescribed fungicide", siliconSpreader: "Silicon spreader (rainfast)", pumps: "Pumps", canopy: "canopy", totalBudget: "Total chemical budget", totalChemical: "Total chemical", harvestTitle: "Days Remaining Until Crop Harvest:", days: "Days", harvestHint: "Stop chemical spraying before harvest to avoid chemical residue.",
    treatmentPackage: "Plant protection package", verified: "Verified guidance", kendraTitle: (district) => `Registered Krishi Seva Kendras & Pricing (${district})`, benchmark: "CIB&RC Agrochemical Fair MRP Benchmark", formulation: "Formulation", pack: "Pack", fairPrice: "Fair Price (INR)", brands: "Brands", loadingKendras: "Loading Krishi Kendra directory…", address: "Address", dealerType: "Dealer type", compatible: "Compatible", caution: "Use caution", avoid: "Avoid mixing", recommendation: "Recommendation",
  },
  hi: {
    voiceHeroTitle: "फसल के बारे में प्रश्न हैं? सीधे AI से पूछें!", voiceHeroBody: "स्थानीय फसल जानकारी पर आधारित आवाज़-आधारित कृषि सलाह।", voiceHeroCta: "बोलकर पूछें", cropSelector: "बेहतर AI सटीकता के लिए फसल चुनें:", allCrops: "सभी फसलें दिखाएँ", original: "मूल", sideBySide: "साथ-साथ", sampleLabel: "या नमूना पत्ती से परीक्षण करें:", sampleSeptoria: "टमाटर सेप्टोरिया (उपयोगकर्ता फोटो)", sampleBlight: "टमाटर अगेती झुलसा", sampleRot: "अंगूर काला सड़न", sampleRust: "सोयाबीन रतुआ", sampleHealthy: "स्वस्थ पत्ता", farmPractical: "खेत के लिए उपयोगी", farmArea: "खेती का क्षेत्र", guntha: "गुंठा", gunthas: "गुंठे", acre: "एकड़", acres: "एकड़", prescribedFungicide: "अनुशंसित फफूंदनाशक", siliconSpreader: "सिलिकॉन स्प्रेडर (वर्षा-रोधी)", pumps: "पंप", canopy: "फसल छत्र", totalBudget: "कुल रसायन बजट", totalChemical: "कुल रसायन", harvestTitle: "फसल कटाई तक शेष दिन:", days: "दिन", harvestHint: "रासायनिक अवशेष से बचने के लिए कटाई से पहले रासायनिक स्प्रे बंद करें।", treatmentPackage: "फसल सुरक्षा पैकेज", verified: "सत्यापित मार्गदर्शन", kendraTitle: (district) => `पंजीकृत कृषि सेवा केंद्र और मूल्य (${district})`, benchmark: "CIB&RC कृषि-रसायन उचित MRP मानक", formulation: "संयोजन", pack: "पैक", fairPrice: "उचित मूल्य (₹)", brands: "ब्रांड", loadingKendras: "कृषि केंद्र सूची लोड हो रही है…", address: "पता", dealerType: "विक्रेता प्रकार", compatible: "संगत", caution: "सावधानी से उपयोग करें", avoid: "मिश्रण न करें", recommendation: "सुझाव",
  },
  mr: {},
  bn: {
    voiceHeroTitle: "ফসল নিয়ে প্রশ্ন আছে? সরাসরি AI-কে জিজ্ঞাসা করুন!", voiceHeroBody: "স্থানীয় ফসল তথ্যভিত্তিক কণ্ঠনির্ভর কৃষি পরামর্শ।", voiceHeroCta: "বলে জিজ্ঞাসা করুন", cropSelector: "উন্নত AI নির্ভুলতার জন্য ফসল বেছে নিন:", allCrops: "সব ফসল দেখুন", original: "মূল", sideBySide: "পাশাপাশি", sampleLabel: "অথবা একটি নমুনা পাতা দিয়ে পরীক্ষা করুন:", sampleSeptoria: "টমেটো সেপ্টোরিয়া (ব্যবহারকারীর ছবি)", sampleBlight: "টমেটোর প্রারম্ভিক ঝলসা", sampleRot: "আঙুরের কালো পচন", sampleRust: "সয়াবিন রস্ট", sampleHealthy: "সুস্থ পাতা", farmPractical: "খেতের জন্য ব্যবহারযোগ্য", farmArea: "খেতের এলাকা", guntha: "গুন্ঠা", gunthas: "গুন্ঠা", acre: "একর", acres: "একর", prescribedFungicide: "প্রস্তাবিত ছত্রাকনাশক", siliconSpreader: "সিলিকন স্প্রেডার (বৃষ্টি-প্রতিরোধী)", pumps: "পাম্প", canopy: "ফসল আচ্ছাদন", totalBudget: "মোট রাসায়নিক বাজেট", totalChemical: "মোট রাসায়নিক", harvestTitle: "ফসল কাটার আগে বাকি দিন:", days: "দিন", harvestHint: "রাসায়নিক অবশিষ্ট এড়াতে ফসল কাটার আগে রাসায়নিক স্প্রে বন্ধ করুন।", treatmentPackage: "ফসল সুরক্ষা প্যাকেজ", verified: "যাচাইকৃত নির্দেশনা", kendraTitle: (district) => `নিবন্ধিত কৃষি সেবা কেন্দ্র ও মূল্য (${district})`, benchmark: "CIB&RC কৃষি-রাসায়ন ন্যায্য MRP মানদণ্ড", formulation: "ফর্মুলেশন", pack: "প্যাক", fairPrice: "ন্যায্য মূল্য (₹)", brands: "ব্র্যান্ড", loadingKendras: "কৃষি কেন্দ্রের তালিকা লোড হচ্ছে…", address: "ঠিকানা", dealerType: "বিক্রেতার ধরন", compatible: "সামঞ্জস্যপূর্ণ", caution: "সতর্কতার সাথে ব্যবহার করুন", avoid: "মেশাবেন না", recommendation: "পরামর্শ",
  },
  ta: {
    voiceHeroTitle: "உங்கள் பயிரைப் பற்றி கேள்விகள் உள்ளதா? AI-யிடம் நேரடியாக கேளுங்கள்!", voiceHeroBody: "உள்ளூர் பயிர் தகவலின் அடிப்படையிலான குரல் வேளாண் ஆலோசனை.", voiceHeroCta: "பேசிக் கேளுங்கள்", cropSelector: "சிறந்த AI துல்லியத்திற்கு பயிரைத் தேர்ந்தெடுக்கவும்:", allCrops: "அனைத்து பயிர்களையும் காண்க", original: "மூலம்", sideBySide: "அருகருகே", sampleLabel: "அல்லது மாதிரி இலையுடன் சோதிக்கவும்:", sampleSeptoria: "தக்காளி செப்டோரியா (பயனர் படம்)", sampleBlight: "தக்காளி ஆரம்பக் கருகல்", sampleRot: "திராட்சை கருப்பழுகல்", sampleRust: "சோயாபீன் துரு", sampleHealthy: "ஆரோக்கியமான இலை", farmPractical: "பண்ணைக்கு ஏற்றது", farmArea: "வயல் பரப்பளவு", guntha: "குண்டா", gunthas: "குண்டா", acre: "ஏக்கர்", acres: "ஏக்கர்", prescribedFungicide: "பரிந்துரைக்கப்பட்ட பூஞ்சைக் கொல்லி", siliconSpreader: "சிலிகான் பரப்பி (மழை எதிர்ப்பு)", pumps: "பம்புகள்", canopy: "பயிர் பரப்பு", totalBudget: "மொத்த ரசாயன செலவு", totalChemical: "மொத்த ரசாயனம்", harvestTitle: "அறுவடைக்கு மீதமுள்ள நாட்கள்:", days: "நாட்கள்", harvestHint: "ரசாயன எச்சத்தைத் தவிர்க்க அறுவடைக்கு முன் ரசாயனத் தெளிப்பை நிறுத்தவும்.", treatmentPackage: "பயிர் பாதுகாப்புத் தொகுப்பு", verified: "சரிபார்க்கப்பட்ட வழிகாட்டல்", kendraTitle: (district) => `பதிவுசெய்யப்பட்ட வேளாண் சேவை மையங்கள் மற்றும் விலை (${district})`, benchmark: "CIB&RC வேளாண்-ரசாயன நியாயமான MRP அளவுகோல்", formulation: "கலவை", pack: "பேக்", fairPrice: "நியாயமான விலை (₹)", brands: "பிராண்டுகள்", loadingKendras: "வேளாண் மைய பட்டியல் ஏற்றப்படுகிறது…", address: "முகவரி", dealerType: "விற்பனையாளர் வகை", compatible: "இணக்கமானது", caution: "எச்சரிக்கையுடன் பயன்படுத்தவும்", avoid: "கலக்க வேண்டாம்", recommendation: "பரிந்துரை",
  },
  te: {
    voiceHeroTitle: "మీ పంట గురించి ప్రశ్నలున్నాయా? నేరుగా AIని అడగండి!", voiceHeroBody: "స్థానిక పంట సమాచారంతో కూడిన వాయిస్ ఆధారిత వ్యవసాయ సలహా.", voiceHeroCta: "మాట్లాడి అడగండి", cropSelector: "మెరుగైన AI ఖచ్చితత్వం కోసం పంటను ఎంచుకోండి:", allCrops: "అన్ని పంటలను చూపండి", original: "అసలు", sideBySide: "పక్కపక్కన", sampleLabel: "లేదా నమూనా ఆకుతో పరీక్షించండి:", sampleSeptoria: "టమాటా సెప్టోరియా (వినియోగదారు ఫోటో)", sampleBlight: "టమాటా ప్రారంభ మాడుడు", sampleRot: "ద్రాక్ష నల్ల తెగులు", sampleRust: "సోయాబీన్ తుప్పు", sampleHealthy: "ఆరోగ్యకరమైన ఆకు", farmPractical: "పొలం కోసం ఉపయోగకరం", farmArea: "పొల విస్తీర్ణం", guntha: "గుంఠా", gunthas: "గుంఠాలు", acre: "ఎకరం", acres: "ఎకరాలు", prescribedFungicide: "సిఫార్సు చేసిన శిలీంధ్రనాశిని", siliconSpreader: "సిలికాన్ స్ప్రెడర్ (వర్ష నిరోధక)", pumps: "పంపులు", canopy: "పంట విస్తీర్ణం", totalBudget: "మొత్తం రసాయన బడ్జెట్", totalChemical: "మొత్తం రసాయనం", harvestTitle: "పంట కోతకు మిగిలిన రోజులు:", days: "రోజులు", harvestHint: "రసాయన అవశేషాలను నివారించడానికి కోతకు ముందు రసాయన స్ప్రేను ఆపండి.", treatmentPackage: "పంట సంరక్షణ ప్యాకేజీ", verified: "ధృవీకరించిన మార్గదర్శకం", kendraTitle: (district) => `నమోదైన వ్యవసాయ సేవా కేంద్రాలు మరియు ధరలు (${district})`, benchmark: "CIB&RC వ్యవసాయ రసాయన న్యాయమైన MRP ప్రమాణం", formulation: "సూత్రీకరణ", pack: "ప్యాక్", fairPrice: "న్యాయమైన ధర (₹)", brands: "బ్రాండ్లు", loadingKendras: "వ్యవసాయ కేంద్రాల జాబితా లోడ్ అవుతోంది…", address: "చిరునామా", dealerType: "డీలర్ రకం", compatible: "అనుకూలం", caution: "జాగ్రత్తగా ఉపయోగించండి", avoid: "కలపవద్దు", recommendation: "సిఫార్సు",
  },
};

const EXTRA = {
  en: {
    heroExplain: "Explainable AI", heroContext: "Local farm context", heroAdvice: "Action-ready advice", systemOnline: "AI system online", plantIntelligence: "Plant intelligence", cropClasses: "crop health classes", modelConfidence: "Model confidence", installApp: "Install app", installed: "Installed", locating: "Locating", liveGps: "Live farm GPS", resetGps: "Reset GPS", platformCapabilities: "Platform capabilities", farmerNavigation: "Farmer navigation", leafGuide: "Leaf Condition Guide", heatmap: "AI Heatmap", wakeService: "Waking the secure AI service and checking your leaf…", preparingGuide: "Classifying the image and preparing its leaf condition guide",
  },
  hi: {
    heroExplain: "समझने योग्य AI", heroContext: "स्थानीय खेत का संदर्भ", heroAdvice: "तुरंत उपयोगी सलाह", systemOnline: "AI प्रणाली ऑनलाइन", plantIntelligence: "पौधा बुद्धिमत्ता", cropClasses: "फसल स्वास्थ्य श्रेणियाँ", modelConfidence: "मॉडल विश्वसनीयता", installApp: "ऐप इंस्टॉल करें", installed: "इंस्टॉल हो गया", locating: "खोज रहा है", liveGps: "खेत का लाइव GPS", resetGps: "GPS रीसेट करें", platformCapabilities: "प्लेटफ़ॉर्म क्षमताएँ", farmerNavigation: "किसान नेविगेशन", leafGuide: "पत्ती स्थिति मार्गदर्शिका", heatmap: "AI ताप-मानचित्र", wakeService: "सुरक्षित AI सेवा शुरू की जा रही है और पत्ते की जाँच हो रही है…", preparingGuide: "तस्वीर का वर्गीकरण और पत्ती स्थिति मार्गदर्शिका तैयार हो रही है",
  },
  bn: {
    heroExplain: "ব্যাখ্যাযোগ্য AI", heroContext: "স্থানীয় খামারের প্রেক্ষাপট", heroAdvice: "কাজের উপযোগী পরামর্শ", systemOnline: "AI ব্যবস্থা অনলাইনে", plantIntelligence: "উদ্ভিদ বুদ্ধিমত্তা", cropClasses: "ফসল স্বাস্থ্য শ্রেণি", modelConfidence: "মডেল নির্ভরযোগ্যতা", installApp: "অ্যাপ ইনস্টল করুন", installed: "ইনস্টল হয়েছে", locating: "খোঁজা হচ্ছে", liveGps: "খামারের লাইভ GPS", resetGps: "GPS রিসেট", platformCapabilities: "প্ল্যাটফর্মের ক্ষমতা", farmerNavigation: "কৃষক নেভিগেশন", leafGuide: "পাতার অবস্থা নির্দেশিকা", heatmap: "AI তাপ-মানচিত্র", wakeService: "নিরাপদ AI পরিষেবা চালু করে পাতাটি পরীক্ষা করা হচ্ছে…", preparingGuide: "ছবি শ্রেণিবিন্যাস করে পাতার অবস্থা নির্দেশিকা তৈরি হচ্ছে",
  },
  ta: {
    heroExplain: "விளக்கக்கூடிய AI", heroContext: "உள்ளூர் பண்ணைச் சூழல்", heroAdvice: "உடனடியாகச் செயல்படுத்தக்கூடிய ஆலோசனை", systemOnline: "AI அமைப்பு ஆன்லைனில் உள்ளது", plantIntelligence: "தாவர நுண்ணறிவு", cropClasses: "பயிர் நல வகைகள்", modelConfidence: "மாதிரி நம்பகத்தன்மை", installApp: "செயலியை நிறுவுக", installed: "நிறுவப்பட்டது", locating: "கண்டறிகிறது", liveGps: "பண்ணை நேரடி GPS", resetGps: "GPS மீட்டமை", platformCapabilities: "தள திறன்கள்", farmerNavigation: "விவசாயி வழிசெலுத்தல்", leafGuide: "இலை நிலை வழிகாட்டி", heatmap: "AI வெப்ப வரைபடம்", wakeService: "பாதுகாப்பான AI சேவை தொடங்கி இலை பரிசோதிக்கப்படுகிறது…", preparingGuide: "படத்தை வகைப்படுத்தி இலை நிலை வழிகாட்டி தயாராகிறது",
  },
  te: {
    heroExplain: "వివరించగల AI", heroContext: "స్థానిక పొలం సందర్భం", heroAdvice: "అమలు చేయగల సలహా", systemOnline: "AI వ్యవస్థ ఆన్‌లైన్‌లో ఉంది", plantIntelligence: "మొక్కల మేధస్సు", cropClasses: "పంట ఆరోగ్య తరగతులు", modelConfidence: "మోడల్ విశ్వసనీయత", installApp: "యాప్‌ను ఇన్‌స్టాల్ చేయండి", installed: "ఇన్‌స్టాల్ అయింది", locating: "గుర్తిస్తోంది", liveGps: "పొలం ప్రత్యక్ష GPS", resetGps: "GPS రీసెట్", platformCapabilities: "ప్లాట్‌ఫామ్ సామర్థ్యాలు", farmerNavigation: "రైతు నావిగేషన్", leafGuide: "ఆకు స్థితి మార్గదర్శి", heatmap: "AI వేడి పటం", wakeService: "సురక్షిత AI సేవ ప్రారంభమై ఆకును పరిశీలిస్తోంది…", preparingGuide: "చిత్రాన్ని వర్గీకరించి ఆకు స్థితి మార్గదర్శి సిద్ధమవుతోంది",
  },
};

const DETAIL = {
  en: {
    analysisSubtitle: "AI-assisted plant assessment", treatmentPackage: "ICAR & CIBRC aligned plant protection package", verified: "ICAR / CIBRC verified", fieldReady: "Farm practical", targetedCurative: "Targeted curative treatment", ecoSafe: "Eco-safe bio-control", safeFoodHint: "The pre-harvest interval helps prevent residues and keeps food safe.", residueHazard: (days, phi) => `Residue hazard: only ${days} days remain before harvest (minimum wait: ${phi} days). Do not spray; choose a suitable bio-control option.`, labelDirections: "Use only according to the product label and local agricultural guidance.", phiDays: (days) => `PHI: ${days} days`, loading: "Loading…", compatibilityTip: "Follow label directions and local agricultural advice before mixing products.",
  },
  hi: {
    analysisSubtitle: "AI-सहायित पौधा आकलन", treatmentPackage: "ICAR और CIBRC अनुरूप फसल सुरक्षा पैकेज", verified: "ICAR / CIBRC सत्यापित", fieldReady: "खेत के लिए उपयोगी", targetedCurative: "लक्षित उपचार", ecoSafe: "पर्यावरण-अनुकूल जैव नियंत्रण", safeFoodHint: "कटाई-पूर्व अंतराल अवशेषों को रोकने और भोजन को सुरक्षित रखने में मदद करता है।", residueHazard: (days, phi) => `अवशेष का खतरा: कटाई में केवल ${days} दिन शेष हैं (न्यूनतम प्रतीक्षा: ${phi} दिन)। स्प्रे न करें; उपयुक्त जैविक विकल्प चुनें।`, labelDirections: "उत्पाद लेबल और स्थानीय कृषि सलाह के अनुसार ही उपयोग करें।", phiDays: (days) => `कटाई-पूर्व अंतराल: ${days} दिन`, loading: "लोड हो रहा है…", compatibilityTip: "उत्पाद मिलाने से पहले लेबल निर्देश और स्थानीय कृषि सलाह का पालन करें।",
  },
  mr: {},
  bn: {
    analysisSubtitle: "AI-সহায়িত উদ্ভিদ মূল্যায়ন", treatmentPackage: "ICAR ও CIBRC অনুযায়ী ফসল সুরক্ষা প্যাকেজ", verified: "ICAR / CIBRC যাচাইকৃত", fieldReady: "খেতের জন্য ব্যবহারযোগ্য", targetedCurative: "লক্ষ্যভিত্তিক চিকিৎসা", ecoSafe: "পরিবেশবান্ধব জৈব নিয়ন্ত্রণ", safeFoodHint: "ফসল কাটার আগের বিরতি অবশিষ্টাংশ এড়াতে এবং খাবার নিরাপদ রাখতে সাহায্য করে।", residueHazard: (days, phi) => `অবশিষ্টাংশের ঝুঁকি: ফসল কাটতে মাত্র ${days} দিন বাকি (ন্যূনতম অপেক্ষা: ${phi} দিন)। স্প্রে করবেন না; উপযুক্ত জৈব বিকল্প নিন।`, labelDirections: "পণ্যের লেবেল ও স্থানীয় কৃষি পরামর্শ অনুযায়ী ব্যবহার করুন।", phiDays: (days) => `ফসল কাটার পূর্ববর্তী বিরতি: ${days} দিন`, loading: "লোড হচ্ছে…", compatibilityTip: "পণ্য মেশানোর আগে লেবেলের নির্দেশ ও স্থানীয় কৃষি পরামর্শ মেনে চলুন।",
  },
  ta: {
    analysisSubtitle: "AI உதவியுடன் தாவர மதிப்பீடு", treatmentPackage: "ICAR மற்றும் CIBRC வழிகாட்டுதலுடன் பயிர் பாதுகாப்புத் தொகுப்பு", verified: "ICAR / CIBRC சரிபார்க்கப்பட்டது", fieldReady: "பண்ணைக்கு ஏற்றது", targetedCurative: "இலக்கு சிகிச்சை", ecoSafe: "சூழலுக்கு உகந்த உயிரியல் கட்டுப்பாடு", safeFoodHint: "அறுவடைக்கு முன் இடைவெளி எச்சங்களைத் தவிர்த்து உணவைப் பாதுகாக்க உதவுகிறது.", residueHazard: (days, phi) => `எச்ச அபாயம்: அறுவடைக்கு ${days} நாட்கள் மட்டுமே உள்ளன (குறைந்தபட்ச காத்திருப்பு: ${phi} நாட்கள்). தெளிக்க வேண்டாம்; பொருத்தமான உயிரியல் மாற்றைத் தேர்ந்தெடுக்கவும்.`, labelDirections: "பொருள் லேபிள் மற்றும் உள்ளூர் வேளாண் வழிகாட்டுதலின்படி மட்டுமே பயன்படுத்தவும்.", phiDays: (days) => `அறுவடைக்கு முன் இடைவெளி: ${days} நாட்கள்`, loading: "ஏற்றப்படுகிறது…", compatibilityTip: "பொருட்களை கலப்பதற்கு முன் லேபிள் வழிமுறைகளையும் உள்ளூர் வேளாண் ஆலோசனையையும் பின்பற்றவும்.",
  },
  te: {
    analysisSubtitle: "AI సహాయంతో మొక్కల అంచనా", treatmentPackage: "ICAR మరియు CIBRC మార్గదర్శకాలతో పంట రక్షణ ప్యాకేజీ", verified: "ICAR / CIBRC ధృవీకరించబడింది", fieldReady: "పొలం కోసం ఉపయోగకరం", targetedCurative: "లక్ష్యిత చికిత్స", ecoSafe: "పర్యావరణ అనుకూల జీవ నియంత్రణ", safeFoodHint: "కోతకు ముందు విరామం అవశేషాలను నివారించి ఆహార భద్రతకు సహాయపడుతుంది.", residueHazard: (days, phi) => `అవశేషాల ప్రమాదం: కోతకు ఇంకా ${days} రోజులు మాత్రమే ఉన్నాయి (కనీస నిరీక్షణ: ${phi} రోజులు). స్ప్రే చేయవద్దు; సరైన జీవ నియంత్రణ ఎంపికను ఎంచుకోండి.`, labelDirections: "ఉత్పత్తి లేబుల్ మరియు స్థానిక వ్యవసాయ మార్గదర్శకాల ప్రకారం మాత్రమే ఉపయోగించండి.", phiDays: (days) => `కోతకు ముందు విరామం: ${days} రోజులు`, loading: "లోడ్ అవుతోంది…", compatibilityTip: "ఉత్పత్తులను కలపడానికి ముందు లేబుల్ సూచనలు మరియు స్థానిక వ్యవసాయ సలహాను పాటించండి.",
  },
};

export function interfaceText(language) {
  return {
    ...COPY.en,
    ...(COPY[language] || {}),
    ...COMPLETE.en,
    ...(COMPLETE[language] || {}),
    ...EXTRA.en,
    ...(EXTRA[language] || {}),
    ...DETAIL.en,
    ...(DETAIL[language] || {}),
  };
}

export function localizedForecastBadge(value, language) {
  const text = String(value || "").toLowerCase();
  if (text.includes("फवारणी") || text.includes("optimal") || text.includes("spray")) return interfaceText(language).optimal;
  return value || "";
}

export function localizedDay(value, language) {
  const suffix = String(value || "").replace(/^day\s*/i, "");
  return suffix ? `${interfaceText(language).day} ${suffix}` : value;
}

const CROP_NAMES = {
  en: ["All Crops", "Tomato", "Grapes", "Potato", "Soybean", "Corn", "Apple", "Capsicum"],
  hi: ["सभी फसलें", "टमाटर", "अंगूर", "आलू", "सोयाबीन", "मक्का", "सेब", "शिमला मिर्च"],
  bn: ["সব ফসল", "টমেটো", "আঙুর", "আলু", "সয়াবিন", "ভুট্টা", "আপেল", "ক্যাপসিকাম"],
  ta: ["அனைத்து பயிர்கள்", "தக்காளி", "திராட்சை", "உருளைக்கிழங்கு", "சோயாபீன்", "மக்காச்சோளம்", "ஆப்பிள்", "குடைமிளகாய்"],
  te: ["అన్ని పంటలు", "టమాటా", "ద్రాక్ష", "బంగాళాదుంప", "సోయాబీన్", "మొక్కజొన్న", "ఆపిల్", "క్యాప్సికం"],
};

const DISTRICTS = {
  hi: { Pune: "पुणे", Nashik: "नासिक", Sangli: "सांगली", Kolhapur: "कोल्हापुर", Narayangaon: "नारायणगांव", Solapur: "सोलापुर", Ahmednagar: "अहमदनगर", Satara: "सतारा", Nagpur: "नागपुर", Amravati: "अमरावती", Jalgaon: "जलगांव", Baramati: "बारामती" },
  bn: { Pune: "পুনে", Nashik: "নাসিক", Sangli: "সাংলি", Kolhapur: "কোলহাপুর", Solapur: "সোলাপুর", Nagpur: "নাগপুর" },
  ta: { Pune: "புனே", Nashik: "நாசிக்", Sangli: "சாங்லி", Kolhapur: "கோலாப்பூர்", Solapur: "சோலாப்பூர்", Nagpur: "நாக்பூர்" },
  te: { Pune: "పూణే", Nashik: "నాసిక్", Sangli: "సాంగ్లీ", Kolhapur: "కొల్హాపూర్", Solapur: "సోలాపూర్", Nagpur: "నాగపూర్" },
};

export function localizedCropName(index, language, fallback) {
  return CROP_NAMES[language]?.[index] || fallback;
}

export function localizedDistrictName(value, language) {
  const text = String(value || "");
  const baseName = text.replace(/\s*\([^)]*\)/g, "").split(" - ")[0].trim();
  if (language === "en" || language === "mr") return baseName;
  const match = Object.entries(DISTRICTS[language] || {}).find(([name]) => baseName.startsWith(name));
  return match ? baseName.replace(match[0], match[1]) : baseName;
}

export function localizedKendraType(value, language) {
  if (language === "en" || language === "mr") return value;
  const type = String(value || "").toLowerCase();
  const values = {
    hi: type.includes("government") ? "सरकारी सहकारी केंद्र" : "अधिकृत विक्रेता", bn: type.includes("government") ? "সরকারি সমবায় কেন্দ্র" : "অনুমোদিত বিক্রেতা", ta: type.includes("government") ? "அரசு கூட்டுறவு மையம்" : "அங்கீகரிக்கப்பட்ட விற்பனையாளர்", te: type.includes("government") ? "ప్రభుత్వ సహకార కేంద్రం" : "అధీకృత డీలర్",
  };
  return values[language] || value;
}

export function localizedCompatibilityTitle(status, language) {
  if (language === "en" || language === "mr") return status || "";
  const labels = {
    hi: { COMPATIBLE: "मिश्रण के लिए सुरक्षित", SAME_CHEMICAL: "एक ही उत्पाद चुना गया", CAUTION: "सावधानी आवश्यक", INCOMPATIBLE: "मिश्रण असंगत है", DANGEROUS: "मिश्रण खतरनाक है", REDUNDANT: "अनावश्यक मिश्रण" },
    bn: { COMPATIBLE: "মেশানোর জন্য নিরাপদ", SAME_CHEMICAL: "একই পণ্য নির্বাচিত", CAUTION: "সতর্কতা প্রয়োজন", INCOMPATIBLE: "মিশ্রণ অসামঞ্জস্যপূর্ণ", DANGEROUS: "মিশ্রণ বিপজ্জনক", REDUNDANT: "অপ্রয়োজনীয় মিশ্রণ" },
    ta: { COMPATIBLE: "கலக்க பாதுகாப்பானது", SAME_CHEMICAL: "ஒரே பொருள் தேர்ந்தெடுக்கப்பட்டது", CAUTION: "எச்சரிக்கை தேவை", INCOMPATIBLE: "கலவை பொருந்தாது", DANGEROUS: "கலவை ஆபத்தானது", REDUNDANT: "தேவையற்ற கலவை" },
    te: { COMPATIBLE: "కలపడానికి సురక్షితం", SAME_CHEMICAL: "అదే ఉత్పత్తి ఎంచుకోబడింది", CAUTION: "జాగ్రత్త అవసరం", INCOMPATIBLE: "మిశ్రమం అనుకూలం కాదు", DANGEROUS: "మిశ్రమం ప్రమాదకరం", REDUNDANT: "అనవసరమైన మిశ్రమం" },
  };
  return labels[language]?.[status] || status || "";
}

const TABS = {
  en: ["Diagnosis", "Spray & Tank-Mix", "7-Day Risk", "Mandi & Dealers", "Recovery"],
  hi: ["रोग निदान", "स्प्रे एवं मिश्रण", "7-दिन जोखिम", "मंडी व केंद्र", "सुधार ट्रैकर"],
  mr: ["रोग निदान", "फवारणी व मिश्रण", "हवामान अंदाज", "बाजारभाव व केंद्रे", "सुधारणा ट्रॅकर"],
  bn: ["রোগ নির্ণয়", "স্প্রে ও মিশ্রণ", "৭ দিনের ঝুঁকি", "বাজার ও কেন্দ্র", "পুনরুদ্ধার"],
  ta: ["நோய் கண்டறிதல்", "தெளிப்பு மற்றும் கலவை", "7 நாள் ஆபத்து", "சந்தை மற்றும் மையங்கள்", "மீட்பு"],
  te: ["వ్యాధి నిర్ధారణ", "స్ప్రే మరియు మిశ్రమం", "7 రోజుల ప్రమాదం", "మార్కెట్ మరియు కేంద్రాలు", "కోలుకోవడం"],
};

export function tabText(language, index) {
  return (TABS[language] || TABS.en)[index];
}
