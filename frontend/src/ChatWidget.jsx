
import { useEffect, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ChatWidget.css";
// import { LANGUAGES } from "./translations";

const API_URL = "http://127.0.0.1:8000/chat";

const CHAT_STORAGE_KEY = "plantHealthChat.messages.v1";
const CHAT_LANGUAGE_KEY = "plantHealthChat.language.v1";

const MAX_STORED_MESSAGES = 50;
const MAX_REQUEST_MESSAGES = 10;



const UI_TEXT = {
  en: {
    title: "Plant Health Assistant",
    subtitle: "Your AI gardening companion",
    greeting: "Hi! 🌱 Ask me about plant diseases, symptoms, prevention, or crop care.",
    placeholder: "Ask about your plants...",
    send: "Send",
    newChat: "New chat",
    language: "Language",
    thinking: "Thinking...",
    close: "Close chat",
    open: "Open plant health assistant",
    error: "Something went wrong. Please try again.",
    footer: "AI advice can be imperfect. Verify important diagnoses.",
    powered: "Powered by Groq",
    currentAnalysis: "Current analysis",
    quickPrompts: "Quick questions",
    explainResult: "Explain this result",
    nextSteps: "What should I do next?",
    prevention: "How can I prevent this disease?",
  },

  hi: {
    title: "पौधों का स्वास्थ्य सहायक",
    subtitle: "आपका AI बागवानी साथी",
    greeting: "नमस्ते! 🌱 पौधों की बीमारी, लक्षण, बचाव या देखभाल के बारे में पूछें।",
    placeholder: "अपने पौधों के बारे में पूछें...",
    send: "भेजें",
    newChat: "नई बातचीत",
    language: "भाषा",
    thinking: "सोच रहा है...",
    close: "चैट बंद करें",
    open: "पौधों का सहायक खोलें",
    error: "कुछ गड़बड़ हुई। कृपया दोबारा प्रयास करें।",
    footer: "AI की सलाह गलत हो सकती है। महत्वपूर्ण निदान की पुष्टि करें।",
    powered: "Groq द्वारा संचालित",
    currentAnalysis: "वर्तमान विश्लेषण",
    quickPrompts: "कुछ सवाल पूछें",
    explainResult: "इस परिणाम को समझाएँ",
    nextSteps: "अब मुझे क्या करना चाहिए?",
    prevention: "इस बीमारी से कैसे बचें?",
  },

  mr: {
    title: "वनस्पती आरोग्य सहाय्यक",
    subtitle: "तुमचा AI बागकाम साथी",
    greeting: "नमस्कार! 🌱 वनस्पतींचे रोग, लक्षणे, प्रतिबंध किंवा पिकांची काळजी याबद्दल विचारा.",
    placeholder: "तुमच्या वनस्पतींबद्दल विचारा...",
    send: "पाठवा",
    newChat: "नवीन संभाषण",
    language: "भाषा",
    thinking: "विचार करत आहे...",
    close: "चॅट बंद करा",
    open: "वनस्पती आरोग्य सहाय्यक उघडा",
    error: "काहीतरी चूक झाली. पुन्हा प्रयत्न करा.",
    footer: "AI चा सल्ला चुकीचा असू शकतो. महत्त्वाच्या निदानाची खात्री करा.",
    powered: "Groq द्वारे समर्थित",
    currentAnalysis: "सध्याचे विश्लेषण",
    quickPrompts: "काही प्रश्न विचारा",
    explainResult: "हा निकाल समजावून सांगा",
    nextSteps: "आता मी काय करावे?",
    prevention: "हा रोग कसा टाळता येईल?",
  },

  bn: {
    title: "উদ্ভিদের স্বাস্থ্য সহায়ক",
    subtitle: "আপনার AI বাগানসঙ্গী",
    greeting: "নমস্কার! 🌱 গাছের রোগ, লক্ষণ, প্রতিরোধ বা ফসলের যত্ন সম্পর্কে জিজ্ঞাসা করুন।",
    placeholder: "আপনার গাছপালা সম্পর্কে জিজ্ঞাসা করুন...",
    send: "পাঠান",
    newChat: "নতুন চ্যাট",
    language: "ভাষা",
    thinking: "ভাবছি...",
    close: "চ্যাট বন্ধ করুন",
    open: "উদ্ভিদের সহায়ক খুলুন",
    error: "কিছু সমস্যা হয়েছে। আবার চেষ্টা করুন।",
    footer: "AI-এর পরামর্শ ভুল হতে পারে। গুরুত্বপূর্ণ রোগনির্ণয় যাচাই করুন।",
    powered: "Groq দ্বারা পরিচালিত",
    currentAnalysis: "বর্তমান বিশ্লেষণ",
    quickPrompts: "দ্রুত প্রশ্ন",
    explainResult: "এই ফলাফলটি বুঝিয়ে দিন",
    nextSteps: "এখন আমার কী করা উচিত?",
    prevention: "এই রোগ কীভাবে প্রতিরোধ করব?",
  },

  te: {
    title: "మొక్కల ఆరోగ్య సహాయకుడు",
    subtitle: "మీ AI తోటల సహచరుడు",
    greeting: "నమస్కారం! 🌱 మొక్కల వ్యాధులు, లక్షణాలు, నివారణ లేదా పంట సంరక్షణ గురించి అడగండి.",
    placeholder: "మీ మొక్కల గురించి అడగండి...",
    send: "పంపండి",
    newChat: "కొత్త సంభాషణ",
    language: "భాష",
    thinking: "ఆలోచిస్తున్నాను...",
    close: "చాట్‌ను మూసివేయండి",
    open: "మొక్కల సహాయకుడిని తెరవండి",
    error: "ఏదో సమస్య వచ్చింది. మళ్లీ ప్రయత్నించండి.",
    footer: "AI సలహా తప్పుగా ఉండవచ్చు. ముఖ్యమైన నిర్ధారణలను ధృవీకరించండి.",
    powered: "Groq ద్వారా నడుస్తుంది",
    currentAnalysis: "ప్రస్తుత విశ్లేషణ",
    quickPrompts: "త్వరిత ప్రశ్నలు",
    explainResult: "ఈ ఫలితాన్ని వివరించండి",
    nextSteps: "ఇప్పుడు నేను ఏమి చేయాలి?",
    prevention: "ఈ వ్యాధిని ఎలా నివారించాలి?",
  },

  ta: {
    title: "தாவர நல உதவியாளர்",
    subtitle: "உங்கள் AI தோட்டப் பராமரிப்பு துணை",
    greeting: "வணக்கம்! 🌱 தாவர நோய்கள், அறிகுறிகள், தடுப்பு அல்லது பயிர் பராமரிப்பு பற்றி கேளுங்கள்.",
    placeholder: "உங்கள் தாவரங்களைப் பற்றி கேளுங்கள்...",
    send: "அனுப்பு",
    newChat: "புதிய உரையாடல்",
    language: "மொழி",
    thinking: "சிந்திக்கிறது...",
    close: "உரையாடலை மூடு",
    open: "தாவர உதவியாளரைத் திற",
    error: "ஏதோ தவறு ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
    footer: "AI ஆலோசனை தவறாக இருக்கலாம். முக்கியமான நோயறிதல்களைச் சரிபார்க்கவும்.",
    powered: "Groq மூலம் இயங்குகிறது",
    currentAnalysis: "தற்போதைய பகுப்பாய்வு",
    quickPrompts: "விரைவான கேள்விகள்",
    explainResult: "இந்த முடிவை விளக்கவும்",
    nextSteps: "இப்போது நான் என்ன செய்ய வேண்டும்?",
    prevention: "இந்த நோயை எவ்வாறு தடுப்பது?",
  },

  gu: {
    title: "છોડના સ્વાસ્થ્ય સહાયક",
    subtitle: "તમારો AI બાગકામ સાથી",
    greeting: "નમસ્તે! 🌱 છોડના રોગો, લક્ષણો, નિવારણ અથવા પાકની સંભાળ વિશે પૂછો.",
    placeholder: "તમારા છોડ વિશે પૂછો...",
    send: "મોકલો",
    newChat: "નવી વાતચીત",
    language: "ભાષા",
    thinking: "વિચારી રહ્યું છે...",
    close: "ચેટ બંધ કરો",
    open: "છોડનો સહાયક ખોલો",
    error: "કંઈક ખોટું થયું. ફરી પ્રયાસ કરો.",
    footer: "AIની સલાહ ખોટી હોઈ શકે છે. મહત્વપૂર્ણ નિદાનની પુષ્ટિ કરો.",
    powered: "Groq દ્વારા સંચાલિત",
    currentAnalysis: "વર્તમાન વિશ્લેષણ",
    quickPrompts: "ઝડપી પ્રશ્નો",
    explainResult: "આ પરિણામ સમજાવો",
    nextSteps: "હવે મારે શું કરવું?",
    prevention: "આ રોગને કેવી રીતે અટકાવવો?",
  },

  kn: {
    title: "ಸಸ್ಯ ಆರೋಗ್ಯ ಸಹಾಯಕ",
    subtitle: "ನಿಮ್ಮ AI ತೋಟಗಾರಿಕೆ ಸಂಗಾತಿ",
    greeting: "ನಮಸ್ಕಾರ! 🌱 ಸಸ್ಯ ರೋಗಗಳು, ಲಕ್ಷಣಗಳು, ತಡೆಗಟ್ಟುವಿಕೆ ಅಥವಾ ಬೆಳೆ ಆರೈಕೆಯ ಬಗ್ಗೆ ಕೇಳಿ.",
    placeholder: "ನಿಮ್ಮ ಸಸ್ಯಗಳ ಬಗ್ಗೆ ಕೇಳಿ...",
    send: "ಕಳುಹಿಸಿ",
    newChat: "ಹೊಸ ಸಂಭಾಷಣೆ",
    language: "ಭಾಷೆ",
    thinking: "ಯೋಚಿಸುತ್ತಿದೆ...",
    close: "ಚಾಟ್ ಮುಚ್ಚಿ",
    open: "ಸಸ್ಯ ಸಹಾಯಕವನ್ನು ತೆರೆಯಿರಿ",
    error: "ಏನೋ ತಪ್ಪಾಗಿದೆ. ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ.",
    footer: "AI ಸಲಹೆ ತಪ್ಪಾಗಿರಬಹುದು. ಮುಖ್ಯ ರೋಗನಿರ್ಣಯವನ್ನು ಪರಿಶೀಲಿಸಿ.",
    powered: "Groq ಮೂಲಕ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತದೆ",
    currentAnalysis: "ಪ್ರಸ್ತುತ ವಿಶ್ಲೇಷಣೆ",
    quickPrompts: "ತ್ವರಿತ ಪ್ರಶ್ನೆಗಳು",
    explainResult: "ಈ ಫಲಿತಾಂಶವನ್ನು ವಿವರಿಸಿ",
    nextSteps: "ಈಗ ನಾನು ಏನು ಮಾಡಬೇಕು?",
    prevention: "ಈ ರೋಗವನ್ನು ಹೇಗೆ ತಡೆಯಬಹುದು?",
  },

  ml: {
    title: "സസ്യ ആരോഗ്യ സഹായി",
    subtitle: "നിങ്ങളുടെ AI തോട്ടപരിപാലന കൂട്ടുകാരൻ",
    greeting: "നമസ്കാരം! 🌱 സസ്യരോഗങ്ങൾ, ലക്ഷണങ്ങൾ, പ്രതിരോധം, വിളപരിപാലനം എന്നിവയെക്കുറിച്ച് ചോദിക്കൂ.",
    placeholder: "നിങ്ങളുടെ ചെടികളെക്കുറിച്ച് ചോദിക്കൂ...",
    send: "അയയ്ക്കുക",
    newChat: "പുതിയ സംഭാഷണം",
    language: "ഭാഷ",
    thinking: "ചിന്തിക്കുന്നു...",
    close: "ചാറ്റ് അടയ്ക്കുക",
    open: "സസ്യ സഹായിയെ തുറക്കുക",
    error: "ഒരു പ്രശ്നം സംഭവിച്ചു. വീണ്ടും ശ്രമിക്കുക.",
    footer: "AI ഉപദേശം തെറ്റായിരിക്കാം. പ്രധാനപ്പെട്ട രോഗനിർണയങ്ങൾ സ്ഥിരീകരിക്കുക.",
    powered: "Groq ഉപയോഗിച്ച് പ്രവർത്തിക്കുന്നു",
    currentAnalysis: "നിലവിലെ വിശകലനം",
    quickPrompts: "വേഗത്തിലുള്ള ചോദ്യങ്ങൾ",
    explainResult: "ഈ ഫലം വിശദീകരിക്കൂ",
    nextSteps: "ഇനി ഞാൻ എന്ത് ചെയ്യണം?",
    prevention: "ഈ രോഗം എങ്ങനെ തടയാം?",
  },

  pa: {
    title: "ਪੌਦਿਆਂ ਦੀ ਸਿਹਤ ਸਹਾਇਕ",
    subtitle: "ਤੁਹਾਡਾ AI ਬਾਗਬਾਨੀ ਸਾਥੀ",
    greeting: "ਸਤ ਸ੍ਰੀ ਅਕਾਲ! 🌱 ਪੌਦਿਆਂ ਦੀਆਂ ਬਿਮਾਰੀਆਂ, ਲੱਛਣਾਂ, ਰੋਕਥਾਮ ਜਾਂ ਫ਼ਸਲ ਦੀ ਦੇਖਭਾਲ ਬਾਰੇ ਪੁੱਛੋ।",
    placeholder: "ਆਪਣੇ ਪੌਦਿਆਂ ਬਾਰੇ ਪੁੱਛੋ...",
    send: "ਭੇਜੋ",
    newChat: "ਨਵੀਂ ਗੱਲਬਾਤ",
    language: "ਭਾਸ਼ਾ",
    thinking: "ਸੋਚ ਰਿਹਾ ਹੈ...",
    close: "ਚੈਟ ਬੰਦ ਕਰੋ",
    open: "ਪੌਦਿਆਂ ਦਾ ਸਹਾਇਕ ਖੋਲ੍ਹੋ",
    error: "ਕੁਝ ਗਲਤ ਹੋਇਆ। ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ।",
    footer: "AI ਦੀ ਸਲਾਹ ਗਲਤ ਹੋ ਸਕਦੀ ਹੈ। ਮਹੱਤਵਪੂਰਨ ਨਿਦਾਨ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ।",
    powered: "Groq ਦੁਆਰਾ ਸੰਚਾਲਿਤ",
    currentAnalysis: "ਮੌਜੂਦਾ ਵਿਸ਼ਲੇਸ਼ਣ",
    quickPrompts: "ਤੁਰੰਤ ਸਵਾਲ",
    explainResult: "ਇਸ ਨਤੀਜੇ ਨੂੰ ਸਮਝਾਓ",
    nextSteps: "ਹੁਣ ਮੈਨੂੰ ਕੀ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ?",
    prevention: "ਇਸ ਬਿਮਾਰੀ ਨੂੰ ਕਿਵੇਂ ਰੋਕਿਆ ਜਾ ਸਕਦਾ ਹੈ?",
  },

  or: {
    title: "ଗଛ ସ୍ୱାସ୍ଥ୍ୟ ସହାୟକ",
    subtitle: "ଆପଣଙ୍କ AI ବଗିଚା ସାଥୀ",
    greeting: "ନମସ୍କାର! 🌱 ଗଛର ରୋଗ, ଲକ୍ଷଣ, ପ୍ରତିରୋଧ କିମ୍ବା ଫସଲର ଯତ୍ନ ବିଷୟରେ ପଚାରନ୍ତୁ।",
    placeholder: "ଆପଣଙ୍କ ଗଛ ବିଷୟରେ ପଚାରନ୍ତୁ...",
    send: "ପଠାନ୍ତୁ",
    newChat: "ନୂଆ କଥାବାର୍ତ୍ତା",
    language: "ଭାଷା",
    thinking: "ଚିନ୍ତା କରୁଛି...",
    close: "ଚାଟ୍ ବନ୍ଦ କରନ୍ତୁ",
    open: "ଗଛ ସହାୟକ ଖୋଲନ୍ତୁ",
    error: "କିଛି ତ୍ରୁଟି ହୋଇଛି। ପୁଣି ଚେଷ୍ଟା କରନ୍ତୁ।",
    footer: "AI ପରାମର୍ଶ ଭୁଲ ହୋଇପାରେ। ଗୁରୁତ୍ୱପୂର୍ଣ୍ଣ ରୋଗନିର୍ଣ୍ଣୟ ଯାଞ୍ଚ କରନ୍ତୁ।",
    powered: "Groq ଦ୍ୱାରା ପରିଚାଳିତ",
    currentAnalysis: "ବର୍ତ୍ତମାନ ବିଶ୍ଳେଷଣ",
    quickPrompts: "ତୁରନ୍ତ ପ୍ରଶ୍ନ",
    explainResult: "ଏହି ଫଳାଫଳ ବୁଝାନ୍ତୁ",
    nextSteps: "ଏବେ ମୁଁ କ'ଣ କରିବି?",
    prevention: "ଏହି ରୋଗକୁ କିପରି ରୋକିବି?",
  },

  ur: {
    title: "پودوں کی صحت کا معاون",
    subtitle: "آپ کا AI باغبانی ساتھی",
    greeting: "السلام علیکم! 🌱 پودوں کی بیماریوں، علامات، بچاؤ یا فصل کی دیکھ بھال کے بارے میں پوچھیں۔",
    placeholder: "اپنے پودوں کے بارے میں پوچھیں...",
    send: "بھیجیں",
    newChat: "نئی گفتگو",
    language: "زبان",
    thinking: "سوچ رہا ہے...",
    close: "چیٹ بند کریں",
    open: "پودوں کا معاون کھولیں",
    error: "کچھ غلط ہوا۔ دوبارہ کوشش کریں۔",
    footer: "AI کا مشورہ غلط ہو سکتا ہے۔ اہم تشخیص کی تصدیق کریں۔",
    powered: "Groq کے ذریعے",
    currentAnalysis: "موجودہ تجزیہ",
    quickPrompts: "فوری سوالات",
    explainResult: "اس نتیجے کی وضاحت کریں",
    nextSteps: "اب مجھے کیا کرنا چاہیے؟",
    prevention: "اس بیماری کو کیسے روکوں؟",
  },

  as: {
    title: "উদ্ভিদ স্বাস্থ্য সহায়ক",
    subtitle: "আপোনাৰ AI বাগিচাৰ সংগী",
    greeting: "নমস্কাৰ! 🌱 উদ্ভিদৰ ৰোগ, লক্ষণ, প্ৰতিৰোধ বা শস্যৰ যত্নৰ বিষয়ে সোধক।",
    placeholder: "আপোনাৰ উদ্ভিদৰ বিষয়ে সোধক...",
    send: "পঠিয়াওক",
    newChat: "নতুন কথোপকথন",
    language: "ভাষা",
    thinking: "ভাবি আছে...",
    close: "চেট বন্ধ কৰক",
    open: "উদ্ভিদ সহায়ক খোলক",
    error: "কিবা ভুল হৈছে। পুনৰ চেষ্টা কৰক।",
    footer: "AIৰ পৰামৰ্শ ভুল হ'ব পাৰে। গুৰুত্বপূৰ্ণ ৰোগ নিৰ্ণয় নিশ্চিত কৰক।",
    powered: "Groqৰ দ্বাৰা চালিত",
    currentAnalysis: "বৰ্তমানৰ বিশ্লেষণ",
    quickPrompts: "দ্ৰুত প্ৰশ্ন",
    explainResult: "এই ফলাফলটো বুজাই দিয়ক",
    nextSteps: "এতিয়া মই কি কৰিব লাগে?",
    prevention: "এই ৰোগ কেনেকৈ প্ৰতিৰোধ কৰিব পাৰি?",
  },

  ne: {
    title: "बिरुवा स्वास्थ्य सहायक",
    subtitle: "तपाईंको AI बगैँचा साथी",
    greeting: "नमस्कार! 🌱 बिरुवाका रोग, लक्षण, रोकथाम वा बालीको हेरचाहबारे सोध्नुहोस्।",
    placeholder: "आफ्ना बिरुवाबारे सोध्नुहोस्...",
    send: "पठाउनुहोस्",
    newChat: "नयाँ कुराकानी",
    language: "भाषा",
    thinking: "सोच्दैछ...",
    close: "च्याट बन्द गर्नुहोस्",
    open: "बिरुवा सहायक खोल्नुहोस्",
    error: "केही समस्या भयो। कृपया फेरि प्रयास गर्नुहोस्।",
    footer: "AI को सल्लाह गलत हुन सक्छ। महत्त्वपूर्ण निदान पुष्टि गर्नुहोस्।",
    powered: "Groq द्वारा सञ्चालित",
    currentAnalysis: "हालको विश्लेषण",
    quickPrompts: "छिटो प्रश्नहरू",
    explainResult: "यो नतिजा बुझाउनुहोस्",
    nextSteps: "अब मैले के गर्नुपर्छ?",
    prevention: "यो रोग कसरी रोक्न सकिन्छ?",
  },
};


// =========================================
// Quick question messages
// =========================================

const QUICK_MESSAGES = {
  en: {
    explain: "Please explain my current plant analysis, the predicted condition, and confidence score in simple language.",
    next: "Based on my current plant analysis, what practical steps should I take next?",
    prevent: "How can I prevent this condition from spreading and reduce the risk of it returning?",
  },

  hi: {
    explain: "मेरे वर्तमान पौधे के विश्लेषण, अनुमानित बीमारी और confidence score को सरल भाषा में समझाएँ।",
    next: "मेरे पौधे के इस विश्लेषण के आधार पर मुझे अब कौन से व्यावहारिक कदम उठाने चाहिए?",
    prevent: "इस बीमारी को फैलने से कैसे रोकूँ और दोबारा होने का जोखिम कैसे कम करूँ?",
  },

  mr: {
    explain: "माझ्या सध्याच्या वनस्पती विश्लेषणात आढळलेला रोग आणि confidence score सोप्या भाषेत समजावून सांगा.",
    next: "माझ्या वनस्पतीच्या या विश्लेषणानुसार मी आता कोणती व्यावहारिक पावले उचलावीत?",
    prevent: "हा रोग पसरण्यापासून कसा रोखू आणि पुन्हा होण्याचा धोका कसा कमी करू?",
  },

  bn: {
    explain: "আমার বর্তমান উদ্ভিদ বিশ্লেষণ, অনুমান করা রোগ এবং confidence score সহজ ভাষায় বুঝিয়ে দিন।",
    next: "আমার গাছের এই বিশ্লেষণের ভিত্তিতে এখন কী কী পদক্ষেপ নেওয়া উচিত?",
    prevent: "এই রোগ ছড়ানো কীভাবে আটকাব এবং আবার হওয়ার ঝুঁকি কীভাবে কমাব?",
  },

  te: {
    explain: "నా మొక్క విశ్లేషణ, అంచనా వేసిన వ్యాధి మరియు confidence score ను సరళంగా వివరించండి.",
    next: "నా మొక్క విశ్లేషణ ఆధారంగా నేను ఇప్పుడు ఏ చర్యలు తీసుకోవాలి?",
    prevent: "ఈ వ్యాధి వ్యాప్తిని ఎలా అడ్డుకోవాలి, మళ్లీ వచ్చే ప్రమాదాన్ని ఎలా తగ్గించాలి?",
  },

  ta: {
    explain: "எனது தாவரப் பகுப்பாய்வு, கணிக்கப்பட்ட நோய் மற்றும் confidence score-ஐ எளிமையாக விளக்கவும்.",
    next: "இந்தப் பகுப்பாய்வின் அடிப்படையில் நான் அடுத்து என்ன செய்ய வேண்டும்?",
    prevent: "இந்த நோய் பரவுவதை எவ்வாறு தடுப்பது, மீண்டும் வரும் அபாயத்தை எவ்வாறு குறைப்பது?",
  },

  gu: {
    explain: "મારા છોડના વિશ્લેષણ, અનુમાનિત રોગ અને confidence score ને સરળ ભાષામાં સમજાવો.",
    next: "મારા છોડના આ વિશ્લેષણના આધારે હવે મારે કયા પગલાં લેવા જોઈએ?",
    prevent: "આ રોગને ફેલાતો કેવી રીતે અટકાવવો અને ફરી થવાનું જોખમ કેવી રીતે ઘટાડવું?",
  },

  kn: {
    explain: "ನನ್ನ ಸಸ್ಯದ ವಿಶ್ಲೇಷಣೆ, ಊಹಿಸಲಾದ ರೋಗ ಮತ್ತು confidence score ಅನ್ನು ಸರಳವಾಗಿ ವಿವರಿಸಿ.",
    next: "ಈ ವಿಶ್ಲೇಷಣೆಯ ಆಧಾರದ ಮೇಲೆ ನಾನು ಮುಂದೇನು ಮಾಡಬೇಕು?",
    prevent: "ಈ ರೋಗ ಹರಡುವುದನ್ನು ಹೇಗೆ ತಡೆಯಬಹುದು ಮತ್ತು ಮತ್ತೆ ಬರುವ ಅಪಾಯವನ್ನು ಹೇಗೆ ಕಡಿಮೆ ಮಾಡಬಹುದು?",
  },

  ml: {
    explain: "എന്റെ സസ്യ വിശകലനവും പ്രവചിച്ച രോഗവും confidence score-ഉം ലളിതമായി വിശദീകരിക്കൂ.",
    next: "ഈ വിശകലനത്തിന്റെ അടിസ്ഥാനത്തിൽ ഞാൻ അടുത്തതായി എന്ത് ചെയ്യണം?",
    prevent: "ഈ രോഗം പടരുന്നത് എങ്ങനെ തടയാം, വീണ്ടും വരാനുള്ള സാധ്യത എങ്ങനെ കുറയ്ക്കാം?",
  },

  pa: {
    explain: "ਮੇਰੇ ਪੌਦੇ ਦੇ ਵਿਸ਼ਲੇਸ਼ਣ, ਅਨੁਮਾਨਿਤ ਬਿਮਾਰੀ ਅਤੇ confidence score ਨੂੰ ਸੌਖੀ ਭਾਸ਼ਾ ਵਿੱਚ ਸਮਝਾਓ।",
    next: "ਇਸ ਵਿਸ਼ਲੇਸ਼ਣ ਦੇ ਆਧਾਰ 'ਤੇ ਮੈਨੂੰ ਅੱਗੇ ਕੀ ਕਰਨਾ ਚਾਹੀਦਾ ਹੈ?",
    prevent: "ਇਸ ਬਿਮਾਰੀ ਨੂੰ ਫੈਲਣ ਤੋਂ ਕਿਵੇਂ ਰੋਕਣਾ ਹੈ ਅਤੇ ਮੁੜ ਆਉਣ ਦਾ ਖ਼ਤਰਾ ਕਿਵੇਂ ਘਟਾਉਣਾ ਹੈ?",
  },

  or: {
    explain: "ମୋ ଗଛର ବିଶ୍ଳେଷଣ, ଅନୁମାନିତ ରୋଗ ଏବଂ confidence score ସରଳ ଭାଷାରେ ବୁଝାନ୍ତୁ।",
    next: "ଏହି ବିଶ୍ଳେଷଣ ଆଧାରରେ ମୁଁ ପରେ କ'ଣ କରିବା ଉଚିତ?",
    prevent: "ଏହି ରୋଗ ବ୍ୟାପିବାକୁ କିପରି ରୋକିବି ଏବଂ ପୁଣି ହେବାର ଆଶଙ୍କା କିପରି କମାଇବି?",
  },

  ur: {
    explain: "میرے پودے کے موجودہ تجزیے، ممکنہ بیماری اور confidence score کو آسان زبان میں سمجھائیں۔",
    next: "اس تجزیے کی بنیاد پر مجھے اب کون سے عملی اقدامات کرنے چاہئیں؟",
    prevent: "اس بیماری کو پھیلنے سے کیسے روکوں اور دوبارہ ہونے کا خطرہ کیسے کم کروں؟",
  },

  as: {
    explain: "মোৰ উদ্ভিদৰ বিশ্লেষণ, অনুমান কৰা ৰোগ আৰু confidence score সহজ ভাষাত বুজাই দিয়ক।",
    next: "এই বিশ্লেষণৰ ভিত্তিত মই এতিয়া কি ব্যৱহাৰিক পদক্ষেপ লোৱা উচিত?",
    prevent: "এই ৰোগ বিয়পাটো কেনেকৈ ৰোধ কৰিম আৰু পুনৰ হোৱাৰ আশংকা কেনেকৈ কমাম?",
  },

  ne: {
    explain: "मेरो बिरुवाको विश्लेषण, अनुमान गरिएको रोग र confidence score सरल भाषामा बुझाउनुहोस्।",
    next: "यो विश्लेषणका आधारमा अब मैले के व्यावहारिक कदम चाल्नुपर्छ?",
    prevent: "यो रोग फैलिनबाट कसरी रोक्ने र फेरि हुने जोखिम कसरी घटाउने?",
  },
};


function getText(language) {
  return UI_TEXT[language] || UI_TEXT.en;
}

function getGreeting(language) {
  return getText(language).greeting;
}

function getSpeechLanguage(language) {
  const speechLocales = {
    auto: "en-IN",
    en: "en-IN",
    hi: "hi-IN",
    mr: "mr-IN",
    bn: "bn-IN",
    te: "te-IN",
    ta: "ta-IN",
    gu: "gu-IN",
    kn: "kn-IN",
    ml: "ml-IN",
    pa: "pa-IN",
    or: "or-IN",
    ur: "ur-IN",
    as: "as-IN",
    ne: "ne-NP",
    kok: "mr-IN",
    mai: "hi-IN",
    mni: "bn-IN",
    ks: "ur-IN",
    sd: "ur-IN",
    sa: "hi-IN",
    brx: "hi-IN",
    doi: "hi-IN",
    sat: "en-IN",
  };

  return speechLocales[language] || "en-IN";
}


function cleanTextForSpeech(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, " ")
    .replace(/`([^`]+)`/g, "$1")
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    .replace(/<br\s*\/?>/gi, ". ")
    .replace(/^\s{0,3}#{1,6}\s+/gm, "")
    .replace(/^\s*[-*+]\s+/gm, "")
    .replace(/^\s*\d+[.)]\s+/gm, "")
    .replace(/[*_~>|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}


function loadSavedLanguage() {
  try {
    const saved = localStorage.getItem(CHAT_LANGUAGE_KEY);

    if (LANGUAGES.some((item) => item.value === saved)) {
      return saved;
    }
  } catch {
    // Continue with the default language if storage is unavailable.
  }

  return "auto";
}


function loadSavedMessages() {
  try {
    const saved = localStorage.getItem(CHAT_STORAGE_KEY);

    if (saved) {
      const parsed = JSON.parse(saved);

      if (Array.isArray(parsed)) {
        const validMessages = parsed.filter(
          (message) =>
            message &&
            ["user", "assistant"].includes(message.role) &&
            typeof message.content === "string" &&
            message.content.trim().length > 0
        );

        if (validMessages.length > 0) {
          return validMessages.slice(-MAX_STORED_MESSAGES);
        }
      }
    }
  } catch {
    // Start a fresh conversation if saved data is invalid.
  }

  return [
    {
      role: "assistant",
      content: getGreeting(loadSavedLanguage()),
    },
  ];
}

function getQuickPrompts(language) {
  const text = getText(language);
  const messages = QUICK_MESSAGES[language] || QUICK_MESSAGES.en;

  return [
    {
      id: "explain",
      label: text.explainResult,
      message: messages.explain,
    },
    {
      id: "next",
      label: text.nextSteps,
      message: messages.next,
    },
    {
      id: "prevent",
      label: text.prevention,
      message: messages.prevent,
    },
  ];
}

function buildPlantContext(result) {
  if (!result || !result.plant || !result.disease) {
    return null;
  }

  return {
    plant: result.plant,
    disease: result.disease,
    confidence:
      typeof result.confidence === "number"
        ? result.confidence
        : undefined,
    confidence_status: result.confidence_status,
    description: result.description,
    symptoms: Array.isArray(result.symptoms)
      ? result.symptoms.slice(0, 5)
      : [],
    management: Array.isArray(result.management)
      ? result.management.slice(0, 5)
      : [],
    prevention: Array.isArray(result.prevention)
      ? result.prevention.slice(0, 5)
      : [],
    top_3: Array.isArray(result.top_3)
      ? result.top_3.slice(0, 3).map((item) => ({
        plant: item.plant,
        disease: item.disease,
        confidence: item.confidence,
      }))
      : [],
  };
}


export default function ChatWidget({ plantResult = null, language }) {
  // const setLanguage = onlanguagechange
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState(loadSavedMessages);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const recognitionRef = useRef(null);
  const voiceRestartTimerRef = useRef(null);
  const shouldKeepListeningRef = useRef(false);
  const [voiceDraft, setVoiceDraft] = useState("");
  const [speakingIndex, setSpeakingIndex] = useState(null);
  const [error, setError] = useState("");

  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  useEffect(() => {
    setMessages((previous) => {
      const userHasAsked = previous.some(
        (message) => message.role === "user"
      );

      if (userHasAsked) {
        return previous;
      }

      return [
        {
          role: "assistant",
          content: getGreeting(language),
        },
      ];
    });
  }, [language]);

  const text = getText(language);
  const plantContext = buildPlantContext(plantResult);
  const quickPrompts = getQuickPrompts(language);

  const hasAskedQuestion = messages.some(
    (message) => message.role === "user"
  );

  // Remember the selected language across page refreshes.
  useEffect(() => {
    try {
      localStorage.setItem(CHAT_LANGUAGE_KEY, language);
    } catch {
      console.warn("Could not save the chatbot language.");
    }
  }, [language]);


  // Keep recent messages in the browser.
  useEffect(() => {
    try {
      const savedMessages = messages
        .filter(
          (message) =>
            message &&
            ["user", "assistant"].includes(message.role) &&
            typeof message.content === "string"
        )
        .slice(-MAX_STORED_MESSAGES);

      localStorage.setItem(
        CHAT_STORAGE_KEY,
        JSON.stringify(savedMessages)
      );
    } catch {
      console.warn("Could not save chatbot conversation history.");
    }
  }, [messages]);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading, isOpen]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  const handleNewChat = () => {
    setMessages([
      {
        role: "assistant",
        content: getGreeting(language),
      },
    ]);
    setInput("");
    setError("");
  };

  const handleSend = async (messageOverride = null) => {
    const content = (
      typeof messageOverride === "string"
        ? messageOverride
        : input
    ).trim();

    if (!content || loading) return;

    const userMessage = {
      role: "user",
      content,
    };

    const requestMessages = [
      ...messages,
      userMessage,
    ].slice(-MAX_REQUEST_MESSAGES);

    setMessages((previous) => [
      ...previous,
      userMessage,
    ]);

    setInput("");
    setError("");
    setLoading(true);

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: requestMessages,
          language,
          plant_context: plantContext,
        }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(
          data.detail ||
          `Chat request failed (${response.status}).`
        );
      }

      if (
        typeof data.reply !== "string" ||
        !data.reply.trim()
      ) {
        throw new Error(
          "The chatbot returned an empty response."
        );
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);
    } catch (err) {
      console.error("Plant chatbot error:", err);
      setError(err.message || text.error);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (
      event.key === "Enter" &&
      !event.shiftKey
    ) {
      event.preventDefault();
      handleSend();
    }
  };


  const handleSpeak = (content, index) => {
    if (
      !("speechSynthesis" in window) ||
      typeof window.SpeechSynthesisUtterance === "undefined"
    ) {
      setError(
        "Spoken responses are not supported by this browser."
      );
      return;
    }

    // Pressing the button again stops the current speech.
    if (speakingIndex === index) {
      window.speechSynthesis.cancel();
      setSpeakingIndex(null);
      return;
    }

    // Only read one answer at a time.
    window.speechSynthesis.cancel();

    const textToSpeak = cleanTextForSpeech(content);

    if (!textToSpeak) return;

    const utterance = new window.SpeechSynthesisUtterance(
      textToSpeak
    );

    utterance.lang = getSpeechLanguage(language);
    utterance.rate = 0.9;
    utterance.pitch = 1;

    const voices = window.speechSynthesis.getVoices();
    const languageCode = utterance.lang.toLowerCase();

    const matchingVoice =
      voices.find(
        (voice) => voice.lang.toLowerCase() === languageCode
      ) ||
      voices.find(
        (voice) =>
          voice.lang.toLowerCase().startsWith(
            languageCode.split("-")[0] + "-"
          )
      );

    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    utterance.onend = () => {
      setSpeakingIndex(null);
    };

    utterance.onerror = () => {
      setSpeakingIndex(null);
    };

    setSpeakingIndex(index);
    window.speechSynthesis.speak(utterance);
  };




  const handleVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(
        "Voice input is not supported in this browser. Try Chrome or Edge."
      );
      return;
    }

    // Stop listening without immediately discarding unfinished words.
    if (isListening) {
      shouldKeepListeningRef.current = false;

      if (voiceRestartTimerRef.current !== null) {
        window.clearTimeout(voiceRestartTimerRef.current);
        voiceRestartTimerRef.current = null;
      }

      try {
        recognitionRef.current?.stop();
      } catch {
        setIsListening(false);
        setVoiceDraft("");
      }

      return;
    }

    const recognition = new SpeechRecognition();

    // Use the shared language map so voice input and speech output agree.
    recognition.lang = getSpeechLanguage(language);
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setError("");
    };

    recognition.onresult = (event) => {
      const finalParts = [];
      const interimParts = [];

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const result = event.results[i];
        const transcript = result[0]?.transcript?.trim();

        if (!transcript) continue;

        if (result.isFinal) {
          finalParts.push(transcript);
        } else {
          interimParts.push(transcript);
        }
      }

      // Keep finalized speech in the input box.
      const finalized = finalParts.join(" ").trim();

      if (finalized) {
        setInput((previous) =>
          [previous.trim(), finalized].filter(Boolean).join(" ")
        );
      }

      // Keep temporary words visible until the browser finalizes them.
      setVoiceDraft(interimParts.join(" ").trim());
    };

    recognition.onerror = (event) => {
      if (
        event.error === "not-allowed" ||
        event.error === "service-not-allowed"
      ) {
        shouldKeepListeningRef.current = false;
        setError(
          "Microphone access was denied. Allow microphone access in your browser settings."
        );
      } else if (event.error === "no-speech") {
        // onend will attempt to resume listening.
      } else if (event.error !== "aborted") {
        shouldKeepListeningRef.current = false;
        setError(
          `Voice input failed (${event.error}). Please try again.`
        );
      }
    };

    recognition.onend = () => {
      // Resume if the browser ends the session while the mic is still active.
      if (
        shouldKeepListeningRef.current &&
        recognitionRef.current === recognition
      ) {
        voiceRestartTimerRef.current = window.setTimeout(() => {
          voiceRestartTimerRef.current = null;

          if (
            !shouldKeepListeningRef.current ||
            recognitionRef.current !== recognition
          ) {
            return;
          }

          try {
            recognition.start();
          } catch {
            shouldKeepListeningRef.current = false;
            recognitionRef.current = null;
            setIsListening(false);
            setVoiceDraft("");
            setError(
              "Listening stopped. Please press the microphone to try again."
            );
          }
        }, 500);

        return;
      }

      setIsListening(false);
      setVoiceDraft("");

      if (recognitionRef.current === recognition) {
        recognitionRef.current = null;
      }
    };

    recognitionRef.current = recognition;
    shouldKeepListeningRef.current = true;
    setVoiceDraft("");

    try {
      recognition.start();
    } catch {
      shouldKeepListeningRef.current = false;
      recognitionRef.current = null;
      setIsListening(false);
      setError("Could not start voice input. Please try again.");
    }
  };



  return (
    <div className="plant-chat-widget">
      <button
        type="button"
        className="plant-chat-launcher"
        onClick={() => setIsOpen((previous) => !previous)}
        aria-label={isOpen ? text.close : text.open}
        aria-expanded={isOpen}
      >
        {isOpen ? "✕" : "🌱"}

        {!isOpen && (
          <span className="plant-chat-launcher-label">
            Ask Plant AI
          </span>
        )}
      </button>

      {isOpen && (
        <section
          className="plant-chat-panel"
          aria-label={text.title}
        >
          <header className="plant-chat-header">
            <div className="plant-chat-brand">
              <div className="plant-chat-avatar">🌿</div>
              <div>
                <h2>{text.title}</h2>
                <p>{text.subtitle}</p>
                <span className="plant-chat-online">
                  <span className="plant-chat-online-dot" />
                  AI assistant
                </span>
              </div>
            </div>

            <button
              type="button"
              className="plant-chat-icon-button"
              onClick={handleNewChat}
              title={text.newChat}
              aria-label={text.newChat}
            >
              ↺
            </button>
          </header>

          {/* <div className="plant-chat-language">
            <label htmlFor="plant-chat-language">
              🌐 {text.language}
            </label>

            <select
              id="plant-chat-language"
              value={language}
              onChange={(event) => {
                const nextLanguage = event.target.value;

                setLanguage(nextLanguage);
                setError("");

                // Update the welcome message if no conversation
                // has started yet.
                setMessages((previous) => {
                  const userHasAsked = previous.some(
                    (message) => message.role === "user"
                  );

                  if (userHasAsked) return previous;

                  return [
                    {
                      role: "assistant",
                      content: getGreeting(nextLanguage),
                    },
                  ];
                });
              }}
            >
              {LANGUAGES.map((item) => (
                <option
                  key={item.value}
                  value={item.value}
                >
                  {item.label}
                </option>
              ))}
            </select>
          </div> */}

          {plantContext && (
            <div className="plant-chat-context">
              {/* <span>🌿 {text.currentAnalysis}</span> */}
              <strong>
                {plantContext.plant} — {plantContext.disease}
              </strong>
              {/* {typeof plantContext.confidence === "number" && (
                <small>
                  Model confidence:{" "}
                  {plantContext.confidence.toFixed(2)}%
                </small>
              )} */}
            </div>
          )}

          <div className="plant-chat-messages">
            {messages.map((message, index) => (
              <div
                key={`${index}-${message.role}`}
                className={`plant-chat-message ${message.role === "user"
                  ? "plant-chat-user"
                  : "plant-chat-assistant"
                  }`}
              >
                {message.role === "assistant" && (
                  <span className="plant-chat-message-avatar">
                    🌱
                  </span>
                )}

                <div className="plant-chat-bubble">
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                  >
                    {message.content
                      .replace(/&lt;br\s*\/?&gt;/gi, "\n\n")
                      .replace(/<br\s*\/?>/gi, "  \n")}
                  </ReactMarkdown>

                  {message.role === "assistant" && (
                    <button
                      type="button"
                      className="plant-chat-speak-button"
                      onClick={() => handleSpeak(message.content, index)}
                      aria-label={
                        speakingIndex === index
                          ? "Stop speaking"
                          : "Read answer aloud"
                      }
                      title={
                        speakingIndex === index
                          ? "Stop speaking"
                          : "Read answer aloud"
                      }
                    >
                      {speakingIndex === index
                        ? "⏹ Stop"
                        : "🔊 Listen"}
                    </button>
                  )}
                </div>
              </div>
            ))}

            {plantContext && !hasAskedQuestion && (
              <div className="plant-chat-quick-prompts">
                <span className="plant-chat-quick-prompts-title">
                  {text.quickPrompts}
                </span>

                <div className="plant-chat-quick-prompts-list">
                  {quickPrompts.map((prompt) => (
                    <button
                      key={prompt.id}
                      type="button"
                      className="plant-chat-quick-prompt"
                      disabled={loading}
                      onClick={() => handleSend(prompt.message)}
                    >
                      {prompt.label}
                      <span aria-hidden="true"> →</span>
                    </button>
                  ))}
                </div>
              </div>
            )}

            {loading && (
              <div className="plant-chat-message plant-chat-assistant">
                <span className="plant-chat-message-avatar">
                  🌱
                </span>

                <div className="plant-chat-bubble plant-chat-thinking">
                  <span className="plant-chat-spinner" />
                  {text.thinking}
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {error && (
            <div className="plant-chat-error">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          <form
            className="plant-chat-composer"
            onSubmit={(event) => {
              event.preventDefault();
              handleSend();
            }}
          >
            <textarea
              ref={inputRef}
              value={
                isListening && voiceDraft
                  ? [input, voiceDraft].filter(Boolean).join(" ")
                  : input
              }
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={handleKeyDown}
              placeholder={text.placeholder}
              maxLength={3000}
              rows={2}
              disabled={loading}
              aria-label={text.placeholder}
            />


            <button
              type="button"
              className={`plant-chat-voice-button ${isListening ? "listening" : ""
                }`}
              onClick={handleVoiceInput}
              disabled={loading}
              title={
                isListening ? "Stop listening" : "Start voice input"
              }
              aria-label={
                isListening ? "Stop listening" : "Start voice input"
              }
            >
              {isListening ? "■" : "🎙️"}
            </button>


            <button
              type="submit"
              disabled={!input.trim() || loading}
              aria-label={text.send}
              title={text.send}
            >
              {loading ? "…" : "➤"}
            </button>
          </form>

          <footer className="plant-chat-footer">
            <span>{text.footer}</span>
            {/* <span>{text.powered}</span> */}
          </footer>
        </section>
      )}
    </div>
  );
}
