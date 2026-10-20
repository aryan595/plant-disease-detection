import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import {
  getLocalizedPlant,
  getLocalizedDisease,
  getLocalizedDescription,
  getLocalizedSymptoms,
  getLocalizedManagement,
  getLocalizedPrevention,
} from "./diseaseTranslations";
import { API_BASE_URL } from "./config";
import "./ChatWidget.css";

const API_URL = `${API_BASE_URL}/chat`;
const CHAT_STORAGE_KEY = "plantHealthChat.messages.v1";
const MAX_STORED_MESSAGES = 50;
const MAX_REQUEST_MESSAGES = 10;

export const SUPPORTED_LANGS = [
  { code: "en", label: "English", native: "English" },
  { code: "hi", label: "Hindi", native: "हिन्दी" },
  { code: "mr", label: "Marathi", native: "मराठी" },
  { code: "bn", label: "Bengali", native: "বাংলা" },
  { code: "ta", label: "Tamil", native: "தமிழ்" },
];

const UI_TEXT = {
  en: {
    title: "Plant Health Assistant",
    subtitle: "1:1 AI Agricultural Doctor",
    greeting: "Hello! 🌱 I am your AI crop doctor. Ask me anything about plant diseases, symptoms, spray dosage, or crop protection.",
    placeholder: "Ask about your crop, disease, or spray...",
    send: "Send",
    newChat: "New chat",
    thinking: "AI Doctor is thinking...",
    close: "Close chat",
    open: "Open plant health assistant",
    error: "Something went wrong. Please try again.",
    footer: "AI agricultural advisory. Confirm critical cases with local extension officers.",
    powered: "Powered by Groq LLaMA 3.3",
    currentAnalysis: "Current crop diagnosis",
    quickPrompts: "Quick questions",
    explainResult: "Explain this diagnosis",
    nextSteps: "What should I do next?",
    prevention: "How do I prevent recurrence?",
    spokenUnsupported: "Audio output is not supported by this browser.",
    voiceUnsupported: "Voice input is not supported in this browser. Please try Chrome or Edge.",
    micDenied: "Microphone access was denied. Allow microphone access in browser settings.",
    voiceFailed: "Voice input encountered an error. Please try again.",
    listeningStopped: "Listening stopped. Tap microphone to speak again.",
    cannotStart: "Could not start voice recognition. Please try again.",
    emptyResponse: "The assistant returned an empty response.",
    voiceModeBtn: "1:1 Voice Mode",
    voiceModeLive: "Live Voice Mode",
    listeningVoice: "Listening to you... Speak naturally",
    thinkingVoice: "AI is analyzing your crop...",
    speakingVoice: "AI is speaking... Tap to interrupt",
    readyVoice: "Ready to listen. Tap to speak",
    stopVoice: "Exit Voice Mode",
    interrupt: "Interrupt",
    doneSpeaking: "Send Now",
    autoSpeakOn: "Auto-Speak: ON",
    autoSpeakOff: "Auto-Speak: OFF",
    switchLang: "Language",
  },

  hi: {
    title: "पौधा स्वास्थ्य सहायक",
    subtitle: "1:1 AI कृषि चिकित्सक",
    greeting: "नमस्ते किसान भाई! 🌱 मैं आपका AI कृषि डॉक्टर हूँ। पौधों की बीमारी, लक्षण, स्प्रे की मात्रा या रोकथाम के बारे में कुछ भी पूछें।",
    placeholder: "अपनी फसल, बीमारी या दवा के बारे में पूछें...",
    send: "भेजें",
    newChat: "नई बातचीत",
    thinking: "AI डॉक्टर सोच रहा है...",
    close: "चैट बंद करें",
    open: "पौधों का सहायक खोलें",
    error: "कुछ गड़बड़ हुई। कृपया दोबारा प्रयास करें।",
    footer: "AI कृषि सलाह। महत्वपूर्ण मामलों की पुष्टि कृषि विशेषज्ञ से करें।",
    powered: "Groq LLaMA 3.3 द्वारा संचालित",
    currentAnalysis: "वर्तमान फसल विश्लेषण",
    quickPrompts: "तुरंत पूछें",
    explainResult: "इस बीमारी को समझाएँ",
    nextSteps: "अब मुझे क्या करना चाहिए?",
    prevention: "दोबारा होने से कैसे रोकें?",
    spokenUnsupported: "यह ब्राउज़र आवाज़ में पढ़ने का समर्थन नहीं करता।",
    voiceUnsupported: "इस ब्राउज़र में वॉइस इनपुट उपलब्ध नहीं है। Chrome या Edge आज़माएँ।",
    micDenied: "माइक्रोफ़ोन की अनुमति नहीं मिली। ब्राउज़र सेटिंग में अनुमति दें।",
    voiceFailed: "वॉइस इनपुट विफल हुआ। कृपया दोबारा कोशिश करें।",
    listeningStopped: "सुनना बंद हो गया। फिर से बोलने के लिए माइक दबाएँ।",
    cannotStart: "वॉइस इनपुट शुरू नहीं हो सका। कृपया दोबारा प्रयास करें।",
    emptyResponse: "सहायक ने खाली जवाब दिया।",
    voiceModeBtn: "1:1 वॉइस मोड",
    voiceModeLive: "लाइव वॉइस मोड",
    listeningVoice: "आपको सुन रहा हूँ... बोलिए",
    thinkingVoice: "AI आपकी फसल का विश्लेषण कर रहा है...",
    speakingVoice: "AI बोल रहा है... रोकने के लिए टैप करें",
    readyVoice: "बोलने के लिए तैयार। माइक दबाएँ",
    stopVoice: "वॉइस मोड बंद करें",
    interrupt: "रोकें",
    doneSpeaking: "अभी भेजें",
    autoSpeakOn: "स्वचालित आवाज़: चालू",
    autoSpeakOff: "स्वचालित आवाज़: बंद",
    switchLang: "भाषा बदलें",
  },

  mr: {
    title: "पीक आरोग्य सहाय्यक",
    subtitle: "१:१ AI कृषी डॉक्टर",
    greeting: "नमस्कार शेतकरी बंधूंनो! 🌱 मी तुमचा AI पीक डॉक्टर आहे. पिकावरील रोग, लक्षणे, फवारणीचे प्रमाण किंवा उपचारांबद्दल कोणताही प्रश्न विचारा.",
    placeholder: "पिकाबद्दल, रोगाबद्दल किंवा फवारणीबद्दल विचारा...",
    send: "पाठवा",
    newChat: "नवीन संभाषण",
    thinking: "AI डॉक्टर विचार करत आहे...",
    close: "चॅट बंद करा",
    open: "पीक सहाय्यक उघडा",
    error: "काहीतरी चूक झाली. कृपया पुन्हा प्रयत्न करा.",
    footer: "AI कृषी सल्ला. गंभीर समस्यांसाठी कृषी सेवा केंद्राचा सल्ला घ्या.",
    powered: "Groq LLaMA 3.3 द्वारे समर्थित",
    currentAnalysis: "सध्याचे पीक विश्लेषण",
    quickPrompts: "जलद प्रश्न",
    explainResult: "हा रोग समजावून सांगा",
    nextSteps: "आता कोणती फवारणी करावी?",
    prevention: "हा रोग कसा टाळता येईल?",
    spokenUnsupported: "या ब्राउझरमध्ये उत्तर मोठ्याने वाचण्याची सुविधा नाही.",
    voiceUnsupported: "या ब्राउझरमध्ये व्हॉइस इनपुट उपलब्ध नाही. Chrome किंवा Edge वापरा.",
    micDenied: "मायक्रोफोनची परवानगी नाकारली आहे. ब्राउझर सेटिंग्जमध्ये परवानगी द्या.",
    voiceFailed: "व्हॉइस इनपुट अयशस्वी झाले. कृपया पुन्हा प्रयत्न करा.",
    listeningStopped: "ऐकणे थांबले. पुन्हा बोलण्यासाठी माइक दाबा.",
    cannotStart: "व्हॉइस इनपुट सुरू करता आले नाही. पुन्हा प्रयत्न करा.",
    emptyResponse: "चॅटबॉटकडून रिकामे उत्तर मिळाले.",
    voiceModeBtn: "१:१ व्हॉइस मोड",
    voiceModeLive: "थेट व्हॉइस मोड",
    listeningVoice: "ऐकत आहे... बोला",
    thinkingVoice: "AI पिकाचा विचार करत आहे...",
    speakingVoice: "AI बोलत आहे... थांबवण्यासाठी टॅप करा",
    readyVoice: "बोलण्यासाठी तयार. माइक दाबा",
    stopVoice: "व्हॉइस मोड बंद करा",
    interrupt: "थांबवा",
    doneSpeaking: "आता पाठवा",
    autoSpeakOn: "स्वयंचलित आवाज: चालू",
    autoSpeakOff: "स्वयंचलित आवाज: बंद",
    switchLang: "भाषा निवडा",
  },

  bn: {
    title: "উদ্ভিদ স্বাস্থ্য সহায়ক",
    subtitle: "১:১ AI কৃষি পরামর্শদাতা",
    greeting: "নমস্কার কৃষক ভাই! 🌱 আমি আপনার AI কৃষি ডাক্তার। ফসলের রোগ, উপসর্গ, স্প্রে ও প্রতিকার সম্পর্কে যা কিছু জিজ্ঞাসা করুন।",
    placeholder: "আপনার ফসল বা রোগ সম্পর্কে লিখুন...",
    send: "পাঠান",
    newChat: "নতুন চ্যাট",
    thinking: "AI ভাবছে...",
    close: "চ্যাট বন্ধ করুন",
    open: "সহায়ক খুলুন",
    error: "কিছু সমস্যা হয়েছে। আবার চেষ্টা করুন।",
    footer: "AI কৃষি পরামর্শ। গুরুত্বপূর্ণ সিদ্ধান্তের জন্য কৃষি কর্মকর্তার সাথে কথা বলুন।",
    powered: "Groq LLaMA 3.3 দ্বারা চালিত",
    currentAnalysis: "বর্তমান ফসল বিশ্লেষণ",
    quickPrompts: "দ্রুত প্রশ্ন",
    explainResult: "রোগটি বুঝিয়ে দিন",
    nextSteps: "এখন কী স্প্রে করব?",
    prevention: "কীভাবে রোগ প্রতিরোধ করব?",
    spokenUnsupported: "এই ব্রাউজারে উত্তর পড়ে শোনানোর সুবিধা নেই।",
    voiceUnsupported: "এই ব্রাউজারে ভয়েস ইনপুট সমর্থিত নয়। Chrome বা Edge ব্যবহার করুন।",
    micDenied: "মাইক্রোফোনের অনুমতি দেওয়া হয়নি। সেটিংসে অনুমতি দিন।",
    voiceFailed: "ভয়েস ইনপুট ব্যর্থ হয়েছে।",
    listeningStopped: "শোনা বন্ধ হয়েছে। আবার বলতে মাইক চাপুন।",
    cannotStart: "ভয়েস ইনপুট শুরু করা যায়নি।",
    emptyResponse: "সহায়ক খালি উত্তর দিয়েছে।",
    voiceModeBtn: "১:১ ভয়েস মোড",
    voiceModeLive: "লাইভ ভয়েস মোড",
    listeningVoice: "শুনছি... কথা বলুন",
    thinkingVoice: "AI বিশ্লেষণ করছে...",
    speakingVoice: "AI কথা বলছে... থামাতে ট্যাপ করুন",
    readyVoice: "বলতে প্রস্তুত। মাইক চাপুন",
    stopVoice: "ভয়েস মোড বন্ধ করুন",
    interrupt: "থামান",
    doneSpeaking: "এখন পাঠান",
    autoSpeakOn: "স্বয়ংক্রিয় কণ্ঠ: চালু",
    autoSpeakOff: "স্বয়ংক্রিয় কণ্ঠ: বন্ধ",
    switchLang: "ভাষা পরিবর্তন",
  },

  ta: {
    title: "பயிர் நல உதவியாளர்",
    subtitle: "1:1 AI வேளாண் மருத்துவர்",
    greeting: "வணக்கம் விவசாய நண்பரே! 🌱 நான் உங்கள் AI பயிர் மருத்துவர். பயிர் நோய்கள், அறிகுறிகள், மருந்தளவு குறித்து கேளுங்கள்.",
    placeholder: "உங்கள் பயிர் அல்லது நோய் பற்றி கேளுங்கள்...",
    send: "அனுப்பு",
    newChat: "புதிய உரையாடல்",
    thinking: "AI மருத்துவர் சிந்திக்கிறது...",
    close: "உரையாடலை மூடு",
    open: "உதவியாளரைத் திற",
    error: "ஏதோ தவறு ஏற்பட்டது. மீண்டும் முயற்சிக்கவும்.",
    footer: "AI வேளாண் ஆலோசனை. முக்கிய முடிவுகளுக்கு வேளாண் அலுவலரை அணுகவும்.",
    powered: "Groq LLaMA 3.3 மூலம் இயங்குகிறது",
    currentAnalysis: "தற்போதைய பயிர் பகுப்பாய்வு",
    quickPrompts: "விரைவான கேள்விகள்",
    explainResult: "நோயை விளக்குங்கள்",
    nextSteps: "அடுத்து என்ன மருந்து அடிக்க வேண்டும்?",
    prevention: "மீண்டும் வராமல் தடுப்பது எப்படி?",
    spokenUnsupported: "இந்த உலாவியில் பதில்களைப் பேசும் வசதி இல்லை.",
    voiceUnsupported: "இந்த உலாவியில் குரல் உள்ளீடு ஆதரிக்கப்படவில்லை.",
    micDenied: "மைக்ரோஃபோன் அனுமதி மறுக்கப்பட்டது.",
    voiceFailed: "குரல் உள்ளீடு தோல்வியடைந்தது.",
    listeningStopped: "கேட்பது நிறுத்தப்பட்டது.",
    cannotStart: "குரல் உள்ளீட்டைத் தொடங்க முடியவில்லை.",
    emptyResponse: "வெற்று பதில் வந்தது.",
    voiceModeBtn: "1:1 குரல் முறை",
    voiceModeLive: "நேரடி குரல் முறை",
    listeningVoice: "கேட்கிறது... பேசுங்கள்",
    thinkingVoice: "AI பகுப்பாய்வு செய்கிறது...",
    speakingVoice: "AI பேசுகிறது... நிறுத்த தட்டவும்",
    readyVoice: "பேசத் தயார்",
    stopVoice: "குரல் முறையை மூடு",
    interrupt: "நிறுத்து",
    doneSpeaking: "இப்போதே அனுப்பு",
    autoSpeakOn: "தானியங்கி குரல்: ஆன்",
    autoSpeakOff: "தானியங்கி குரல்: ஆஃப்",
    switchLang: "மொழி",
  },
};

const QUICK_MESSAGES = {
  en: {
    explain: "Please explain my current plant analysis, the predicted disease, and what it means in simple words.",
    next: "Based on my current plant analysis, what exact medicine or spray dose should I use in my 15-liter pump?",
    prevent: "How can I prevent this disease from spreading and reduce the risk of it returning?",
  },
  hi: {
    explain: "मेरी वर्तमान फसल के विश्लेषण, पहचानी गई बीमारी और इसके प्रभाव को सरल भाषा में समझाएँ।",
    next: "इस बीमारी के लिए 15 लीटर नैपसैक पंप में कौन सी दवा और कितनी मात्रा में मिलाकर छिड़कनी चाहिए?",
    prevent: "इस बीमारी को खेत में फैलने से कैसे रोकूँ और दोबारा आने का खतरा कैसे कम करूँ?",
  },
  mr: {
    explain: "माझ्या पिकाच्या या विश्लेषणातील रोग आणि त्याचे संभाव्य नुकसान सोप्या भाषेत समजावून सांगा.",
    next: "या रोगासाठी १५ लिटर नॅपसॅक पंपात कोणते औषध आणि किती प्रमाणात मिसळून फवारणी करावी?",
    prevent: "हा रोग शेतात पसरण्यापासून कसा रोखायचा आणि पुढील हंगामात पुन्हा होऊ नये म्हणून काय करावे?",
  },
  bn: {
    explain: "আমার ফসলের এই রোগ এবং ক্ষতির কারণ সহজ কথায় বুঝিয়ে দিন।",
    next: "১৫ লিটার স্প্রে পাম্পে কোন ওষুধ এবং কত মাত্রায় স্প্রে করতে হবে?",
    prevent: "এই রোগ জমিতে ছড়ানো কীভাবে আটকাব এবং আবার হওয়ার ঝুঁকি কীভাবে কমাব?",
  },
  ta: {
    explain: "எனது பயிரில் உள்ள நோயின் பாதிப்பை எளிய தமிழில் விளக்கவும்.",
    next: "15 லிட்டர் தெளிப்பான் பம்பில் என்ன மருந்து, எவ்வளவு அளவு கலந்து அடிக்க வேண்டும்?",
    prevent: "இந்த நோய் மீண்டும் பரவாமல் இருக்க என்ன முன்னெச்சரிக்கை எடுக்க வேண்டும்?",
  },
};

function getText(language) {
  return UI_TEXT[language] || UI_TEXT.en;
}

function getGreeting(language) {
  return getText(language).greeting;
}

function getSpeechLanguage(language) {
  const locales = {
    en: "en-IN",
    hi: "hi-IN",
    mr: "mr-IN",
    bn: "bn-IN",
    ta: "ta-IN",
  };
  return locales[language] || "en-IN";
}

/**
 * Strips ALL Markdown, HTML, asterisks, hashes, brackets, bullets, emojis,
 * and formats agricultural measurements into natural human-spoken words.
 */
export function cleanTextForSpeech(markdown, lang = "en") {
  if (!markdown) return "";

  let text = markdown
    // Fenced code blocks
    .replace(/```[\s\S]*?```/g, " ")
    // Inline code
    .replace(/`([^`]+)`/g, "$1")
    // Images
    .replace(/!\[([^\]]*)\]\([^)]+\)/g, "$1")
    // Links
    .replace(/\[([^\]]+)\]\([^)]+\)/g, "$1")
    // HTML breaks and tags
    .replace(/<br\s*\/?>/gi, ". ")
    .replace(/<\/?[^>]+(>|$)/g, " ")
    // Headings (##, ###)
    .replace(/^\s{0,3}#{1,6}\s+/gm, "")
    // Horizontal rules (---, ***, ___)
    .replace(/^\s*[-*_]{3,}\s*$/gm, ". ")
    // Bullet signs at start of line
    .replace(/^\s*[-*+•]\s+/gm, "")
    // Numbered lists at start of line
    .replace(/^\s*\d+[.)]\s+/gm, "")
    // Triple asterisks / underscores (bold italic)
    .replace(/\*{3}([^*]+)\*{3}/g, "$1")
    .replace(/_{3}([^_]+)_{3}/g, "$1")
    // Double asterisks / underscores (bold)
    .replace(/\*{2}([^*]+)\*{2}/g, "$1")
    .replace(/_{2}([^_]+)_{2}/g, "$1")
    // Single asterisk / underscore (italic)
    .replace(/\*([^*]+)\*/g, "$1")
    .replace(/_([^_]+)_/g, "$1")
    // Strikethrough
    .replace(/~~([^~]+)~~/g, "$1")
    // Blockquotes
    .replace(/^\s*>\s?/gm, "")
    // Tables & pipes
    .replace(/\|/g, ", ")
    .replace(/^\s*[-:]+\s*$/gm, "")
    // Strip any stray asterisks, hashes, tildes, backticks, pipes
    .replace(/[*_~#`>]/g, " ")
    // Strip all emojis (which TTS engines read out awkwardly)
    .replace(/[\u{1F300}-\u{1F9FF}\u{2600}-\u{27BF}\u{1F600}-\u{1F64F}\u{1F680}-\u{1F6FF}]/gu, " ");

  // Expand units into natural spoken words based on language
  if (lang === "mr") {
    text = text
      .replace(/(\S+)\s*g\/L\b/gi, "$1 ग्रॅम प्रति लिटर")
      .replace(/(\S+)\s*ml\/L\b/gi, "$1 मिली प्रति लिटर")
      .replace(/(\S+)\s*kg\/ha\b/gi, "$1 किलो प्रति हेक्टर")
      .replace(/%/g, " टक्के ")
      .replace(/@/g, " दर ");
  } else if (lang === "hi") {
    text = text
      .replace(/(\S+)\s*g\/L\b/gi, "$1 ग्राम प्रति लीटर")
      .replace(/(\S+)\s*ml\/L\b/gi, "$1 मिली प्रति लीटर")
      .replace(/(\S+)\s*kg\/ha\b/gi, "$1 किलो प्रति हेक्टेयर")
      .replace(/%/g, " प्रतिशत ")
      .replace(/@/g, " दर ");
  } else {
    text = text
      .replace(/(\S+)\s*g\/L\b/gi, "$1 grams per liter")
      .replace(/(\S+)\s*ml\/L\b/gi, "$1 milliliters per liter")
      .replace(/(\S+)\s*kg\/ha\b/gi, "$1 kilograms per hectare")
      .replace(/%/g, " percent ")
      .replace(/@/g, " at ");
  }

  return text
    .replace(/\s+/g, " ")
    .replace(/\.\s*\./g, ".")
    .replace(/,\s*,/g, ",")
    .trim();
}

/**
 * Splits text into natural sentence chunks to prevent Chrome's 15-second SpeechSynthesis cutoff bug.
 */
function splitIntoSentenceChunks(text) {
  if (!text) return [];
  const rawParts = text.split(/(?<=[.!?\n])\s+/);
  const chunks = [];

  for (const part of rawParts) {
    const trimmed = part.trim();
    if (!trimmed) continue;
    if (trimmed.length > 180) {
      // Split long clauses on commas
      const sub = trimmed.split(/(?<=[,;])\s+/);
      for (const s of sub) {
        if (s.trim()) chunks.push(s.trim());
      }
    } else {
      chunks.push(trimmed);
    }
  }

  return chunks.length > 0 ? chunks : [text];
}

/**
 * Finds the highest quality neural or regional voice for speech synthesis.
 */
function selectBestVoice(langCode) {
  if (typeof window === "undefined" || !("speechSynthesis" in window)) return null;
  const voices = window.speechSynthesis.getVoices();
  if (!voices || voices.length === 0) return null;

  const target = langCode.toLowerCase();
  const prefix = target.split("-")[0];

  // 1. Natural / Google / Neural voice with exact locale match
  const naturalMatch = voices.find(
    (v) =>
      v.lang.toLowerCase() === target &&
      (v.name.includes("Google") ||
        v.name.includes("Natural") ||
        v.name.includes("Neural") ||
        v.name.includes("Online"))
  );
  if (naturalMatch) return naturalMatch;

  // 2. Exact locale match
  const exactMatch = voices.find((v) => v.lang.toLowerCase() === target);
  if (exactMatch) return exactMatch;

  // 3. Prefix match with Google / Natural
  const prefixNatural = voices.find(
    (v) =>
      v.lang.toLowerCase().startsWith(prefix) &&
      (v.name.includes("Google") ||
        v.name.includes("Natural") ||
        v.name.includes("Neural"))
  );
  if (prefixNatural) return prefixNatural;

  // 4. Any prefix match
  const prefixMatch = voices.find((v) => v.lang.toLowerCase().startsWith(prefix));
  if (prefixMatch) return prefixMatch;

  // 5. Indian English / Hindi fallback
  const inFallback = voices.find(
    (v) =>
      v.lang.toLowerCase().includes("in") ||
      v.name.toLowerCase().includes("india")
  );
  if (inFallback) return inFallback;

  return voices[0] || null;
}

function loadSavedMessages(language) {
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
    // Start fresh
  }

  return [
    {
      role: "assistant",
      content: getGreeting(language),
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

function buildPlantContext(result, language = "en") {
  if (!result || !result.plant || !result.disease) {
    return null;
  }

  const isMr = language === "mr";
  const plant = isMr
    ? (result.plant_mr || getLocalizedPlant(result.plant, language) || result.plant)
    : result.plant;
  const disease = isMr
    ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant) || result.disease)
    : result.disease;
  const description = isMr
    ? (result.description_mr || getLocalizedDescription(result.disease, language, result.description, result.class_name, result.plant) || result.description)
    : result.description;
  const rawSymptoms = isMr && result.symptoms_mr?.length
    ? result.symptoms_mr
    : (isMr
        ? getLocalizedSymptoms(result.disease, language, result.symptoms, result.class_name, result.plant)
        : result.symptoms);
  const rawManagement = isMr && result.management_mr?.length
    ? result.management_mr
    : (isMr
        ? getLocalizedManagement(result.disease, language, result.management, result.class_name, result.plant)
        : result.management);
  const rawPrevention = isMr && result.prevention_mr?.length
    ? result.prevention_mr
    : (isMr
        ? getLocalizedPrevention(result.disease, language, result.prevention, result.class_name, result.plant)
        : result.prevention);

  return {
    plant,
    disease,
    confidence:
      typeof result.confidence === "number" ? result.confidence : undefined,
    confidence_status: result.confidence_status,
    description,
    symptoms: Array.isArray(rawSymptoms) ? rawSymptoms.slice(0, 5) : [],
    management: Array.isArray(rawManagement) ? rawManagement.slice(0, 5) : [],
    prevention: Array.isArray(rawPrevention) ? rawPrevention.slice(0, 5) : [],
    top_3: Array.isArray(result.top_3)
      ? result.top_3.slice(0, 3).map((item) => ({
          plant: isMr ? (item.plant_mr || getLocalizedPlant(item.plant, language) || item.plant) : item.plant,
          disease: isMr ? (item.disease_mr || getLocalizedDisease(item.disease, language, item.class_name, item.plant) || item.disease) : item.disease,
          confidence: item.confidence,
        }))
      : [],
  };
}

export default function ChatWidget({
  plantResult = null,
  language = "en",
  onLanguageChange = null,
}) {
  // Local active language state to allow switching directly in the bot
  const [botLanguage, setBotLanguage] = useState(language);

  // Sync with prop if parent changes language externally
  useEffect(() => {
    if (language && language !== botLanguage) {
      setBotLanguage(language);
    }
  }, [language]);

  const activeLanguage = UI_TEXT[botLanguage] ? botLanguage : "en";

  const [isOpen, setIsOpen] = useState(false);
  const [messageHistory, setMessageHistory] = useState(() =>
    loadSavedMessages(activeLanguage)
  );
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [voiceDraft, setVoiceDraft] = useState("");
  const [speakingIndex, setSpeakingIndex] = useState(null);
  const [error, setError] = useState("");

  // 1:1 ChatGPT Voice Mode States
  const [voiceModeActive, setVoiceModeActive] = useState(false);
  const [voiceStatus, setVoiceStatus] = useState("idle"); // 'idle' | 'listening' | 'thinking' | 'speaking'
  const [autoSpeak, setAutoSpeak] = useState(true);

  const recognitionRef = useRef(null);
  const shouldKeepListeningRef = useRef(false);
  const voiceRestartTimerRef = useRef(null);
  const autoSubmitTimerRef = useRef(null);
  const latestTranscriptRef = useRef("");
  const isSpeakingRef = useRef(false);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const text = getText(activeLanguage);
  const plantContext = buildPlantContext(plantResult, activeLanguage);
  const quickPrompts = getQuickPrompts(activeLanguage);

  const hasAskedQuestion = messageHistory.some(
    (message) => message.role === "user"
  );

  const messages = useMemo(
    () =>
      hasAskedQuestion
        ? messageHistory
        : [
            {
              role: "assistant",
              content: getGreeting(activeLanguage),
            },
          ],
    [activeLanguage, hasAskedQuestion, messageHistory]
  );

  // Save history
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

      localStorage.setItem(CHAT_STORAGE_KEY, JSON.stringify(savedMessages));
    } catch {
      // Ignore storage errors
    }
  }, [messages]);

  // Pre-load voices on mount
  useEffect(() => {
    if (typeof window !== "undefined" && "speechSynthesis" in window) {
      window.speechSynthesis.getVoices();
      const onVoices = () => {
        window.speechSynthesis.getVoices();
      };
      window.speechSynthesis.addEventListener("voiceschanged", onVoices);
      return () => {
        window.speechSynthesis.removeEventListener("voiceschanged", onVoices);
      };
    }
  }, []);

  // Listen for programmatic open events
  useEffect(() => {
    const handleOpenChat = (event) => {
      setIsOpen(true);
      if (event.detail?.message) {
        setInput(event.detail.message);
      }
      if (event.detail?.startVoice) {
        setTimeout(() => {
          handleVoiceInput();
        }, 350);
      }
    };
    window.addEventListener("open-plant-chat", handleOpenChat);
    return () => window.removeEventListener("open-plant-chat", handleOpenChat);
  }, []);

  // Scroll to bottom
  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "end",
    });
  }, [messages, loading, isOpen, voiceStatus]);

  useEffect(() => {
    if (isOpen) {
      inputRef.current?.focus();
    }
  }, [isOpen]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      shouldKeepListeningRef.current = false;
      if (voiceRestartTimerRef.current !== null) {
        window.clearTimeout(voiceRestartTimerRef.current);
      }
      if (autoSubmitTimerRef.current !== null) {
        window.clearTimeout(autoSubmitTimerRef.current);
      }
      try {
        recognitionRef.current?.stop();
      } catch {
        // Ignored
      }
      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
      isSpeakingRef.current = false;
    };
  }, []);

  const stopAllAudio = () => {
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }
    isSpeakingRef.current = false;
    setSpeakingIndex(null);
    if (voiceStatus === "speaking") {
      setVoiceStatus(voiceModeActive ? "ready" : "idle");
    }
  };

  const stopVoiceInput = () => {
    shouldKeepListeningRef.current = false;
    if (voiceRestartTimerRef.current !== null) {
      window.clearTimeout(voiceRestartTimerRef.current);
      voiceRestartTimerRef.current = null;
    }
    if (autoSubmitTimerRef.current !== null) {
      window.clearTimeout(autoSubmitTimerRef.current);
      autoSubmitTimerRef.current = null;
    }
    try {
      recognitionRef.current?.stop();
    } catch {
      // Ignored
    }
    setIsListening(false);
    setVoiceDraft("");
    recognitionRef.current = null;
  };

  // Switch language directly in the chatbot
  const handleLanguageSwitch = (newLangCode) => {
    if (!UI_TEXT[newLangCode]) return;
    stopAllAudio();
    stopVoiceInput();
    setBotLanguage(newLangCode);

    if (onLanguageChange) {
      onLanguageChange(newLangCode);
    }

    // If chat hasn't started yet, refresh greeting
    if (!hasAskedQuestion) {
      setMessageHistory([
        {
          role: "assistant",
          content: getGreeting(newLangCode),
        },
      ]);
    }
  };

  const handleNewChat = () => {
    stopVoiceInput();
    stopAllAudio();
    setVoiceModeActive(false);
    setVoiceStatus("idle");

    setMessageHistory([
      {
        role: "assistant",
        content: getGreeting(activeLanguage),
      },
    ]);

    setInput("");
    setError("");
  };

  /**
   * Reads assistant messages aloud using sentence-chunked synthesis.
   * Completely strips * signs, #, and markdown formatting artifacts.
   */
  const handleSpeak = (content, index, onComplete = null) => {
    if (
      !("speechSynthesis" in window) ||
      typeof window.SpeechSynthesisUtterance === "undefined"
    ) {
      setError(text.spokenUnsupported);
      return;
    }

    // Toggle off if currently speaking this message
    if (speakingIndex === index && isSpeakingRef.current) {
      stopAllAudio();
      return;
    }

    stopAllAudio();

    const cleanText = cleanTextForSpeech(content, activeLanguage);
    if (!cleanText) return;

    const chunks = splitIntoSentenceChunks(cleanText);
    if (chunks.length === 0) return;

    setSpeakingIndex(index);
    isSpeakingRef.current = true;
    setVoiceStatus("speaking");

    let chunkIndex = 0;

    const speakNextChunk = () => {
      if (!isSpeakingRef.current || chunkIndex >= chunks.length) {
        isSpeakingRef.current = false;
        setSpeakingIndex(null);
        setVoiceStatus(voiceModeActive ? "ready" : "idle");
        if (onComplete) onComplete();
        return;
      }

      const chunk = chunks[chunkIndex++];
      const utterance = new window.SpeechSynthesisUtterance(chunk);
      utterance.lang = getSpeechLanguage(activeLanguage);
      utterance.rate = 0.96;
      utterance.pitch = 1.0;

      const voice = selectBestVoice(utterance.lang);
      if (voice) {
        utterance.voice = voice;
      }

      utterance.onend = () => {
        speakNextChunk();
      };

      utterance.onerror = () => {
        isSpeakingRef.current = false;
        setSpeakingIndex(null);
        setVoiceStatus(voiceModeActive ? "ready" : "idle");
      };

      window.speechSynthesis.speak(utterance);
    };

    speakNextChunk();
  };

  /**
   * Core send message handler.
   * Automatically triggers speech playback in 1:1 Voice Mode or when Auto-Speak is enabled.
   */
  const handleSend = async (messageOverride = null) => {
    const content = (
      typeof messageOverride === "string" ? messageOverride : input
    ).trim();

    if (!content || loading) {
      return;
    }

    // Interrupt any ongoing speech immediately
    stopAllAudio();
    stopVoiceInput();

    const userMessage = {
      role: "user",
      content,
    };

    const requestMessages = [...messages, userMessage].slice(
      -MAX_REQUEST_MESSAGES
    );

    setMessageHistory([...messages, userMessage]);
    setInput("");
    setVoiceDraft("");
    latestTranscriptRef.current = "";
    setError("");
    setLoading(true);
    setVoiceStatus("thinking");

    try {
      const response = await fetch(API_URL, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          messages: requestMessages,
          language: activeLanguage,
          plant_context: plantContext,
        }),
      });

      let data;
      try {
        data = await response.json();
      } catch {
        throw new Error(`Chat request failed (${response.status}).`);
      }

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Chat request failed (${response.status}).`
        );
      }

      if (typeof data.reply !== "string" || !data.reply.trim()) {
        throw new Error(text.emptyResponse);
      }

      const newIndex = messages.length + 1;

      setMessageHistory((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.reply,
        },
      ]);

      // 1:1 ChatGPT Voice Mode loop: automatically speak the response!
      if (voiceModeActive || autoSpeak) {
        handleSpeak(data.reply, newIndex, () => {
          // If in continuous 1:1 voice mode, resume listening for farmer's follow-up question
          if (voiceModeActive) {
            setTimeout(() => {
              startVoiceInput();
            }, 600);
          }
        });
      } else {
        setVoiceStatus("idle");
      }
    } catch (err) {
      console.error("Plant chatbot error:", err);
      setError(err.message || text.error);
      setVoiceStatus("idle");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  /**
   * Voice input handler with real-time transcription and automatic speech submission.
   */
  const startVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(text.voiceUnsupported);
      return;
    }

    // Stop ongoing audio so the user isn't competing with the bot speaking
    stopAllAudio();

    if (isListening) {
      stopVoiceInput();
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = getSpeechLanguage(activeLanguage);
    recognition.continuous = true;
    recognition.interimResults = true;
    recognition.maxAlternatives = 1;

    recognition.onstart = () => {
      setIsListening(true);
      setError("");
      setVoiceStatus("listening");
    };

    recognition.onresult = (event) => {
      const finalParts = [];
      const interimParts = [];

      for (let i = event.resultIndex; i < event.results.length; i++) {
        const speechResult = event.results[i];
        const transcript = speechResult[0]?.transcript?.trim();
        if (!transcript) continue;

        if (speechResult.isFinal) {
          finalParts.push(transcript);
        } else {
          interimParts.push(transcript);
        }
      }

      const finalized = finalParts.join(" ").trim();
      if (finalized) {
        setInput((prev) => {
          const updated = [prev.trim(), finalized].filter(Boolean).join(" ");
          latestTranscriptRef.current = updated;
          return updated;
        });
      }

      const currentInterim = interimParts.join(" ").trim();
      setVoiceDraft(currentInterim);

      // In 1:1 Voice Mode, detect silence and auto-submit like ChatGPT Voice!
      if (voiceModeActive) {
        if (autoSubmitTimerRef.current !== null) {
          window.clearTimeout(autoSubmitTimerRef.current);
        }
        autoSubmitTimerRef.current = window.setTimeout(() => {
          const textToSend = (
            latestTranscriptRef.current ||
            finalized ||
            currentInterim
          ).trim();
          if (textToSend && textToSend.length > 2) {
            handleSend(textToSend);
          }
        }, 1400);
      }
    };

    recognition.onerror = (event) => {
      if (
        event.error === "not-allowed" ||
        event.error === "service-not-allowed"
      ) {
        shouldKeepListeningRef.current = false;
        setError(text.micDenied);
        setVoiceStatus("idle");
      } else if (event.error === "no-speech") {
        // Will continue on continuous mode
      } else if (event.error !== "aborted") {
        shouldKeepListeningRef.current = false;
        setError(`${text.voiceFailed} (${event.error})`);
        setVoiceStatus("idle");
      }
    };

    recognition.onend = () => {
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
            setVoiceStatus("idle");
          }
        }, 400);
        return;
      }

      setIsListening(false);
      setVoiceDraft("");
      if (recognitionRef.current === recognition) {
        recognitionRef.current = null;
      }
      if (voiceStatus === "listening") {
        setVoiceStatus(voiceModeActive ? "ready" : "idle");
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
      setError(text.cannotStart);
      setVoiceStatus("idle");
    }
  };

  const handleVoiceInput = () => {
    if (isListening) {
      stopVoiceInput();
    } else {
      startVoiceInput();
    }
  };

  // Toggle 1:1 ChatGPT Voice Mode
  const toggleVoiceMode = () => {
    if (voiceModeActive) {
      setVoiceModeActive(false);
      stopVoiceInput();
      stopAllAudio();
      setVoiceStatus("idle");
    } else {
      setVoiceModeActive(true);
      stopAllAudio();
      setTimeout(() => {
        startVoiceInput();
      }, 200);
    }
  };

  const handleToggleOpen = () => {
    if (isOpen) {
      stopVoiceInput();
      stopAllAudio();
      setVoiceModeActive(false);
    }
    setIsOpen((previous) => !previous);
  };

  return (
    <div className={`plant-chat-widget${isOpen ? " is-open" : ""}`}>
      {/* Floating launcher */}
      <button
        type="button"
        className="plant-chat-launcher"
        onClick={handleToggleOpen}
        aria-label={isOpen ? text.close : text.open}
        aria-expanded={isOpen}
      >
        {isOpen ? "✕" : "🌱"}
        {!isOpen && (
          <span className="plant-chat-launcher-label">
            {activeLanguage === "mr"
              ? "कृषी AI डॉक्टर"
              : activeLanguage === "hi"
              ? "किसान AI डॉक्टर"
              : "Ask Plant AI"}
          </span>
        )}
      </button>

      {/* Main chat panel */}
      {isOpen && (
        <section className="plant-chat-panel" aria-label={text.title}>
          {/* Header */}
          <header className="plant-chat-header">
            <div className="plant-chat-brand">
              <div className="plant-chat-avatar">🌿</div>
              <div>
                <h2>{text.title}</h2>
                <p>{text.subtitle}</p>
                <span className="plant-chat-online">
                  <span className="plant-chat-online-dot" />
                  {voiceModeActive ? "🎙️ 1:1 Voice Live" : "AI Specialist"}
                </span>
              </div>
            </div>

            <div className="plant-chat-header-actions">
              {/* Dynamic language switcher inside chatbot */}
              <div className="plant-chat-lang-picker" title={text.switchLang}>
                <span className="plant-chat-lang-icon" aria-hidden="true">🌐</span>
                <select
                  className="plant-chat-lang-select"
                  value={activeLanguage}
                  onChange={(e) => handleLanguageSwitch(e.target.value)}
                  aria-label="Select Chatbot Language"
                >
                  {SUPPORTED_LANGS.map((lang) => (
                    <option key={lang.code} value={lang.code}>
                      {lang.native} ({lang.code.toUpperCase()})
                    </option>
                  ))}
                </select>
              </div>

              {/* Reset chat button */}
              <button
                type="button"
                className="plant-chat-icon-button"
                onClick={handleNewChat}
                title={text.newChat}
                aria-label={text.newChat}
              >
                ↺
              </button>

              <button
                type="button"
                className="plant-chat-icon-button plant-chat-close-button"
                onClick={handleToggleOpen}
                title={text.close}
                aria-label={text.close}
              >
                ×
              </button>
            </div>
          </header>

          {/* Current diagnosis badge */}
          {plantContext && (
            <div className="plant-chat-context">
              <span>🌿 {text.currentAnalysis}:</span>
              <strong>
                {plantContext.plant} — {plantContext.disease}
              </strong>
              {typeof plantContext.confidence === "number" && (
                <small>({plantContext.confidence.toFixed(1)}% match)</small>
              )}
            </div>
          )}

          {/* 1:1 ChatGPT Voice Mode Live Banner */}
          {voiceModeActive && (
            <div className={`plant-chat-voice-live-banner status-${voiceStatus}`}>
              <div className="plant-chat-voice-live-info">
                {/* Acoustic waveform animation */}
                <div className="plant-chat-waveform" aria-hidden="true">
                  <span className={`wave-bar bar-1 ${voiceStatus}`} />
                  <span className={`wave-bar bar-2 ${voiceStatus}`} />
                  <span className={`wave-bar bar-3 ${voiceStatus}`} />
                  <span className={`wave-bar bar-4 ${voiceStatus}`} />
                </div>
                <div className="plant-chat-voice-live-text">
                  <span className="voice-status-title">
                    {voiceStatus === "listening"
                      ? text.listeningVoice
                      : voiceStatus === "thinking"
                      ? text.thinkingVoice
                      : voiceStatus === "speaking"
                      ? text.speakingVoice
                      : text.readyVoice}
                  </span>
                  <span className="voice-status-sub">
                    {activeLanguage === "mr"
                      ? "मराठीत स्पष्ट संवाद • ० एरर"
                      : activeLanguage === "hi"
                      ? "हिन्दी में सीधा संवाद • 0 एरर"
                      : "Human-like natural voice • No asterisks"}
                  </span>
                </div>
              </div>

              <div className="plant-chat-voice-live-actions">
                {voiceStatus === "speaking" && (
                  <button
                    type="button"
                    className="plant-chat-voice-interrupt-btn"
                    onClick={() => {
                      stopAllAudio();
                      startVoiceInput();
                    }}
                  >
                    ✋ {text.interrupt}
                  </button>
                )}

                {voiceStatus === "listening" && (input || voiceDraft) && (
                  <button
                    type="button"
                    className="plant-chat-voice-send-now-btn"
                    onClick={() => handleSend()}
                  >
                    ➤ {text.doneSpeaking}
                  </button>
                )}

                <button
                  type="button"
                  className="plant-chat-voice-close-btn"
                  onClick={toggleVoiceMode}
                  title={text.stopVoice}
                >
                  ✕
                </button>
              </div>
            </div>
          )}

          {/* Messages container */}
          <div className="plant-chat-messages">
            {messages.map((message, index) => (
              <div
                key={`${index}-${message.role}`}
                className={`plant-chat-message ${
                  message.role === "user"
                    ? "plant-chat-user"
                    : "plant-chat-assistant"
                } ${speakingIndex === index ? "is-speaking-active" : ""}`}
              >
                {message.role === "assistant" && (
                  <span className="plant-chat-message-avatar">🌱</span>
                )}

                <div className="plant-chat-bubble">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content
                      .replace(/&lt;br\s*\/?&gt;/gi, "\n\n")
                      .replace(/<br\s*\/?>/gi, "  \n")}
                  </ReactMarkdown>

                  {message.role === "assistant" && (
                    <button
                      type="button"
                      className={`plant-chat-speak-button ${
                        speakingIndex === index ? "playing" : ""
                      }`}
                      onClick={() => handleSpeak(message.content, index)}
                      aria-label={
                        speakingIndex === index
                          ? "Stop speaking"
                          : "Read answer aloud"
                      }
                      title={
                        speakingIndex === index
                          ? "Stop speaking"
                          : "Read answer aloud in natural human voice"
                      }
                    >
                      {speakingIndex === index ? (
                        <>
                          <span className="pulse-dot" /> ⏹ Stop
                        </>
                      ) : (
                        "🔊 Listen"
                      )}
                    </button>
                  )}
                </div>
              </div>
            ))}

            {/* Quick prompts */}
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

            {/* Thinking bubble */}
            {loading && (
              <div className="plant-chat-message plant-chat-assistant">
                <span className="plant-chat-message-avatar">🌱</span>
                <div className="plant-chat-bubble plant-chat-thinking">
                  <span className="plant-chat-spinner" />
                  {text.thinking}
                </div>
              </div>
            )}

            <div ref={bottomRef} />
          </div>

          {/* Error notice */}
          {error && (
            <div className="plant-chat-error">
              <span>⚠️</span>
              <span>{error}</span>
            </div>
          )}

          {/* Composer */}
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
              placeholder={
                isListening ? text.listeningVoice : text.placeholder
              }
              maxLength={3000}
              rows={2}
              disabled={loading}
              aria-label={text.placeholder}
            />

            {/* Voice input mic button */}
            <button
              type="button"
              className={`plant-chat-voice-button ${
                isListening ? "listening" : ""
              }`}
              onClick={handleVoiceInput}
              disabled={loading}
              title={
                isListening ? "Stop listening" : "Start voice input (Speak)"
              }
              aria-label={
                isListening ? "Stop listening" : "Start voice input"
              }
            >
              {isListening ? "■" : "🎙️"}
            </button>

            {/* Auto-Speak toggle switch */}
            <button
              type="button"
              className={`plant-chat-autospeak-toggle ${
                autoSpeak ? "active" : ""
              }`}
              onClick={() => setAutoSpeak((prev) => !prev)}
              title={autoSpeak ? text.autoSpeakOn : text.autoSpeakOff}
              aria-label={autoSpeak ? text.autoSpeakOn : text.autoSpeakOff}
            >
              {autoSpeak ? "🔊" : "🔇"}
            </button>

            {/* Submit button */}
            <button
              type="submit"
              disabled={!input.trim() || loading}
              aria-label={text.send}
              title={text.send}
            >
              {loading ? "…" : "➤"}
            </button>
          </form>

          {/* Footer */}
          <footer className="plant-chat-footer">
            <span>{text.footer}</span>
            <span>{text.powered}</span>
          </footer>
        </section>
      )}
    </div>
  );
}
