import { useEffect, useMemo, useRef, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import "./ChatWidget.css";

const API_URL = "http://127.0.0.1:8000/chat";
const CHAT_STORAGE_KEY = "plantHealthChat.messages.v1";
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
    spokenUnsupported: "Spoken responses are not supported by this browser.",
    voiceUnsupported: "Voice input is not supported in this browser. Try Chrome or Edge.",
    micDenied: "Microphone access was denied. Allow microphone access in your browser settings.",
    voiceFailed: "Voice input failed. Please try again.",
    listeningStopped: "Listening stopped. Please press the microphone to try again.",
    cannotStart: "Could not start voice input. Please try again.",
    emptyResponse: "The chatbot returned an empty response.",
  },

  hi: {
    title: "पौधों का स्वास्थ्य सहायक",
    subtitle: "आपका AI बागवानी साथी",
    greeting: "नमस्ते! 🌱 पौधों की बीमारी, लक्षण, बचाव या देखभाल के बारे में पूछें।",
    placeholder: "अपने पौधों के बारे में पूछें...",
    send: "भेजें",
    newChat: "नई बातचीत",
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
    spokenUnsupported: "यह ब्राउज़र जवाबों को आवाज़ में पढ़ने का समर्थन नहीं करता।",
    voiceUnsupported: "इस ब्राउज़र में वॉइस इनपुट उपलब्ध नहीं है। Chrome या Edge आज़माएँ।",
    micDenied: "माइक्रोफ़ोन की अनुमति नहीं मिली। ब्राउज़र सेटिंग में इसकी अनुमति दें।",
    voiceFailed: "वॉइस इनपुट विफल हुआ। कृपया फिर कोशिश करें।",
    listeningStopped: "सुनना बंद हो गया। फिर से कोशिश करने के लिए माइक्रोफ़ोन दबाएँ।",
    cannotStart: "वॉइस इनपुट शुरू नहीं हो सका। कृपया फिर कोशिश करें।",
    emptyResponse: "चैटबॉट ने खाली जवाब दिया।",
  },

  mr: {
    title: "वनस्पती आरोग्य सहाय्यक",
    subtitle: "तुमचा AI बागकाम साथी",
    greeting: "नमस्कार! 🌱 वनस्पतींचे रोग, लक्षणे, प्रतिबंध किंवा पिकांची काळजी याबद्दल विचारा.",
    placeholder: "तुमच्या वनस्पतींबद्दल विचारा...",
    send: "पाठवा",
    newChat: "नवीन संभाषण",
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
    spokenUnsupported: "या ब्राउझरमध्ये उत्तर मोठ्याने वाचण्याची सुविधा उपलब्ध नाही.",
    voiceUnsupported: "या ब्राउझरमध्ये व्हॉइस इनपुट उपलब्ध नाही. Chrome किंवा Edge वापरून पाहा.",
    micDenied: "मायक्रोफोनची परवानगी नाकारली आहे. ब्राउझर सेटिंग्जमध्ये परवानगी द्या.",
    voiceFailed: "व्हॉइस इनपुट अयशस्वी झाले. पुन्हा प्रयत्न करा.",
    listeningStopped: "ऐकणे थांबले. पुन्हा प्रयत्न करण्यासाठी मायक्रोफोन दाबा.",
    cannotStart: "व्हॉइस इनपुट सुरू करता आले नाही. पुन्हा प्रयत्न करा.",
    emptyResponse: "चॅटबॉटकडून रिकामे उत्तर मिळाले.",
  },

  bn: {
    title: "উদ্ভিদের স্বাস্থ্য সহায়ক",
    subtitle: "আপনার AI বাগানসঙ্গী",
    greeting: "নমস্কার! 🌱 গাছের রোগ, লক্ষণ, প্রতিরোধ বা ফসলের যত্ন সম্পর্কে জিজ্ঞাসা করুন।",
    placeholder: "আপনার গাছপালা সম্পর্কে জিজ্ঞাসা করুন...",
    send: "পাঠান",
    newChat: "নতুন চ্যাট",
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
    spokenUnsupported: "এই ব্রাউজারে উত্তর পড়ে শোনানোর সুবিধা নেই।",
    voiceUnsupported: "এই ব্রাউজারে ভয়েস ইনপুট সমর্থিত নয়। Chrome বা Edge ব্যবহার করুন।",
    micDenied: "মাইক্রোফোনের অনুমতি দেওয়া হয়নি। ব্রাউজার সেটিংসে অনুমতি দিন।",
    voiceFailed: "ভয়েস ইনপুট ব্যর্থ হয়েছে। আবার চেষ্টা করুন।",
    listeningStopped: "শোনা বন্ধ হয়েছে। আবার চেষ্টা করতে মাইক্রোফোন চাপুন।",
    cannotStart: "ভয়েস ইনপুট শুরু করা যায়নি। আবার চেষ্টা করুন।",
    emptyResponse: "চ্যাটবট খালি উত্তর দিয়েছে।",
  },

  ta: {
    title: "தாவர நல உதவியாளர்",
    subtitle: "உங்கள் AI தோட்டப் பராமரிப்பு துணை",
    greeting: "வணக்கம்! 🌱 தாவர நோய்கள், அறிகுறிகள், தடுப்பு அல்லது பயிர் பராமரிப்பு பற்றி கேளுங்கள்.",
    placeholder: "உங்கள் தாவரங்களைப் பற்றி கேளுங்கள்...",
    send: "அனுப்பு",
    newChat: "புதிய உரையாடல்",
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
    spokenUnsupported: "இந்த உலாவியில் பதில்களைப் பேசும் வசதி ஆதரிக்கப்படவில்லை.",
    voiceUnsupported: "இந்த உலாவியில் குரல் உள்ளீடு ஆதரிக்கப்படவில்லை. Chrome அல்லது Edge முயற்சிக்கவும்.",
    micDenied: "மைக்ரோஃபோன் அனுமதி மறுக்கப்பட்டது. உலாவி அமைப்புகளில் அனுமதிக்கவும்.",
    voiceFailed: "குரல் உள்ளீடு தோல்வியடைந்தது. மீண்டும் முயற்சிக்கவும்.",
    listeningStopped: "கேட்பது நிறுத்தப்பட்டது. மீண்டும் முயற்சிக்க மைக்ரோஃபோனை அழுத்தவும்.",
    cannotStart: "குரல் உள்ளீட்டைத் தொடங்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
    emptyResponse: "சாட்பாட் வெற்று பதிலை வழங்கியது.",
  },
};

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
  ta: {
    explain: "எனது தாவரப் பகுப்பாய்வு, கணிக்கப்பட்ட நோய் மற்றும் confidence score-ஐ எளிமையாக விளக்கவும்.",
    next: "இந்தப் பகுப்பாய்வின் அடிப்படையில் நான் அடுத்து என்ன செய்ய வேண்டும்?",
    prevent: "இந்த நோய் பரவுவதை எவ்வாறு தடுப்பது, மீண்டும் வரும் அபாயத்தை எவ்வாறு குறைப்பது?",
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
    // .replace(/[\*_~>|]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
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
    // Start a fresh conversation if saved data is invalid.
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

export default function ChatWidget({
  plantResult = null,
  language = "en",
}) {
  const activeLanguage = UI_TEXT[language] ? language : "en";

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

  const recognitionRef = useRef(null);
  const shouldKeepListeningRef = useRef(false);
  const voiceRestartTimerRef = useRef(null);
  const bottomRef = useRef(null);
  const inputRef = useRef(null);

  const text = getText(activeLanguage);
  const plantContext = buildPlantContext(plantResult);
  const quickPrompts = getQuickPrompts(activeLanguage);

  const hasAskedQuestion = messageHistory.some(
    (message) => message.role === "user"
  );

  // Keep the welcome message in the selected language without syncing state
  // from an effect. Once the user starts a conversation, preserve its history.
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

  // Save recent conversation history.
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

  // Scroll to the latest message.
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

  // Release microphone resources when unmounting.
  useEffect(() => {
    return () => {
      shouldKeepListeningRef.current = false;

      if (voiceRestartTimerRef.current !== null) {
        window.clearTimeout(voiceRestartTimerRef.current);
      }

      try {
        recognitionRef.current?.stop();
      } catch {
        // Recognition may already be stopped.
      }

      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }
    };
  }, []);

  const stopVoiceInput = () => {
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
      recognitionRef.current = null;
    }
  };

  const handleNewChat = () => {
    stopVoiceInput();

    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
    }

    setSpeakingIndex(null);

    setMessageHistory([
      {
        role: "assistant",
        content: getGreeting(activeLanguage),
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

    if (!content || loading) {
      return;
    }

    stopVoiceInput();

    const userMessage = {
      role: "user",
      content,
    };

    const requestMessages = [
      ...messages,
      userMessage,
    ].slice(-MAX_REQUEST_MESSAGES);

    setMessageHistory([...messages, userMessage]);

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
          language: activeLanguage,
          plant_context: plantContext,
        }),
      });

      let data;

      try {
        data = await response.json();
      } catch {
        throw new Error(
          `Chat request failed (${response.status}).`
        );
      }

      if (!response.ok) {
        throw new Error(
          typeof data.detail === "string"
            ? data.detail
            : `Chat request failed (${response.status}).`
        );
      }

      if (
        typeof data.reply !== "string" ||
        !data.reply.trim()
      ) {
        throw new Error(text.emptyResponse);
      }

      setMessageHistory((previous) => [
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
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      handleSend();
    }
  };

  // Read assistant messages aloud.
  const handleSpeak = (content, index) => {
    if (
      !("speechSynthesis" in window) ||
      typeof window.SpeechSynthesisUtterance === "undefined"
    ) {
      setError(text.spokenUnsupported);
      return;
    }

    if (speakingIndex === index) {
      window.speechSynthesis.cancel();
      setSpeakingIndex(null);
      return;
    }

    window.speechSynthesis.cancel();

    const textToSpeak = cleanTextForSpeech(content);

    if (!textToSpeak) {
      return;
    }

    const utterance =
      new window.SpeechSynthesisUtterance(textToSpeak);

    utterance.lang = getSpeechLanguage(activeLanguage);
    utterance.rate = 0.9;
    utterance.pitch = 1;

    const voices = window.speechSynthesis.getVoices();
    const locale = utterance.lang.toLowerCase();

    const matchingVoice =
      voices.find(
        (voice) => voice.lang.toLowerCase() === locale
      ) ||
      voices.find((voice) =>
        voice.lang
          .toLowerCase()
          .startsWith(`${locale.split("-")[0]}-`)
      );

    if (matchingVoice) {
      utterance.voice = matchingVoice;
    }

    utterance.onend = () => setSpeakingIndex(null);
    utterance.onerror = () => setSpeakingIndex(null);

    setSpeakingIndex(index);
    window.speechSynthesis.speak(utterance);
  };

  // Voice input with automatic restart after browser pauses.
  const handleVoiceInput = () => {
    const SpeechRecognition =
      window.SpeechRecognition ||
      window.webkitSpeechRecognition;

    if (!SpeechRecognition) {
      setError(text.voiceUnsupported);
      return;
    }

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
    };

    recognition.onresult = (event) => {
      const finalParts = [];
      const interimParts = [];

      for (
        let i = event.resultIndex;
        i < event.results.length;
        i++
      ) {
        const speechResult = event.results[i];
        const transcript = speechResult[0]?.transcript?.trim();

        if (!transcript) {
          continue;
        }

        if (speechResult.isFinal) {
          finalParts.push(transcript);
        } else {
          interimParts.push(transcript);
        }
      }

      const finalized = finalParts.join(" ").trim();

      if (finalized) {
        setInput((previous) =>
          [previous.trim(), finalized]
            .filter(Boolean)
            .join(" ")
        );
      }

      setVoiceDraft(interimParts.join(" ").trim());
    };

    recognition.onerror = (event) => {
      if (
        event.error === "not-allowed" ||
        event.error === "service-not-allowed"
      ) {
        shouldKeepListeningRef.current = false;
        setError(text.micDenied);
      } else if (event.error === "no-speech") {
        // onend will attempt to resume listening.
      } else if (event.error !== "aborted") {
        shouldKeepListeningRef.current = false;
        setError(`${text.voiceFailed} (${event.error})`);
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
            setError(text.listeningStopped);
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
      setError(text.cannotStart);
    }
  };

  const handleToggleOpen = () => {
    if (isOpen) {
      stopVoiceInput();

      if ("speechSynthesis" in window) {
        window.speechSynthesis.cancel();
      }

      setSpeakingIndex(null);
    }

    setIsOpen((previous) => !previous);
  };

  return (
    <div className="plant-chat-widget">
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

          {plantContext && (
            <div className="plant-chat-context">
              <span>🌿 {text.currentAnalysis}</span>

              <strong>
                {plantContext.plant} — {plantContext.disease}
              </strong>

              {typeof plantContext.confidence === "number" && (
                <small>
                  Model confidence:{" "}
                  {plantContext.confidence.toFixed(2)}%
                </small>
              )}
            </div>
          )}

          <div className="plant-chat-messages">
            {messages.map((message, index) => (
              <div
                key={`${index}-${message.role}`}
                className={`plant-chat-message ${
                  message.role === "user"
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
                      onClick={() =>
                        handleSpeak(message.content, index)
                      }
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
                  ? [input, voiceDraft]
                      .filter(Boolean)
                      .join(" ")
                  : input
              }
              onChange={(event) =>
                setInput(event.target.value)
              }
              onKeyDown={handleKeyDown}
              placeholder={text.placeholder}
              maxLength={3000}
              rows={2}
              disabled={loading}
              aria-label={text.placeholder}
            />

            <button
              type="button"
              className={`plant-chat-voice-button ${
                isListening ? "listening" : ""
              }`}
              onClick={handleVoiceInput}
              disabled={loading}
              title={
                isListening
                  ? "Stop listening"
                  : "Start voice input"
              }
              aria-label={
                isListening
                  ? "Stop listening"
                  : "Start voice input"
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
            <span>{text.powered}</span>
          </footer>
        </section>
      )}
    </div>
  );
}
