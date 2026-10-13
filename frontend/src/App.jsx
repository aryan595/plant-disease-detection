import { useEffect, useRef, useState } from "react";
import { LANGUAGES, TRANSLATIONS } from "./translations";
import {
  getLocalizedPlant,
  getLocalizedDisease,
  getLocalizedDescription,
  getLocalizedSymptoms,
  getLocalizedManagement,
  getLocalizedPrevention,
} from "./diseaseTranslations";
import "./App.css";
import ChatWidget from "./ChatWidget";

const LANGUAGE_STORAGE_KEY = "plantDiseaseDetector.language";
const CHAT_LANGUAGE_KEY = "plantHealthChat.language.v1";

const CAMERA_TEXT = {
  en: {
    takePhoto: "Take Photo",
    title: "Take a photo of your leaf",
    hint: "Position the leaf in the frame and capture your photo.",
    capture: "Capture Photo",
    close: "Close camera",
    cancel: "Cancel",
    unavailable: "Camera access requires a supported browser and localhost or HTTPS.",
    denied: "Camera permission denied. Allow camera access in your browser settings.",
    failed: "Could not start the camera. Check whether another app is using it.",
    notReady: "The camera is not ready yet. Please wait a moment.",
    captureFailed: "Could not capture the photo. Please try again.",
  },
  hi: {
    takePhoto: "कैमरे से फोटो लें",
    title: "पत्ते की फोटो लें",
    hint: "पत्ते को फ्रेम के अंदर रखें और फोटो लें।",
    capture: "फोटो लें",
    close: "कैमरा बंद करें",
    cancel: "रद्द करें",
    unavailable: "कैमरे के लिए समर्थित ब्राउज़र और localhost या HTTPS आवश्यक है।",
    denied: "कैमरे की अनुमति नहीं मिली। ब्राउज़र सेटिंग में अनुमति दें।",
    failed: "कैमरा शुरू नहीं हो सका। जाँचें कि कोई अन्य ऐप कैमरे का उपयोग तो नहीं कर रहा।",
    notReady: "कैमरा अभी तैयार नहीं है। कृपया प्रतीक्षा करें।",
    captureFailed: "फोटो नहीं ली जा सकी। कृपया फिर प्रयास करें।",
  },
  mr: {
    takePhoto: "कॅमेऱ्याने फोटो काढा",
    title: "पानाचा फोटो काढा",
    hint: "पान फ्रेममध्ये ठेवा आणि फोटो काढा.",
    capture: "फोटो काढा",
    close: "कॅमेरा बंद करा",
    cancel: "रद्द करा",
    unavailable: "कॅमेऱ्यासाठी समर्थित ब्राउझर आणि localhost किंवा HTTPS आवश्यक आहे.",
    denied: "कॅमेऱ्याची परवानगी मिळाली नाही. ब्राउझर सेटिंग्जमध्ये परवानगी द्या.",
    failed: "कॅमेरा सुरू करता आला नाही. दुसरे ॲप कॅमेरा वापरत आहे का ते तपासा.",
    notReady: "कॅमेरा अजून तयार नाही. कृपया थोडे थांबा.",
    captureFailed: "फोटो काढता आला नाही. पुन्हा प्रयत्न करा.",
  },
  bn: {
    takePhoto: "ছবি তুলুন",
    title: "পাতার ছবি তুলুন",
    hint: "পাতাটি ফ্রেমের মধ্যে রাখুন এবং ছবি তুলুন।",
    capture: "ছবি তুলুন",
    close: "ক্যামেরা বন্ধ করুন",
    cancel: "বাতিল",
    unavailable: "ক্যামেরার জন্য সমর্থিত ব্রাউজার এবং localhost অথবা HTTPS প্রয়োজন।",
    denied: "ক্যামেরার অনুমতি দেওয়া হয়নি। ব্রাউজার সেটিংসে অনুমতি দিন।",
    failed: "ক্যামেরা চালু করা যায়নি। অন্য কোনো অ্যাপ ক্যামেরা ব্যবহার করছে কি না দেখুন।",
    notReady: "ক্যামেরা এখনও প্রস্তুত নয়। একটু অপেক্ষা করুন।",
    captureFailed: "ছবি তোলা যায়নি। আবার চেষ্টা করুন।",
  },
  ta: {
    takePhoto: "புகைப்படம் எடுக்கவும்",
    title: "இலையின் புகைப்படத்தை எடுக்கவும்",
    hint: "இலையைச் சட்டகத்தின் உள்ளே வைத்து புகைப்படம் எடுக்கவும்.",
    capture: "புகைப்படம் எடுக்கவும்",
    close: "கேமராவை மூடவும்",
    cancel: "ரத்துசெய்",
    unavailable: "கேமராவிற்கு ஆதரிக்கப்படும் உலாவியும் localhost அல்லது HTTPS இணைப்பும் தேவை.",
    denied: "கேமரா அனுமதி மறுக்கப்பட்டது. உலாவி அமைப்புகளில் அனுமதிக்கவும்.",
    failed: "கேமராவைத் தொடங்க முடியவில்லை. வேறு செயலி கேமராவைப் பயன்படுத்துகிறதா எனச் சரிபார்க்கவும்.",
    notReady: "கேமரா இன்னும் தயாராகவில்லை. சிறிது காத்திருக்கவும்.",
    captureFailed: "புகைப்படம் எடுக்க முடியவில்லை. மீண்டும் முயற்சிக்கவும்.",
  },
};

function App() {
  const [language, setLanguage] = useState(() => {
    try {
      const saved = localStorage.getItem(LANGUAGE_STORAGE_KEY);

      return LANGUAGES.some((item) => item.value === saved)
        ? saved
        : "en";
    } catch {
      return "en";
    }
  });

  const t = TRANSLATIONS[language] || TRANSLATIONS.en;
  const cameraText = CAMERA_TEXT[language] || CAMERA_TEXT.en;

  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [gradcamImage, setGradcamImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);
  const [downloadingPdf, setDownloadingPdf] = useState(false);
  const [pdfMessage, setPdfMessage] = useState(null);
  const [selectedTankSize, setSelectedTankSize] = useState(15);
  const [farmAcres, setFarmAcres] = useState(1);
  const [selectedCrop, setSelectedCrop] = useState("all");
  const [imageViewMode, setImageViewMode] = useState("original"); // "original" | "heatmap" | "split"

  const [selectedDistrict, setSelectedDistrict] = useState("Pune (पुणे)");
  const [districts, setDistricts] = useState([
    { id: "Pune (पुणे)", name: "Pune (पुणे)", name_mr: "पुणे", primary_crop: "Tomato / Vegetables" },
    { id: "Nashik - Grape Belt (नाशिक - द्राक्ष पट्टा)", name: "Nashik - Grape Belt (नाशिक - द्राक्ष पट्टा)", name_mr: "नाशिक", primary_crop: "Grapes / Onion" },
    { id: "Sangli - Tasgaon (सांगली - तासगाव)", name: "Sangli - Tasgaon (सांगली - तासगाव)", name_mr: "सांगली", primary_crop: "Grapes / Turmeric" },
    { id: "Kolhapur - Soybean Belt (कोल्हापूर - सोयाबीन पट्टा)", name: "Kolhapur - Soybean Belt (कोल्हापूर - सोयाबीन पट्टा)", name_mr: "कोल्हापूर", primary_crop: "Soybean / Sugarcane" },
    { id: "Narayangaon - Tomato Belt (नारायणगाव - टोमॅटो पट्टा)", name: "Narayangaon - Tomato Belt (नारायणगाव - टोमॅटो पट्टा)", name_mr: "नारायणगाव", primary_crop: "Tomato" },
    { id: "Solapur - Pomegranate Belt (सोलापूर - डाळिंब पट्टा)", name: "Solapur - Pomegranate Belt (सोलापूर - डाळिंब पट्टा)", name_mr: "सोलापूर", primary_crop: "Pomegranate / Jowar" },
    { id: "Ahmednagar - Rahuri MPKV (अहमदनगर - राहुरी)", name: "Ahmednagar - Rahuri MPKV (अहमदनगर - राहुरी)", name_mr: "अहमदनगर", primary_crop: "Onion / Pomegranate" },
    { id: "Satara - Strawberry & Soybean (सातारा - स्ट्रॉबेरी व सोयाबीन)", name: "Satara - Strawberry & Soybean (सातारा - स्ट्रॉबेरी व सोयाबीन)", name_mr: "सातारा", primary_crop: "Strawberry / Soybean" },
    { id: "Nagpur - Orange Belt (नागपूर - संत्रा पट्टा)", name: "Nagpur - Orange Belt (नागपूर - संत्रा पट्टा)", name_mr: "नागपूर", primary_crop: "Oranges / Cotton" },
    { id: "Amravati - Cotton & Soybean (अमरावती - कापूस व सोयाबीन)", name: "Amravati - Cotton & Soybean (अमरावती - कापूस व सोयाबीन)", name_mr: "अमरावती", primary_crop: "Soybean / Cotton" },
    { id: "Jalgaon - Banana Belt (जळगाव - केळी पट्टा)", name: "Jalgaon - Banana Belt (जळगाव - केळी पट्टा)", name_mr: "जळगाव", primary_crop: "Banana / Cotton" },
    { id: "Baramati - Sugarcane Belt (बारामती - ऊस पट्टा)", name: "Baramati - Sugarcane Belt (बारामती - ऊस पट्टा)", name_mr: "बारामती", primary_crop: "Sugarcane / Soybean" },
    { id: "Chhatrapati Sambhajinagar (छत्रपती संभाजीनगर)", name: "Chhatrapati Sambhajinagar (छत्रपती संभाजीनगर)", name_mr: "संभाजीनगर", primary_crop: "Cotton / Maize" }
  ]);
  const [districtWeather, setDistrictWeather] = useState(null);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const audioPlayerRef = useRef(null);

  // Advanced Agronomy States
  const [downloadingPmfby, setDownloadingPmfby] = useState(false);
  const [daysToHarvest, setDaysToHarvest] = useState(14);
  const [landUnit, setLandUnit] = useState("acre"); // "acre" or "guntha"
  const [chemicalsList, setChemicalsList] = useState([]);
  const [chem1, setChem1] = useState("copper_oxychloride");
  const [chem2, setChem2] = useState("chlorpyrifos");
  const [compatibilityResult, setCompatibilityResult] = useState(null);
  const [checkingCompat, setCheckingCompat] = useState(false);
  const [forecastData, setForecastData] = useState(null);
  const [kendrasData, setKendrasData] = useState(null);
  const [activeTab, setActiveTab] = useState("diagnosis"); // "diagnosis" | "spray_mix" | "forecast" | "mandi_kendras" | "recovery"
  const [farmerMode, setFarmerMode] = useState(true); // true = Farmer Mode, false = Expert Mode

  // PWA and Live GPS States
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [isAppInstalled, setIsAppInstalled] = useState(false);
  const [gpsActive, setGpsActive] = useState(false);
  const [gpsCoords, setGpsCoords] = useState(null);
  const [gpsLoading, setGpsLoading] = useState(false);
  const [, setGpsError] = useState(null);

  // PWA beforeinstallprompt and standalone detection
  useEffect(() => {
    if (
      window.matchMedia("(display-mode: standalone)").matches ||
      window.navigator.standalone === true
    ) {
      setIsAppInstalled(true);
    }

    const handleBeforeInstall = (e) => {
      e.preventDefault();
      setDeferredPrompt(e);
    };

    const handleAppInstalled = () => {
      setIsAppInstalled(true);
      setDeferredPrompt(null);
    };

    window.addEventListener("beforeinstallprompt", handleBeforeInstall);
    window.addEventListener("appinstalled", handleAppInstalled);

    return () => {
      window.removeEventListener("beforeinstallprompt", handleBeforeInstall);
      window.removeEventListener("appinstalled", handleAppInstalled);
    };
  }, []);

  const handleInstallApp = async () => {
    if (!deferredPrompt) {
      alert(
        language === "mr"
          ? "ॲप इन्स्टॉल करण्यासाठी: ब्राउझरच्या मेनूवर (⋮ किंवा Share) जाऊन 'Add to Home screen' (होम स्क्रीनवर जोडा) निवडा."
          : "To install: Tap browser menu (⋮ or Share) and select 'Add to Home Screen' or 'Install App'."
      );
      return;
    }

    deferredPrompt.prompt();
    const choice = await deferredPrompt.userChoice;
    if (choice?.outcome === "accepted") {
      setIsAppInstalled(true);
    }
    setDeferredPrompt(null);
  };

  const handleFetchGpsLocation = () => {
    if (!navigator.geolocation) {
      alert(
        language === "mr"
          ? "तुमच्या ब्राउझरमध्ये जीपीएस (Geolocation) उपलब्ध नाही."
          : "Geolocation is not supported by your browser."
      );
      return;
    }

    setGpsLoading(true);
    setGpsError(null);

    navigator.geolocation.getCurrentPosition(
      async (pos) => {
        const lat = pos.coords.latitude;
        const lon = pos.coords.longitude;
        const accuracy = Math.round(pos.coords.accuracy || 0);

        setGpsCoords({ lat, lon, accuracy });
        setGpsActive(true);
        setGpsLoading(false);

        try {
          const wRes = await fetch(`http://127.0.0.1:8000/weather?lat=${lat}&lon=${lon}`);
          const wData = await wRes.json();
          setDistrictWeather(wData);

          if (wData.nearest_district) {
            setSelectedDistrict(wData.nearest_district);
          }

          const fcRes = await fetch(`http://127.0.0.1:8000/forecast?lat=${lat}&lon=${lon}`);
          const fcData = await fcRes.json();
          setForecastData(fcData);

          if (wData.nearest_district) {
            const kRes = await fetch(
              `http://127.0.0.1:8000/krishi-kendras?district=${encodeURIComponent(wData.nearest_district)}`
            );
            const kData = await kRes.json();
            setKendrasData(kData);
          }
        } catch (err) {
          console.error("GPS Weather fetch error:", err);
        }
      },
      (err) => {
        setGpsLoading(false);
        setGpsActive(false);
        let msg = "Could not access location.";
        if (err.code === 1) {
          msg = language === "mr" ? "स्थान परवानगी नाकारली (Location Permission Denied)." : "Location access denied.";
        } else if (err.code === 2) {
          msg = language === "mr" ? "स्थान माहिती उपलब्ध नाही (Position Unavailable)." : "Position unavailable.";
        } else if (err.code === 3) {
          msg = language === "mr" ? "स्थान मिळण्यास वेळ संपला (Timeout)." : "Location request timed out.";
        }
        setGpsError(msg);
        alert(msg);
      },
      { enableHighAccuracy: true, timeout: 10000, maximumAge: 60000 }
    );
  };

  const handleClearGps = () => {
    setGpsActive(false);
    setGpsCoords(null);
    fetch(`http://127.0.0.1:8000/weather?district=${encodeURIComponent(selectedDistrict)}`)
      .then((r) => r.json())
      .then((d) => setDistrictWeather(d))
      .catch(() => {});
    fetch(`http://127.0.0.1:8000/forecast?district=${encodeURIComponent(selectedDistrict)}`)
      .then((r) => r.json())
      .then((d) => setForecastData(d))
      .catch(() => {});
  };

  // Open ChatWidget with Voice input activated immediately
  const handleOpenVoiceChat = () => {
    window.dispatchEvent(
      new CustomEvent("open-plant-chat", {
        detail: {
          startVoice: true,
          message:
            language === "mr"
              ? "नमस्कार, माझ्या पिकावर रोग आहे, काय उपाय करावा?"
              : language === "hi"
                ? "नमस्ते, मेरी फसल में बीमारी है, क्या उपाय करें?"
                : "Hello, my crop has symptoms, please guide me with treatment.",
        },
      })
    );
  };
  const [recoveryBefore, setRecoveryBefore] = useState(null);
  const [recoveryAfter, setRecoveryAfter] = useState(null);
  const [recoveryResult, setRecoveryResult] = useState(null);
  const [recoveryLoading, setRecoveryLoading] = useState(false);
  const [recoveryError, setRecoveryError] = useState(null);

  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);
  const [cameraError, setCameraError] = useState("");

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const cameraStreamRef = useRef(null);
  const cameraRequestRef = useRef(0);

  // Fetch all available districts from backend
  useEffect(() => {
    fetch("http://127.0.0.1:8000/districts")
      .then((r) => r.json())
      .then((d) => {
        if (d.districts && Array.isArray(d.districts)) {
          setDistricts(d.districts);
        }
      })
      .catch(() => {});

    fetch("http://127.0.0.1:8000/compatibility-chemicals")
      .then((r) => r.json())
      .then((d) => {
        if (d.chemicals && Array.isArray(d.chemicals)) {
          setChemicalsList(d.chemicals);
        }
      })
      .catch(() => {});
  }, []);

  // Fetch live weather, 7-day forecast & Krishi Kendras for the selected district
  useEffect(() => {
    fetch(`http://127.0.0.1:8000/weather?district=${encodeURIComponent(selectedDistrict)}`)
      .then((r) => r.json())
      .then((d) => setDistrictWeather(d))
      .catch(() => {});

    fetch(`http://127.0.0.1:8000/forecast?district=${encodeURIComponent(selectedDistrict)}`)
      .then((r) => r.json())
      .then((d) => setForecastData(d))
      .catch(() => {});

    fetch(`http://127.0.0.1:8000/krishi-kendras?district=${encodeURIComponent(selectedDistrict)}`)
      .then((r) => r.json())
      .then((d) => setKendrasData(d))
      .catch(() => {});
  }, [selectedDistrict]);

  // Remember the selected website language.
  useEffect(() => {
    try {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
      localStorage.setItem(CHAT_LANGUAGE_KEY, language);
    } catch {
      console.warn("Could not save the selected language.");
    }
  }, [language]);

  // Attach the camera stream after the video element has rendered.
  useEffect(() => {
    if (
      !isCameraOpen ||
      !cameraReady ||
      !cameraStreamRef.current ||
      !videoRef.current
    ) {
      return;
    }

    const video = videoRef.current;
    video.srcObject = cameraStreamRef.current;

    video.play().catch(() => {
      // The video may begin playing after the browser finishes loading it.
    });
  }, [isCameraOpen, cameraReady]);

  // Release the camera if this component unmounts.
  useEffect(() => {
    return () => {
      cameraRequestRef.current += 1;

      if (cameraStreamRef.current) {
        cameraStreamRef.current
          .getTracks()
          .forEach((track) => track.stop());

        cameraStreamRef.current = null;
      }
    };
  }, []);

  // Stop the camera and release its hardware resources.
  const stopCamera = () => {
    cameraRequestRef.current += 1;

    if (cameraStreamRef.current) {
      cameraStreamRef.current
        .getTracks()
        .forEach((track) => track.stop());

      cameraStreamRef.current = null;
    }

    if (videoRef.current) {
      videoRef.current.srcObject = null;
    }

    setCameraReady(false);
    setCameraError("");
    setIsCameraOpen(false);
  };

  // Start the live camera preview.
  const startCamera = async () => {
    const requestId = ++cameraRequestRef.current;

    setCameraError("");
    setCameraReady(false);
    setIsCameraOpen(true);

    if (
      !navigator.mediaDevices ||
      typeof navigator.mediaDevices.getUserMedia !== "function"
    ) {
      setCameraError(cameraText.unavailable);
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: {
          facingMode: { ideal: "environment" },
        },
        audio: false,
      });

      // Release a stream if the modal was closed while permission was pending.
      if (requestId !== cameraRequestRef.current) {
        stream.getTracks().forEach((track) => track.stop());
        return;
      }

      cameraStreamRef.current = stream;
      setCameraReady(true);
    } catch (err) {
      if (requestId !== cameraRequestRef.current) {
        return;
      }

      if (
        err.name === "NotAllowedError" ||
        err.name === "PermissionDeniedError"
      ) {
        setCameraError(cameraText.denied);
      } else {
        setCameraError(cameraText.failed);
      }
    }
  };

  // Client-side auto-compression for instant uploads on mobile network
  const compressImageFile = (file, maxDim = 1280, quality = 0.82) => {
    return new Promise((resolve) => {
      if (!file || !file.type.startsWith("image/") || file.size < 300 * 1024) {
        resolve(file);
        return;
      }
      const reader = new FileReader();
      reader.onload = (e) => {
        const img = new Image();
        img.onload = () => {
          let width = img.width;
          let height = img.height;
          if (width > maxDim || height > maxDim) {
            if (width > height) {
              height = Math.round((height * maxDim) / width);
              width = maxDim;
            } else {
              width = Math.round((width * maxDim) / height);
              height = maxDim;
            }
          }
          const canvas = document.createElement("canvas");
          canvas.width = width;
          canvas.height = height;
          const ctx = canvas.getContext("2d");
          ctx.drawImage(img, 0, 0, width, height);
          canvas.toBlob(
            (blob) => {
              if (blob && blob.size < file.size) {
                const compressedFile = new File(
                  [blob],
                  file.name.replace(/\.[^/.]+$/, ".jpg"),
                  { type: "image/jpeg", lastModified: Date.now() }
                );
                resolve(compressedFile);
              } else {
                resolve(file);
              }
            },
            "image/jpeg",
            quality
          );
        };
        img.onerror = () => resolve(file);
        img.src = e.target.result;
      };
      reader.onerror = () => resolve(file);
      reader.readAsDataURL(file);
    });
  };

  // Validate a file, compress for mobile speed, create preview, and prepare for analysis.
  const processFile = async (rawFile) => {
    if (!rawFile) {
      return;
    }

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(rawFile.type)) {
      setError(t.invalidFileType);
      return;
    }

    // Auto-compress large phone camera photos to lightweight ~200KB for instant mobile upload
    const file = await compressImageFile(rawFile, 1280, 0.82);

    const imageUrl = URL.createObjectURL(file);
    const image = new Image();

    image.onload = () => {
      setSelectedImage({
        file,
        preview: imageUrl,
      });

      setResult(null);
      setGradcamImage(null);
      setError(null);
    };

    image.onerror = () => {
      URL.revokeObjectURL(imageUrl);
      setError(t.invalidImage);
    };

    image.src = imageUrl;
  };

  // Capture the camera frame and pass it through processFile().
  const capturePhoto = () => {
    const video = videoRef.current;

    if (
      !video ||
      !video.videoWidth ||
      !video.videoHeight
    ) {
      setCameraError(cameraText.notReady);
      return;
    }

    const canvas = document.createElement("canvas");
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    const context = canvas.getContext("2d");

    if (!context) {
      setCameraError(cameraText.captureFailed);
      return;
    }

    context.drawImage(
      video,
      0,
      0,
      canvas.width,
      canvas.height
    );

    canvas.toBlob(
      (blob) => {
        if (!blob) {
          setCameraError(cameraText.captureFailed);
          return;
        }

        const file = new File(
          [blob],
          `plant-photo-${Date.now()}.jpg`,
          {
            type: "image/jpeg",
            lastModified: Date.now(),
          }
        );

        stopCamera();
        processFile(file);
      },
      "image/jpeg",
      0.92
    );
  };

  // Reset the current analysis.
  const handleReset = () => {
    if (isCameraOpen) {
      stopCamera();
    }

    setSelectedImage(null);
    setResult(null);
    setGradcamImage(null);
    setLoading(false);
    setError(null);
    setIsDragging(false);
    setDownloadingPdf(false);
    setPdfMessage(null);
    setSelectedTankSize(15);
    setFarmAcres(1);
    setSelectedCrop("all");
    setImageViewMode("original");

    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  // File picker.
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    processFile(file);

    // Allow selecting the same file again later.
    event.target.value = "";
  };

  const openFilePicker = () => {
    if (!loading) {
      fileInputRef.current?.click();
    }
  };

  // Drag and drop.
  const handleDragOver = (event) => {
    event.preventDefault();

    if (!loading) {
      setIsDragging(true);
    }
  };

  const handleDragLeave = (event) => {
    event.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (event) => {
    event.preventDefault();
    setIsDragging(false);

    if (loading) {
      return;
    }

    processFile(event.dataTransfer.files[0]);
  };

  // Play audio stream from backend TTS endpoint as fallback
  const playBackendAudio = async (speechText, lang) => {
    try {
      setIsSpeaking(true);
      const res = await fetch("http://127.0.0.1:8000/tts", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ text: speechText, language: lang }),
      });
      if (res.ok) {
        const blob = await res.blob();
        const audioUrl = URL.createObjectURL(blob);
        const audio = new Audio(audioUrl);
        audioPlayerRef.current = audio;
        audio.onended = () => {
          setIsSpeaking(false);
          audioPlayerRef.current = null;
        };
        audio.onerror = () => {
          setIsSpeaking(false);
          audioPlayerRef.current = null;
        };
        audio.play();
      } else {
        setIsSpeaking(false);
      }
    } catch {
      setIsSpeaking(false);
    }
  };

  // Text-to-speech audio advisory readout in Marathi, Hindi, or English
  const handleSpeakAdvisory = async () => {
    if (isSpeaking) {
      if (window.speechSynthesis) {
        window.speechSynthesis.cancel();
      }
      if (audioPlayerRef.current) {
        audioPlayerRef.current.pause();
        audioPlayerRef.current = null;
      }
      setIsSpeaking(false);
      return;
    }

    if (!result) return;

    const plantName = language === "mr"
      ? (result.plant_mr || getLocalizedPlant(result.plant, language) || "पीक")
      : (result.plant || "Crop");
    const diseaseName = result.is_healthy
      ? (language === "mr" ? "निरोगी" : "Healthy")
      : (language === "mr"
          ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant) || "रोग")
          : (result.disease || "Disease"));
    const sev = language === "mr" && result.severity?.level_mr
      ? result.severity.level_mr
      : (result.severity ? result.severity.level : "Mild");
    const chemRec = result.treatment_advisory?.chemical_treatments?.[0]?.commercial_name || "Bio-control spray";
    const dose = result.treatment_advisory?.chemical_treatments?.[0]?.dosage || "2 g/L";
    const sprayStatus = result.spray_window?.status === "OPTIMAL" ? "Today weather is optimal for spray." : "Check wind and humidity before spraying.";

    let speechText = "";
    let langCode = "en-IN";

    if (language === "mr") {
      langCode = "mr-IN";
      if (result.is_healthy) {
        speechText = `नमस्कार शेतकरी बंधूंनो. तुमचे ${plantName} पीक पूर्णपणे निरोगी आहे. कोणत्याही रासायनिक फवारणीची आवश्यकता नाही.`;
      } else {
        speechText = `नमस्कार शेतकरी बंधूंनो. तुमच्या ${plantName} पिकावर ${diseaseName} रोगाचा प्रादुर्भाव आढळला आहे. तीव्रता ${sev} आहे. शिफारस केलेले औषध: ${chemRec}, प्रमाण: ${dose}. १५ लिटर पंपासाठी ३० ग्रॅम औषध मिसळून फवारणी करा.`;
      }
    } else if (language === "hi") {
      langCode = "hi-IN";
      if (result.is_healthy) {
        speechText = `नमस्ते किसान भाई। आपकी ${plantName} फसल पूर्ण रूप से स्वस्थ है। किसी स्प्रे की आवश्यकता नहीं है।`;
      } else {
        speechText = `नमस्ते किसान भाई। आपकी ${plantName} फसल में ${diseaseName} रोग का प्रकोप देखा गया है। तीव्रता ${sev} है। अनुशंसित दवा: ${chemRec}, मात्रा ${dose}। 15 लीटर पंप में 30 ग्राम मिलाकर छिड़काव करें।`;
      }
    } else {
      speechText = `Hello Farmer. AgriSense diagnosis for ${plantName} is ${diseaseName}. Severity level is ${sev}. Recommended treatment is ${chemRec} at ${dose}. For a 15-liter knapsack tank, mix 30 grams. ${sprayStatus}`;
    }

    // Try Web Speech API first
    if ("speechSynthesis" in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(speechText);
      utterance.lang = langCode;
      utterance.rate = 0.95;
      utterance.pitch = 1.0;

      utterance.onstart = () => setIsSpeaking(true);
      utterance.onend = () => setIsSpeaking(false);
      utterance.onerror = () => {
        setIsSpeaking(false);
        playBackendAudio(speechText, language);
      };

      window.speechSynthesis.speak(utterance);
    } else {
      playBackendAudio(speechText, language);
    }
  };

  // Instant demo sample leaf loader
  const handleLoadSample = async (samplePath, sampleName) => {
    try {
      setLoading(true);
      setError(null);
      setResult(null);
      setGradcamImage(null);

      const res = await fetch(samplePath);
      const blob = await res.blob();
      const file = new File([blob], `${sampleName}.jpg`, { type: "image/jpeg" });

      const imageUrl = URL.createObjectURL(file);
      setSelectedImage({
        file,
        preview: imageUrl,
      });

      const formData = new FormData();
      formData.append("file", file);
      formData.append("district", selectedDistrict);

      const apiRes = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        body: formData,
      });

      if (!apiRes.ok) {
        const errorData = await apiRes.json().catch(() => ({}));
        throw new Error(errorData.detail || "Analysis request failed.");
      }

      const data = await apiRes.json();
      setResult(data);
      setGradcamImage(data.gradcam_image || null);
    } catch (err) {
      setError(err.message || "Failed to analyze sample image.");
    } finally {
      setLoading(false);
    }
  };

  // Open ChatWidget with contextual prompt about current diagnosis
  const handleOpenChatWithDiagnosis = () => {
    if (!result) return;
    const plantName = language === "mr"
      ? (result.plant_mr || getLocalizedPlant(result.plant, language) || result.plant)
      : result.plant;
    const diseaseName = result.is_healthy
      ? (language === "mr" ? "निरोगी स्थिती" : "healthy condition")
      : (language === "mr"
          ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant) || result.disease)
          : result.disease);
    const prompt =
      language === "mr"
        ? `माझ्या ${plantName} पिकावर ${diseaseName} रोग आला आहे. महाराष्ट्रातील हवामानानुसार उपाय आणि फवारणीचे वेळापत्रक सांगा.`
        : language === "hi"
          ? `मेरी ${plantName} फसल में ${diseaseName} रोग है। उचित दवा और छिड़काव की सलाह दें।`
          : `My ${plantName} plant is diagnosed with ${diseaseName}. Please explain detailed treatment and tank-mix steps for Maharashtra.`;

    window.dispatchEvent(
      new CustomEvent("open-plant-chat", { detail: { message: prompt } })
    );
  };

  // Analyze the selected or captured image.
  const handlePredict = async () => {
    if (!selectedImage || loading || result) {
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedImage.file);
      formData.append("district", selectedDistrict);
      if (selectedCrop && selectedCrop !== "all") {
        formData.append("crop", selectedCrop);
      }

      const response = await fetch(
        "http://127.0.0.1:8000/analyze",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        let message = t.analysisRequestFailed;

        try {
          const errorData = await response.json();

          if (errorData.detail) {
            message = errorData.detail;
          }
        } catch {
          // Keep the default error message.
        }

        throw new Error(message);
      }

      const data = await response.json();

      setResult(data);
      setGradcamImage(data.gradcam_image || null);
      if (data.gradcam_image) {
        setImageViewMode("heatmap");
      }
    } catch (err) {
      console.error("Plant analysis error:", err);

      setError(err.message || t.couldNotAnalyze);
    } finally {
      setLoading(false);
    }
  };

  // Download printable PDF diagnostic slip.
  const handleDownloadReport = async () => {
    if (!selectedImage || downloadingPdf) {
      return;
    }

    setDownloadingPdf(true);
    setPdfMessage(null);

    try {
      const formData = new FormData();
      formData.append("file", selectedImage.file);
      formData.append("farmer_name", "Grower / Farmer");
      formData.append("district", selectedDistrict);

      const response = await fetch(
        "http://127.0.0.1:8000/download-report",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Failed to generate PDF diagnostic report.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const plantName = result?.plant || "Crop";
      const diseaseName = result?.disease || "Diagnosis";
      a.download = `AgriSense_Diagnostic_Report_${plantName}_${diseaseName}.pdf`.replace(
        /\s+/g,
        "_"
      );
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setPdfMessage(t.downloadReportSuccess);
    } catch (err) {
      console.error("PDF download failed:", err);
      setPdfMessage(err.message || "Could not download report.");
    } finally {
      setDownloadingPdf(false);
    }
  };

  // Download PMFBY Crop Insurance Damage Assessment Certificate
  const handleDownloadPmfby = async () => {
    if (!selectedImage || downloadingPmfby) return;
    setDownloadingPmfby(true);
    setPdfMessage(null);
    try {
      const formData = new FormData();
      formData.append("file", selectedImage.file);
      formData.append("farmer_name", "Insured Farmer / Grower");
      formData.append("district", selectedDistrict);
      const farmSizeText =
        landUnit === "guntha"
          ? `${farmAcres} Gunthas (${(farmAcres / 40).toFixed(2)} Acres)`
          : `${farmAcres} Acres (${farmAcres * 40} Gunthas)`;
      formData.append("farm_size", farmSizeText);

      const response = await fetch(
        "http://127.0.0.1:8000/download-pmfby-certificate",
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        throw new Error("Could not generate PMFBY claim certificate.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      const plantName = result?.plant || "Crop";
      const diseaseName = result?.disease || "Damage";
      a.download = `PMFBY_Loss_Certificate_${plantName}_${diseaseName}.pdf`.replace(
        /\s+/g,
        "_"
      );
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
      setPdfMessage(language === "mr" ? "✓ पीक विमा पंचनामा दाखला डाउनलोड झाला!" : "✓ PMFBY Certificate downloaded successfully!");
    } catch (err) {
      console.error("PMFBY certificate error:", err);
      setPdfMessage(err.message || "Could not download PMFBY certificate.");
    } finally {
      setDownloadingPmfby(false);
    }
  };

  // Check Tank-Mix Compatibility between two chemicals
  const handleCheckCompatibility = async () => {
    if (!chem1 || !chem2) return;
    setCheckingCompat(true);
    try {
      const res = await fetch("http://127.0.0.1:8000/check-compatibility", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ chem1, chem2 }),
      });
      const data = await res.json();
      setCompatibilityResult(data);
    } catch (err) {
      console.error("Tank mix check failed:", err);
    } finally {
      setCheckingCompat(false);
    }
  };

  // Compare Recovery between Before and After images
  const handleCompareRecovery = async () => {
    if (!recoveryBefore?.file || !recoveryAfter?.file) return;
    setRecoveryLoading(true);
    setRecoveryError(null);
    try {
      const formData = new FormData();
      formData.append("before_file", recoveryBefore.file);
      formData.append("after_file", recoveryAfter.file);
      formData.append("crop", result?.plant || "Tomato");
      formData.append("disease", result?.disease || "Early Blight");

      const res = await fetch("http://127.0.0.1:8000/compare-recovery", {
        method: "POST",
        body: formData,
      });

      if (!res.ok) throw new Error("Recovery comparison failed. Please try again.");
      const data = await res.json();
      setRecoveryResult(data);
    } catch (err) {
      setRecoveryError(err.message || "Failed to compare recovery images.");
    } finally {
      setRecoveryLoading(false);
    }
  };

  // One-tap WhatsApp shareable diagnostic advisory.
  const handleShareWhatsApp = () => {
    if (!result) return;
    const isMr = language === "mr";
    const plantName = isMr
      ? (result.plant_mr || getLocalizedPlant(result.plant, language) || "पीक")
      : (result.plant || "Crop");
    const condName = result.is_healthy
      ? (isMr ? "निरोगी" : "Healthy")
      : (isMr
          ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant) || "रोग")
          : (result.disease || "Disease"));
    const sev = result.severity
      ? `${isMr && result.severity.level_mr ? result.severity.level_mr : result.severity.level} (${result.severity.affected_percentage}%)`
      : "N/A";
    const sprayRec =
      result.treatment_advisory?.chemical_treatments?.[0]?.commercial_name ||
      (isMr ? "सेंद्रिय / जैविक फवारणी" : "Bio-control / Organic spray");
    const dose =
      result.treatment_advisory?.chemical_treatments?.[0]?.dosage || (isMr ? "२ ग्रॅम/लिटर" : "2 g/L");
    const dose15L = result.treatment_advisory?.chemical_treatments?.[0]
      ?.dosage_per_liter
      ? `${(
          result.treatment_advisory.chemical_treatments[0].dosage_per_liter *
          15
        ).toFixed(0)} ग्रॅम/मिली`
      : "३० ग्रॅम";
    const sprayWin =
      result.spray_window?.status === "OPTIMAL"
        ? (isMr ? "आज फवारणीसाठी योग्य वेळ" : "Safe to spray today")
        : (isMr ? "सावधगिरी: हवामान तपासा" : "Caution: Check wind/humidity");

    const text = isMr
      ? `🌱 *अग्रीसेन्स AI पीक रोग निदान स्लिप*\n\n` +
        `🌾 *पीक:* ${plantName}\n` +
        `🔬 *रोग निदान:* ${condName}\n` +
        `📊 *तीव्रता:* ${sev}\n` +
        `🎯 *फवारणी वेळ:* ${sprayWin}\n` +
        `💊 *शिफारस औषध:* ${sprayRec} (प्रमाण: ${dose})\n` +
        `🎒 *१५L पंपाचे प्रमाण:* ${dose15L} + १० मिली स्टिकर\n\n` +
        `_अग्रीसेन्स AI शेती सल्लागार प्रणालीद्वारे निदान_`
      : `🌱 *AgriSense AI Crop Diagnostic Slip*\n\n` +
        `🌾 *Crop:* ${plantName}\n` +
        `🔬 *Diagnosis:* ${condName}\n` +
        `📊 *Severity:* ${sev}\n` +
        `🎯 *Spray Window:* ${sprayWin}\n` +
        `💊 *Recommended Spray:* ${sprayRec} (Dose: ${dose})\n` +
        `🎒 *15L Pump Tank Mix:* ${dose15L} + 10ml Spreader per tank\n\n` +
        `_Diagnosed via AgriSense Explainable AI_`;

    const url = `https://api.whatsapp.com/send?text=${encodeURIComponent(
      text
    )}`;
    window.open(url, "_blank");
  };

  // Translate the result status.
  const getStatusText = () => {
    if (!result) {
      return "";
    }

    if (result.confidence_status === "inconclusive") {
      return language === "mr" ? "⚠ अस्पष्ट / पुनर्परीक्षण आवश्यक" : "⚠ Inconclusive / Review";
    }

    if (result.confidence_status === "healthy") {
      return `✓ ${t.healthy}`;
    }

    if (result.confidence_status === "low") {
      return `⚠ ${t.lowConfidence}`;
    }

    return `✓ ${t.highConfidence}`;
  };

  return (
    <div className="app">
      {/* Header */}
      {/* Modern Uncluttered Header */}
      <header className="header">
        <div className="brand-group">
          <div className="logo-wrap">
            <span className="logo-leaf-icon">🌱</span>
            <div className="logo-text">
              <span className="logo-title">AgriSense AI</span>
              <span className="logo-badge">PRO</span>
            </div>
          </div>
          <div className="header-subtitle">
            {language === "mr" ? "स्मार्ट पीक रोग निदान व कृषी सल्लागार" : t.appSubtitle}
          </div>
        </div>

        <div className="header-toolbar">
          {/* Location & Microclimate Cluster */}
          <div className="toolbar-cluster location-cluster">
            <div className="district-control">
              <span className="cluster-icon">📍</span>
              <select
                id="app-district"
                className="district-selector"
                value={selectedDistrict}
                onChange={(e) => {
                  if (gpsActive) setGpsActive(false);
                  setSelectedDistrict(e.target.value);
                }}
                aria-label="Select Maharashtra District"
              >
                {districts.map((d) => (
                  <option key={d.id} value={d.name}>
                    {language === "mr" ? d.name_mr : d.name.split(" - ")[0]}
                  </option>
                ))}
              </select>
            </div>

            {/* Live GPS Quick Tap */}
            {gpsActive && gpsCoords ? (
              <div className="gps-active-pill" title="Live GPS Active">
                <span className="gps-dot active"></span>
                <span>GPS {gpsCoords.lat.toFixed(1)}°, {gpsCoords.lon.toFixed(1)}°</span>
                <button
                  type="button"
                  className="gps-clear-btn"
                  onClick={handleClearGps}
                  title={language === "mr" ? "जीपीएस रीसेट" : "Reset GPS"}
                >
                  ✕
                </button>
              </div>
            ) : (
              <button
                type="button"
                className={`gps-pill-btn ${gpsLoading ? "loading" : ""}`}
                onClick={handleFetchGpsLocation}
                disabled={gpsLoading}
                title={language === "mr" ? "थेट शेत GPS हवामान" : "Live Farm GPS"}
              >
                <span>{gpsLoading ? "⏳" : "🛰️"}</span>
                <span>{gpsLoading ? (language === "mr" ? "शोधत आहे" : "Locating") : "GPS"}</span>
              </button>
            )}

            {/* Weather Quick Pill */}
            {districtWeather?.weather && (
              <div className="weather-quick-pill" title="Live Microclimate Weather">
                <span>🌡️ {districtWeather.weather.temperature_c}°C</span>
                <span className="weather-divider">•</span>
                <span>💧 {districtWeather.weather.humidity_percent}%</span>
              </div>
            )}
          </div>

          {/* Right Utility Cluster */}
          <div className="toolbar-cluster utility-cluster">
            {/* Language Selector */}
            <div className="language-control">
              <span className="cluster-icon">🌐</span>
              <select
                id="app-language"
                className="language-selector"
                value={language}
                onChange={(event) => setLanguage(event.target.value)}
                aria-label={t.language}
              >
                {LANGUAGES.map((item) => (
                  <option key={item.value} value={item.value}>
                    {item.label}
                  </option>
                ))}
              </select>
            </div>

            {/* Neural Model Status Badge */}
            <div className="model-status-badge" title="Trained on 38 PlantVillage Classes">
              <span className="pulse-indicator"></span>
              <span>EfficientNet-V2</span>
            </div>

            {/* PWA Install Button */}
            <button
              type="button"
              className={`pwa-pill-btn ${isAppInstalled ? "installed" : ""}`}
              onClick={handleInstallApp}
              title={language === "mr" ? "ॲप इन्स्टॉल करा" : "Install AgriSense PWA"}
            >
              <span>{isAppInstalled ? "✓" : "📲"}</span>
              <span className="pwa-text">{isAppInstalled ? (language === "mr" ? "इन्स्टॉल झाले" : "Installed") : (language === "mr" ? "ॲप" : "App")}</span>
            </button>
          </div>
        </div>
      </header>

      <main className="main-content">
        {/* Hero */}
        <section className="hero">
          <div className="hero-badge">
            {t.heroBadge}
          </div>

          <h1>{t.heroTitle}</h1>

          <p>{t.heroDescription}</p>
        </section>

        {/* Farmer-First Navigation Dock */}
        <nav className="farmer-nav-dock" aria-label="Farmer Navigation">
          <button
            type="button"
            className={`farmer-tab-btn ${activeTab === "diagnosis" ? "active" : ""}`}
            onClick={() => setActiveTab("diagnosis")}
          >
            <span className="farmer-tab-icon">🌿</span>
            <span>{language === "mr" ? "रोग निदान (Scanner)" : language === "hi" ? "रोग निदान" : "Diagnosis"}</span>
          </button>
          <button
            type="button"
            className={`farmer-tab-btn ${activeTab === "spray_mix" ? "active" : ""}`}
            onClick={() => setActiveTab("spray_mix")}
          >
            <span className="farmer-tab-icon">🧪</span>
            <span>{language === "mr" ? "फवारणी व मिश्रण (Spray)" : language === "hi" ? "स्प्रे एवं मिश्रण" : "Spray & Tank-Mix"}</span>
          </button>
          <button
            type="button"
            className={`farmer-tab-btn ${activeTab === "forecast" ? "active" : ""}`}
            onClick={() => setActiveTab("forecast")}
          >
            <span className="farmer-tab-icon">⛅</span>
            <span>{language === "mr" ? "हवामान अंदाज (Forecast)" : language === "hi" ? "मौसम जोखिम" : "7-Day Risk"}</span>
          </button>
          <button
            type="button"
            className={`farmer-tab-btn ${activeTab === "mandi_kendras" ? "active" : ""}`}
            onClick={() => setActiveTab("mandi_kendras")}
          >
            <span className="farmer-tab-icon">🏪</span>
            <span>{language === "mr" ? "बाजारभाव व केंद्रे (Mandi)" : language === "hi" ? "मंडी व केंद्र" : "Mandi & Dealers"}</span>
          </button>
          <button
            type="button"
            className={`farmer-tab-btn ${activeTab === "recovery" ? "active" : ""}`}
            onClick={() => setActiveTab("recovery")}
          >
            <span className="farmer-tab-icon">📈</span>
            <span>{language === "mr" ? "सुधारणा ट्रॅकर (Recovery)" : language === "hi" ? "सुधार ट्रैकर" : "Recovery"}</span>
          </button>
        </nav>

        {/* Diagnosis Tab */}
        {activeTab === "diagnosis" && (
          <>
            {/* Voice Hero Consultation Banner */}
            <div className="voice-hero-banner">
              <div className="voice-hero-content">
                <div className="voice-hero-avatar">🎙️</div>
                <div className="voice-hero-text">
                  <h3>
                    {language === "mr"
                      ? "काही अडचण किंवा प्रश्न आहे का? थेट बोलून विचारा!"
                      : language === "hi"
                      ? "कोई समस्या या सवाल है? सीधे बोलकर पूछें!"
                      : "Have questions about your crop? Speak directly to AI!"}
                  </h3>
                  <p>
                    {language === "mr"
                      ? "मराठी, हिंदी किंवा इंग्रजीत बोला. आमचा AI कृषी मित्र क्षणात मार्गदर्शन करेल."
                      : language === "hi"
                      ? "अपनी भाषा में बोलें। AI कृषि मित्र तुरंत सटीक सलाह देगा।"
                      : "Voice-first agronomic advisory powered by local Krishi intelligence."}
                  </p>
                </div>
              </div>
              <button
                type="button"
                className="voice-hero-cta"
                onClick={handleOpenVoiceChat}
              >
                🎙️ {language === "mr" ? "आताच बोलून विचारा" : language === "hi" ? "बोलकर पूछें" : "Tap to Speak"}
              </button>
            </div>

            {/* Crop Selector Dock */}
            <div className="crop-selector-dock">
              <div className="crop-dock-header">
                <span className="crop-dock-title">
                  🌾 {language === "mr" ? "तुमचे पीक निवडा (AI अचूकतेसाठी):" : "Select Crop for Enhanced AI Accuracy:"}
                </span>
                {selectedCrop !== "all" && (
                  <button
                    type="button"
                    className="clear-crop-btn"
                    onClick={() => setSelectedCrop("all")}
                  >
                    {language === "mr" ? "सर्व पिके (Reset)" : "Show All Crops"}
                  </button>
                )}
              </div>
              <div className="crop-chips-scroll">
                {[
                  { id: "all", name: "All Crops", name_mr: "सर्व पिके", icon: "🌱" },
                  { id: "Tomato", name: "Tomato", name_mr: "टोमॅटो", icon: "🍅" },
                  { id: "Grape", name: "Grapes", name_mr: "द्राक्ष", icon: "🍇" },
                  { id: "Potato", name: "Potato", name_mr: "बटाटा", icon: "🥔" },
                  { id: "Soybean", name: "Soybean", name_mr: "सोयाबीन", icon: "🌿" },
                  { id: "Corn_(maize)", name: "Corn", name_mr: "मका", icon: "🌽" },
                  { id: "Apple", name: "Apple", name_mr: "सफरचंद", icon: "🍎" },
                  { id: "Pepper,_bell", name: "Capsicum", name_mr: "मिरची", icon: "🌶️" },
                ].map((c) => (
                  <button
                    key={c.id}
                    type="button"
                    className={`crop-pill ${selectedCrop === c.id ? "active" : ""}`}
                    onClick={() => setSelectedCrop(c.id)}
                  >
                    <span className="crop-icon">{c.icon}</span>
                    <span className="crop-name">{language === "mr" ? c.name_mr : c.name}</span>
                  </button>
                ))}
              </div>
            </div>

            {/* Main workspace */}
            <section className="workspace">
          {/* Image panel */}
          <div className="image-panel">
            <div className="panel-header">
              <div>
                <h2>{t.leafImage}</h2>
                <p>{t.uploadPrompt}</p>
              </div>

              <div className="step-number">01</div>
            </div>

            <input
              ref={fileInputRef}
              id="plant-image-input"
              type="file"
              accept="image/jpeg,image/png,image/webp"
              onChange={handleImageChange}
              className="hidden-file-input"
            />

            {/* View Mode Bar for Analyzed Image */}
            {selectedImage && gradcamImage && (
              <div className="image-view-mode-bar">
                <button
                  type="button"
                  className={`view-mode-btn ${imageViewMode === "original" ? "active" : ""}`}
                  onClick={() => setImageViewMode("original")}
                >
                  📷 {language === "mr" ? "मूळ पान" : "Original"}
                </button>
                <button
                  type="button"
                  className={`view-mode-btn ${imageViewMode === "heatmap" ? "active" : ""}`}
                  onClick={() => setImageViewMode("heatmap")}
                >
                  🔥 {language === "mr" ? "उष्णता नकाशा" : "AI Heatmap"}
                </button>
                <button
                  type="button"
                  className={`view-mode-btn ${imageViewMode === "split" ? "active" : ""}`}
                  onClick={() => setImageViewMode("split")}
                >
                  🔲 {language === "mr" ? "तुलना" : "Side-by-Side"}
                </button>
              </div>
            )}

            {/* Upload / preview area */}
            <div
              className={`upload-area ${
                isDragging ? "dragging" : ""
              } ${
                loading ? "disabled" : ""
              } ${
                selectedImage ? "has-image" : ""
              }`}
              onClick={
                selectedImage ? undefined : openFilePicker
              }
              onDragOver={handleDragOver}
              onDragLeave={handleDragLeave}
              onDrop={handleDrop}
              role={selectedImage ? undefined : "button"}
              tabIndex={selectedImage ? -1 : 0}
              onKeyDown={(event) => {
                if (
                  !selectedImage &&
                  (event.key === "Enter" ||
                    event.key === " ")
                ) {
                  event.preventDefault();
                  openFilePicker();
                }
              }}
            >
              {!selectedImage && (
                <>
                  <div className="upload-icon">
                    {isDragging ? "📥" : "🍃"}
                  </div>

                  <h3>
                    {isDragging ? t.dropHere : t.dragDrop}
                  </h3>

                  <p>{t.browseFiles}</p>

                  <span className="upload-button">
                    {t.chooseImage}
                  </span>

                  <span className="upload-formats">
                    {t.fileFormats}
                  </span>
                </>
              )}

              {selectedImage && (
                <>
                  {imageViewMode === "split" && gradcamImage ? (
                    <div className="split-view-row">
                      <div className="split-view-col">
                        <span className="split-label">📷 {language === "mr" ? "मूळ फोटो" : "Original"}</span>
                        <img src={selectedImage.preview} alt="Original Leaf" className="main-preview-image split" />
                      </div>
                      <div className="split-view-col">
                        <span className="split-label">🔥 {language === "mr" ? "AI उष्णता नकाशा" : "AI Heatmap"}</span>
                        <img src={gradcamImage} alt="Grad-CAM Lesion Heatmap" className="main-preview-image split" />
                      </div>
                    </div>
                  ) : (
                    <img
                      src={imageViewMode === "heatmap" && gradcamImage ? gradcamImage : selectedImage.preview}
                      alt={t.selectedLeafAlt}
                      className="main-preview-image"
                    />
                  )}
                </>
              )}
            </div>

            {/* Camera button */}
            <div className="camera-action-row">
              <button
                type="button"
                className="camera-button"
                onClick={startCamera}
                disabled={loading}
              >
                📷 {cameraText.takePhoto}
              </button>
            </div>

            {/* Quick Sample Leaves for Immediate Testing */}
            <div className="quick-sample-section">
              <span className="sample-label">
                ⚡ {language === "mr" ? "किंवा डेमो पान निवडा (त्वरीत चाचणी):" : language === "hi" ? "या डेमो पत्ती चुनें (त्वरित परीक्षण):" : "Or test with a sample leaf:"}
              </span>
              <div className="sample-chips-row">
                <button
                  type="button"
                  className="sample-chip highlight"
                  onClick={() => handleLoadSample("/samples/sample_tomato_septoria.jpg", "Tomato_Septoria_Spot")}
                  disabled={loading}
                  title="Test Tomato Septoria Leaf Spot sample"
                >
                  🍅 {language === "mr" ? "टोमॅटो सेप्टोरिया (User Photo)" : "Tomato Septoria (User Photo)"}
                </button>
                <button
                  type="button"
                  className="sample-chip"
                  onClick={() => handleLoadSample("/samples/sample_tomato_early_blight.jpg", "Tomato_Early_Blight")}
                  disabled={loading}
                  title="Test Tomato Early Blight sample"
                >
                  🍅 {language === "mr" ? "टोमॅटो करपा" : "Tomato Early Blight"}
                </button>
                <button
                  type="button"
                  className="sample-chip"
                  onClick={() => handleLoadSample("/samples/sample_grape_black_rot.jpg", "Grape_Black_Rot")}
                  disabled={loading}
                  title="Test Grape Black Rot sample"
                >
                  🍇 {language === "mr" ? "द्राक्ष काळा करपा" : "Grape Black Rot"}
                </button>
                <button
                  type="button"
                  className="sample-chip"
                  onClick={() => handleLoadSample("/samples/sample_soybean_rust.jpg", "Soybean_Rust")}
                  disabled={loading}
                  title="Test Soybean Rust sample"
                >
                  🌱 {language === "mr" ? "सोयाबीन तांबेरा" : "Soybean Rust"}
                </button>
                <button
                  type="button"
                  className="sample-chip"
                  onClick={() => handleLoadSample("/samples/sample_healthy_leaf.jpg", "Healthy_Leaf")}
                  disabled={loading}
                  title="Test Healthy Control Leaf"
                >
                  🍃 {language === "mr" ? "निरोगी पान" : "Healthy Leaf"}
                </button>
              </div>
            </div>

            {/* Selected file */}
            {selectedImage && (
              <div className="selected-file">
                <span>📄</span>

                <span className="file-name">
                  {selectedImage.file.name}
                </span>
              </div>
            )}

            {/* Image action buttons */}
            {selectedImage && (
              <div className="image-actions">
                <button
                  type="button"
                  className="change-image-button"
                  onClick={openFilePicker}
                  disabled={loading}
                >
                  🖼️ {t.changeImage}
                </button>

                <button
                  type="button"
                  className={`predict-button ${
                    result ? "analyzed" : ""
                  }`}
                  onClick={handlePredict}
                  disabled={loading || Boolean(result)}
                >
                  {loading
                    ? `⏳ ${t.analyzing}`
                    : result
                      ? `✓ ${t.analysisComplete}`
                      : `🔍 ${t.analyzeLeaf}`}
                </button>
              </div>
            )}

            {/* Analysis complete note */}
            {result && !loading && (
              <div className="analysis-complete-note">
                {t.analysisSuccess}{" "}
                <strong>{t.newAnalysis}</strong>{" "}
                {t.testAnotherLeaf}
              </div>
            )}
          </div>

          {/* Result panel */}
          <div className="result-panel">
            {/* Error Notification Card directly in result panel */}
            {error && !loading && (
              <div className="invalid-image-card">
                <div className="invalid-card-top">
                  <span className="invalid-icon">
                    {error.includes("Human") || error.includes("portrait") || error.includes("face")
                      ? "🚫👤"
                      : "🚫🍃"}
                  </span>
                  <div>
                    <h3>
                      {error.includes("Human") || error.includes("portrait") || error.includes("face")
                        ? "Human Face or Portrait Detected"
                        : error.includes("plant leaf") || error.includes("leaf")
                          ? "No Plant Leaf Detected"
                          : "Image Validation Error"}
                    </h3>
                    <p className="error-detail-text">{error}</p>
                  </div>
                </div>

                <div className="photo-guidance-box">
                  <strong>📸 Diagnostic Image Guidelines for Farmers:</strong>
                  <ul>
                    <li>Hold the camera steady and focus on a single crop leaf (Tomato, Potato, Grape, Soybean).</li>
                    <li>Ensure clear natural daylight without excessive shadow or lens glare.</li>
                    <li>Keep human faces, selfies, animals, walls, or indoor screens completely out of the frame.</li>
                  </ul>
                </div>

                <div className="invalid-card-actions">
                  <button
                    type="button"
                    className="retry-upload-button"
                    onClick={openFilePicker}
                  >
                    🖼️ Select Crop Leaf Image
                  </button>
                  <button
                    type="button"
                    className="retry-camera-button"
                    onClick={startCamera}
                  >
                    📷 Take Leaf Photo
                  </button>
                </div>
              </div>
            )}

            {!result && !loading && !error && (
              <div className="empty-result">
                <div className="empty-icon">🧠</div>

                <h2>{t.analysisResult}</h2>

                <p>{t.predictionPlaceholder}</p>
              </div>
            )}

            {/* Loading */}
            {loading && (
              <div className="loading-result">
                <div className="loading-spinner">⟳</div>

                <h2>{t.analyzingLeaf}</h2>

                <p>{t.examiningImage}</p>

                <div className="loading-progress">
                  <div className="loading-progress-fill" />
                </div>

                <span className="loading-caption">
                  {t.inferenceProgress}
                </span>
              </div>
            )}

            {/* Prediction result */}
            {result && (
              <div className="result-content">
                <div className="panel-header">
                  <div>
                    <h2>{t.analysisResult}</h2>
                    <p>AI-assisted plant assessment</p>
                  </div>

                  <div
                    className={
                      result.confidence_status === "healthy"
                        ? "result-status-badge healthy"
                        : result.confidence_status === "low"
                          ? "result-status-badge low"
                          : "result-status-badge high"
                    }
                  >
                    {getStatusText()}
                  </div>
                </div>

                {/* Plant and condition */}
                <div className="prediction-summary">
                  <div className="prediction-main">
                    <span className="label">{t.plant}</span>
                    <strong>
                      {language === "mr"
                        ? (result.plant_mr || getLocalizedPlant(result.plant, language))
                        : result.plant}
                    </strong>
                  </div>

                  <div className="prediction-main">
                    <span className="label">
                      {result.is_healthy
                        ? t.healthStatus
                        : t.detectedCondition}
                    </span>

                    <strong>
                      {result.is_healthy
                        ? t.healthy
                        : (language === "mr"
                            ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant))
                            : result.disease)}
                    </strong>
                  </div>
                </div>

                {/* Confidence */}
                <div className="confidence-box">
                  <div className="confidence-header">
                    <span>{t.modelConfidence}</span>

                    <strong>
                      {Number(result.confidence).toFixed(2)}%
                    </strong>
                  </div>

                  <div className="confidence-bar">
                    <div
                      className="confidence-fill"
                      style={{
                        width: `${Math.min(
                          Number(result.confidence),
                          100
                        )}%`,
                      }}
                    />
                  </div>
                </div>

                {/* Farmer Mode vs Expert Mode Switcher */}
                <div className="mode-switch-wrapper">
                  <div className="mode-switch-info">
                    <span>{farmerMode ? "👨‍🌾 शेतकरी सोपा मोड (थेट औषध प्रमाण व व्हॉट्सॲप)" : "🔬 सविस्तर तज्ज्ञ मोड (Grad-CAM व विमा क्लेम)"}</span>
                  </div>
                  <div className="mode-switch-pill">
                    <button
                      type="button"
                      className={`mode-pill-btn ${farmerMode ? "active" : ""}`}
                      onClick={() => setFarmerMode(true)}
                    >
                      👨‍🌾 {language === "mr" ? "शेतकरी मोड" : "Farmer Mode"}
                    </button>
                    <button
                      type="button"
                      className={`mode-pill-btn ${!farmerMode ? "active" : ""}`}
                      onClick={() => setFarmerMode(false)}
                    >
                      🔬 {language === "mr" ? "तज्ज्ञ मोड" : "Expert Mode"}
                    </button>
                  </div>
                </div>

                {/* Spoken Audio Voice Prescription Card */}
                <div className="spoken-prescription-card">
                  <div className="spoken-prescription-info">
                    <span className="spoken-sound-icon">{isSpeaking ? "🔊" : "📢"}</span>
                    <div className="spoken-prescription-text">
                      <strong>
                        {language === "mr"
                          ? "AI डॉक्टरांचा सल्ला आवाजात ऐका"
                          : language === "hi"
                          ? "AI डॉक्टर की सलाह आवाज़ में सुनें"
                          : "Listen to Spoken Agronomic Advisory"}
                      </strong>
                      <span>
                        {language === "mr"
                          ? "निदान, तीव्रता व थेट १५L पंपाचे फवारणी प्रमाण एका क्लिकवर ऐका."
                          : language === "hi"
                          ? "निदान, रोग तीव्रता और 15L पंप की खुराक सुनें।"
                          : "Complete voice diagnosis & knapsack pump dosing in your language."}
                      </span>
                    </div>
                  </div>
                  <button
                    type="button"
                    className={`spoken-play-btn ${isSpeaking ? "speaking" : ""}`}
                    onClick={handleSpeakAdvisory}
                  >
                    {isSpeaking ? (
                      <>⏹️ {language === "mr" ? "थांबवा" : "Stop"}</>
                    ) : (
                      <>🔊 {language === "mr" ? "आवाजात ऐका" : language === "hi" ? "आवाज़ में सुनें" : "Play Voice"}</>
                    )}
                  </button>
                </div>

                {/* Direct 15L Knapsack Pump Dose Highlight for Farmer Mode */}
                {farmerMode && (
                  <div className="farmer-direct-dose-box">
                    <div className="farmer-direct-dose-header">
                      <h4>🎒 {language === "mr" ? "१५ लिटर पंपासाठी थेट औषध प्रमाण:" : language === "hi" ? "15 लीटर पंप के लिए सीधी खुराक:" : "15L Knapsack Pump Direct Prescription:"}</h4>
                      <span className="farmer-dose-pill">
                        {result.treatment_advisory?.chemical_treatments?.[0]?.commercial_name || "Mancozeb 75% WP"}
                      </span>
                    </div>
                    <div className="farmer-direct-dose-instruction">
                      👉 {result.confidence_status === "inconclusive"
                        ? (language === "mr"
                            ? "विश्वास स्तर कमी असल्याने फवारणीची शिफारस थांबवली आहे. कृपया पानाचा जवळून स्पष्ट फोटो काढून पुनर्परीक्षण करा."
                            : "Prescription on hold due to low confidence. Please re-scan leaf with a clear close-up.")
                        : result.is_healthy
                          ? (language === "mr" ? "पीक पूर्णपणे निरोगी आहे. कोणत्याही रासायनिक फवारणीची गरज नाही." : "Crop is completely healthy. No chemical spray needed.")
                          : (language === "mr" 
                              ? `१५ लिटर पंपाच्या पाण्यात ${result.treatment_advisory?.chemical_treatments?.[0]?.dosage_per_liter ? (result.treatment_advisory.chemical_treatments[0].dosage_per_liter * 15).toFixed(0) : '३०'} ग्रॅम/मिली औषध आणि १० मिली स्टीकर (Spreader) मिसळून फवारणी करा.`
                              : `Mix ${(result.treatment_advisory?.chemical_treatments?.[0]?.dosage_per_liter ? (result.treatment_advisory.chemical_treatments[0].dosage_per_liter * 15).toFixed(0) : '30')}g/ml of ${(result.treatment_advisory?.chemical_treatments?.[0]?.commercial_name || 'fungicide')} + 10ml wetting sticker per 15-liter knapsack tank.`
                            )}
                    </div>
                    <p className="farmer-direct-dose-tips">
                      ⏰ {language === "mr" ? "फवारणीची योग्य वेळ: सकाळी ९ वाजेपूर्वी किंवा संध्याकाळी ४ नंतर शांत हवेत." : "Ideal spray time: Calm morning before 9 AM or evening after 4 PM."}
                    </p>
                  </div>
                )}

                {/* Quick Crosslinks inside Result */}
                <div className="quick-crosslinks-bar">
                  <button
                    type="button"
                    className="quick-crosslink-btn"
                    onClick={() => setActiveTab("spray_mix")}
                  >
                    🧪 {language === "mr" ? "औषध मिश्रण व पंपाचे बजेट तपासा" : "Check Spray Tank Mix"}
                  </button>
                  <button
                    type="button"
                    className="quick-crosslink-btn"
                    onClick={() => setActiveTab("forecast")}
                  >
                    ⛅ {language === "mr" ? "७-दिवस हवामान व बुरशी धोका पहा" : "View 7-Day Weather Risk"}
                  </button>
                  <button
                    type="button"
                    className="quick-crosslink-btn"
                    onClick={() => setActiveTab("mandi_kendras")}
                  >
                    🏪 {language === "mr" ? "जवळचे कृषी केंद्र व वाजवी भाव पहा" : "Find Krishi Kendras"}
                  </button>
                  {farmerMode && (
                    <button
                      type="button"
                      className="quick-crosslink-btn"
                      onClick={() => setFarmerMode(false)}
                      style={{ color: "#166534", fontWeight: "bold" }}
                    >
                      🔍 {language === "mr" ? "Grad-CAM उष्णता नकाशा व विमा क्लेम (Expert Mode)" : "View Grad-CAM & Insurance Claim"}
                    </button>
                  )}
                </div>

                {/* Severity Assessment */}
                {result.severity && (
                  <div className="severity-box">
                    <div className="severity-header">
                      <span className="severity-title">
                        📊 {t.severityAssessment}
                      </span>

                      <span
                        className="severity-badge"
                        style={{
                          backgroundColor:
                            result.severity.badge_color || "#f59e0b",
                        }}
                      >
                        {language === "mr" && result.severity.level_mr
                          ? result.severity.level_mr
                          : result.severity.level}
                      </span>
                    </div>

                    <div className="severity-metric-row">
                      <span>{t.leafAffected}:</span>
                      <strong>
                        {result.severity.affected_percentage}%
                      </strong>
                    </div>

                    <div className="severity-bar-track">
                      <div
                        className="severity-bar-fill"
                        style={{
                          width: `${Math.min(
                            result.severity.affected_percentage || 0,
                            100
                          )}%`,
                          backgroundColor:
                            result.severity.badge_color || "#f59e0b",
                        }}
                      />
                    </div>

                    <p className="severity-desc">
                      {language === "mr" && result.severity.description_mr
                        ? result.severity.description_mr
                        : result.severity.description_en}
                    </p>
                  </div>
                )}

                {/* Weather & Epidemic Progression Alert */}
                {result.weather_progression && (
                  <div
                    className={`weather-progression-card risk-${(
                      result.weather_progression.risk_level || "moderate"
                    ).toLowerCase()}`}
                  >
                    <div className="weather-progression-header">
                      <div className="weather-title-group">
                        <span className="weather-icon">🌦️</span>
                        <div>
                          <h4>{t.weatherRiskTitle}</h4>
                          <span className="weather-location">
                            {result.weather_progression.district ||
                              "Regional Microclimate"}
                          </span>
                        </div>
                      </div>

                      <span
                        className={`risk-pill risk-${(
                          result.weather_progression.risk_level ||
                          "moderate"
                        ).toLowerCase()}`}
                      >
                        {language === "mr" &&
                        result.weather_progression.risk_level_mr
                          ? result.weather_progression.risk_level_mr
                          : `${result.weather_progression.risk_level} Risk`}
                      </span>
                    </div>

                    <div className="weather-metrics-grid">
                      <div className="weather-metric">
                        <span className="metric-label">
                          {t.temperature}
                        </span>
                        <span className="metric-value">
                          {result.weather_progression.temperature_c}°C
                        </span>
                      </div>

                      <div className="weather-metric">
                        <span className="metric-label">{t.humidity}</span>
                        <span className="metric-value">
                          {result.weather_progression.humidity_percent}%
                        </span>
                      </div>

                      <div className="weather-metric">
                        <span className="metric-label">
                          {t.windSpeed}
                        </span>
                        <span className="metric-value">
                          {result.weather_progression.wind_speed_kmh} km/h
                        </span>
                      </div>
                    </div>

                    <div className="progression-alert-body">
                      <strong>
                        {language === "mr" &&
                        result.weather_progression.alert_title_mr
                          ? result.weather_progression.alert_title_mr
                          : result.weather_progression.alert_title_en}
                      </strong>

                      <p>
                        {language === "mr" &&
                        result.weather_progression.alert_message_mr
                          ? result.weather_progression.alert_message_mr
                          : result.weather_progression.alert_message_en}
                      </p>

                      {result.weather_progression
                        .recommended_action_en && (
                        <div className="progression-action">
                          <span>💡</span>
                          <em>
                            {language === "mr" &&
                            result.weather_progression
                              .recommended_action_mr
                              ? result.weather_progression
                                  .recommended_action_mr
                              : result.weather_progression
                                  .recommended_action_en}
                          </em>
                        </div>
                      )}
                    </div>
                  </div>
                )}

                {/* Real-Time Spray Window Feasibility */}
                {result.spray_window && (
                  <div
                    className={`spray-window-card status-${(
                      result.spray_window.status || "optimal"
                    ).toLowerCase()}`}
                  >
                    <div className="spray-window-header">
                      <div className="spray-title-group">
                        <span className="spray-icon">🎯</span>
                        <div>
                          <h4>{t.sprayWindowCardTitle}</h4>
                          <span className="spray-summary">
                            {language === "mr"
                              ? result.spray_window.summary_mr
                              : result.spray_window.summary_en}
                          </span>
                        </div>
                      </div>

                      <span
                        className="spray-status-badge"
                        style={{
                          backgroundColor:
                            result.spray_window.badge_color || "#16a34a",
                        }}
                      >
                        {result.spray_window.status === "OPTIMAL"
                          ? t.safeToSpray
                          : result.spray_window.status === "CAUTION"
                            ? t.cautionSpray
                            : t.avoidSpray}
                      </span>
                    </div>

                    <div className="spray-details-grid">
                      <div className="spray-detail-item">
                        <span className="detail-icon">⏰</span>
                        <div>
                          <strong>{t.bestWindowToday}</strong>
                          <p>
                            {language === "mr"
                              ? result.spray_window.best_hours_mr
                              : result.spray_window.best_hours_en}
                          </p>
                        </div>
                      </div>

                      <div className="spray-detail-item">
                        <span className="detail-icon">💨</span>
                        <div>
                          <strong>{t.windDriftStatus}</strong>
                          <p>
                            {language === "mr"
                              ? result.spray_window.wind_note_mr
                              : result.spray_window.wind_note_en}
                          </p>
                        </div>
                      </div>

                      <div className="spray-detail-item">
                        <span className="detail-icon">🌧️</span>
                        <div>
                          <strong>{t.rainfastnessStatus}</strong>
                          <p>
                            {language === "mr"
                              ? result.spray_window.rain_note_mr
                              : result.spray_window.rain_note_en}
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                )}

                {/* Confidence warning */}
                {result.confidence_warning && (
                  <div className="confidence-warning">
                    <span>⚠️</span>
                    <p>{result.confidence_warning}</p>
                  </div>
                )}

                {/* Healthy result */}
                {result.is_healthy && (
                  <div className="healthy-message">
                    <span>🌿</span>

                    <div>
                      <strong>{t.noDiseaseDetected}</strong>
                      <p>{t.classifiedHealthy}</p>
                    </div>
                  </div>
                )}

                {/* Top predictions */}
                <div className="top-predictions">
                  <div className="subsection-header">
                    <h3>{t.topPredictions}</h3>
                    <span>{t.modelRanking}</span>
                  </div>

                  {result.top_3.map((prediction, index) => (
                    <div
                      className={`prediction-item ${
                        index === 0 ? "top-result" : ""
                      }`}
                      key={index}
                    >
                      <span>
                        <span className="prediction-rank">
                          {index + 1}
                        </span>{" "}
                        {language === "mr"
                          ? (prediction.plant_mr || getLocalizedPlant(prediction.plant, language))
                          : prediction.plant}
                        {" — "}
                        {language === "mr"
                          ? (prediction.disease_mr || getLocalizedDisease(prediction.disease, language, prediction.class_name, prediction.plant))
                          : prediction.disease}
                      </span>

                      <strong>
                        {Number(
                          prediction.confidence
                        ).toFixed(2)}%
                      </strong>
                    </div>
                  ))}
                </div>

                {/* Maharashtra APMC Mandi Rates Card */}
                {result.mandi_rates && (
                  <div className="mandi-rates-card">
                    <div className="mandi-card-header">
                      <span className="mandi-badge">🌾 APMC MARKET RATES (बाजारभाव)</span>
                      <span className="mandi-trend">{result.mandi_rates.trend}</span>
                    </div>
                    <div className="mandi-market-title">
                      <strong>{result.mandi_rates.market_name}</strong>
                    </div>
                    <div className="mandi-price-grid">
                      <div className="mandi-stat-box modal-box">
                        <span className="mandi-stat-lbl">सरासरी भाव (Modal Rate)</span>
                        <span className="mandi-stat-val">₹{result.mandi_rates.modal_price?.toLocaleString()} / क्विंटल</span>
                        <small>(~₹{result.mandi_rates.kg_price} / किलो)</small>
                      </div>
                      <div className="mandi-stat-box range-box">
                        <span className="mandi-stat-lbl">किमान - कमाल भाव (Range)</span>
                        <span className="mandi-stat-val">₹{result.mandi_rates.min_price} - ₹{result.mandi_rates.max_price}</span>
                        <small>आवक: {result.mandi_rates.arrivals_qtl?.toLocaleString()} क्विंटल</small>
                      </div>
                    </div>
                  </div>
                )}

                {/* Consult AI Doctor Card */}
                <div className="ai-doctor-card">
                  <div className="ai-doctor-text">
                    <h4>💬 {language === "mr" ? "शंका आहे? AI कृषी डॉक्टरांशी चर्चा करा" : language === "hi" ? "AI कृषि डॉक्टर से सलाह लें" : "Need Advice? Consult AI Plant Doctor"}</h4>
                    <p>{language === "mr" ? "या रोगाचे व्यवस्थापन, फवारणी व खतांबद्दल मराठीत विचारा." : language === "hi" ? "कीटनाशक मात्रा और फसल सुरक्षा के बारे में तुरंत पूछें।" : "Get instant answers on dosage, safety intervals, and crop management."}</p>
                  </div>
                  <button
                    type="button"
                    className="ai-doctor-btn"
                    onClick={handleOpenChatWithDiagnosis}
                  >
                    💬 {language === "mr" ? "चॅट सुरू करा" : language === "hi" ? "चैट शुरू करें" : "Open AI Chat"}
                  </button>
                </div>

                {/* PDF & WhatsApp Action Buttons */}
                <div className="pdf-report-action">
                  <div className="report-action-buttons">
                    <button
                      type="button"
                      className="download-pdf-button"
                      onClick={handleDownloadReport}
                      disabled={downloadingPdf}
                    >
                      {downloadingPdf
                        ? `⏳ ${t.downloadingPdf}`
                        : `📄 ${t.downloadPdf}`}
                    </button>

                    <button
                      type="button"
                      className="pmfby-pdf-button"
                      onClick={handleDownloadPmfby}
                      disabled={downloadingPmfby}
                      title="Download Official PMFBY Crop Insurance Loss Assessment Certificate"
                    >
                      {downloadingPmfby
                        ? "⏳ Generating PMFBY..."
                        : language === "mr"
                          ? "📑 पीक विमा पंचनामा दाखला (PMFBY)"
                          : language === "hi"
                            ? "📑 फसल बीमा प्रमाण पत्र (PMFBY)"
                            : "📑 PMFBY Loss Certificate"}
                    </button>

                    <button
                      type="button"
                      className="whatsapp-share-button"
                      onClick={handleShareWhatsApp}
                      title={t.shareWhatsApp}
                    >
                      {t.shareWhatsApp}
                    </button>
                  </div>

                  {pdfMessage && (
                    <div className="pdf-message">
                      {pdfMessage}
                    </div>
                  )}
                </div>

                {/* New analysis */}
                <button
                  type="button"
                  className="reset-button"
                  onClick={handleReset}
                >
                  ↺ {t.newAnalysis}
                </button>
              </div>
            )}
          </div>
        </section>

        {/* Disease information */}
        {result && (
          <section className="disease-info-section">
            <div className="section-heading">
              <div>
                <h2>
                  {result.is_healthy
                    ? t.plantHealthInfo
                    : t.aboutDisease}
                </h2>

                <p>{t.relatedInfo}</p>
              </div>

              <div className="step-number">03</div>
            </div>

            <div className="description-card">
              <div className="description-label">
                {result.is_healthy
                  ? t.healthAssessment
                  : t.conditionOverview}
              </div>

              <h3>
                {result.is_healthy
                  ? t.healthy
                  : (language === "mr"
                      ? (result.disease_mr || getLocalizedDisease(result.disease, language, result.class_name, result.plant))
                      : result.disease)}
              </h3>
              <p>
                {language === "mr"
                  ? (result.description_mr || getLocalizedDescription(result.disease, language, result.description, result.class_name, result.plant))
                  : result.description}
              </p>
            </div>

            {/* Disease Root Cause & Progression Timeline */}
            {result.timeline && (
              <div className="disease-timeline-section">
                <div className="timeline-header">
                  <div>
                    <h3>{t.diseaseTimelineTitle}</h3>
                    <p>{t.diseaseTimelineSubtitle}</p>
                  </div>

                  <span className="timeline-urgency-badge">
                    {language === "mr"
                      ? result.timeline.curative_window.urgency_mr
                      : result.timeline.curative_window.urgency_en}
                  </span>
                </div>

                <div className="timeline-cards-row">
                  {/* Stage 1 */}
                  <div className="timeline-card stage-past">
                    <div className="stage-top">
                      <span className="stage-num">01</span>
                      <span className="stage-badge past">
                        {language === "mr"
                          ? result.timeline.stage_1_cause.badge_mr
                          : result.timeline.stage_1_cause.badge_en}
                      </span>
                    </div>

                    <h4>
                      {language === "mr"
                        ? result.timeline.stage_1_cause.title_mr
                        : result.timeline.stage_1_cause.title_en}
                    </h4>

                    <p>
                      {language === "mr"
                        ? result.timeline.stage_1_cause.description_mr
                        : result.timeline.stage_1_cause.description_en}
                    </p>
                  </div>

                  {/* Stage 2 */}
                  <div className="timeline-card stage-current">
                    <div className="stage-top">
                      <span className="stage-num">02</span>
                      <span className="stage-badge current">
                        {language === "mr"
                          ? result.timeline.stage_2_current.badge_mr
                          : result.timeline.stage_2_current.badge_en}
                      </span>
                    </div>

                    <h4>
                      {language === "mr"
                        ? result.timeline.stage_2_current.title_mr
                        : result.timeline.stage_2_current.title_en}
                    </h4>

                    <p>
                      {language === "mr"
                        ? result.timeline.stage_2_current.description_mr
                        : result.timeline.stage_2_current.description_en}
                    </p>
                  </div>

                  {/* Stage 3 */}
                  <div className="timeline-card stage-future">
                    <div className="stage-top">
                      <span className="stage-num">03</span>
                      <span className="stage-badge future">
                        {language === "mr"
                          ? result.timeline.stage_3_future.badge_mr
                          : result.timeline.stage_3_future.badge_en}
                      </span>
                    </div>

                    <h4>
                      {language === "mr"
                        ? result.timeline.stage_3_future.title_mr
                        : result.timeline.stage_3_future.title_en}
                    </h4>

                    <p>
                      {language === "mr"
                        ? result.timeline.stage_3_future.description_mr
                        : result.timeline.stage_3_future.description_en}
                    </p>
                  </div>
                </div>

                <div className="curative-window-box">
                  <span className="curative-icon">⚡</span>
                  <div>
                    <strong>{t.curativeActionWindow}:</strong>{" "}
                    <span>
                      {language === "mr"
                        ? result.timeline.curative_window.action_mr
                        : result.timeline.curative_window.action_en}
                    </span>
                  </div>
                </div>
              </div>
            )}

            <div className="disease-info-grid">
              {/* Symptoms */}
              <div className="disease-info-card">
                <div className="disease-card-top">
                  <div className="disease-card-icon">🔎</div>
                </div>

                <h3>
                  {result.is_healthy
                    ? t.healthyIndicators
                    : t.commonSymptoms}
                </h3>

                <ul>
                  {((language === "mr" && result.symptoms_mr && result.symptoms_mr.length > 0)
                    ? result.symptoms_mr
                    : (language === "mr"
                        ? getLocalizedSymptoms(result.disease, language, result.symptoms, result.class_name, result.plant)
                        : result.symptoms)
                  ).map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              {/* Management */}
              <div className="disease-info-card">
                <div className="disease-card-top">
                  <div className="disease-card-icon">🛠️</div>
                </div>

                <h3>{t.management}</h3>

                <ul>
                  {((language === "mr" && result.management_mr && result.management_mr.length > 0)
                    ? result.management_mr
                    : (language === "mr"
                        ? getLocalizedManagement(result.disease, language, result.management, result.class_name, result.plant)
                        : result.management)
                  ).map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>

              {/* Prevention */}
              <div className="disease-info-card">
                <div className="disease-card-top">
                  <div className="disease-card-icon">🛡️</div>
                </div>

                <h3>{t.prevention}</h3>

                <ul>
                  {((language === "mr" && result.prevention_mr && result.prevention_mr.length > 0)
                    ? result.prevention_mr
                    : (language === "mr"
                        ? getLocalizedPrevention(result.disease, language, result.prevention, result.class_name, result.plant)
                        : result.prevention)
                  ).map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Prescribed Treatments & Advisory */}
            {result.treatment_advisory && (
              <div className="treatments-section">
                <div className="treatments-section-header">
                  <div>
                    <h3>💊 {t.treatmentsTitle}</h3>
                    <p>ICAR & CIBRC Aligned Plant Protection Package</p>
                  </div>
                  <span className="cib-badge">ICAR / CIBRC Verified</span>
                </div>

                {/* Knapsack Pump Tank-Mix Calculator */}
                <div className="tank-calculator-box">
                  <div className="tank-calc-header">
                    <div>
                      <h4>{t.tankMixCalculatorTitle}</h4>
                      <p>{t.tankMixSubtitle}</p>
                    </div>
                    <span className="field-ready-badge">Farm Practical</span>
                  </div>

                  <div className="tank-calc-controls">
                    <div className="control-group">
                      <label>{t.selectSprayerType}</label>
                      <div className="pump-size-tabs">
                        <button
                          type="button"
                          className={`pump-tab ${
                            selectedTankSize === 15 ? "active" : ""
                          }`}
                          onClick={() => setSelectedTankSize(15)}
                        >
                          🎒 {t.knapsack15}
                        </button>
                        <button
                          type="button"
                          className={`pump-tab ${
                            selectedTankSize === 20 ? "active" : ""
                          }`}
                          onClick={() => setSelectedTankSize(20)}
                        >
                          🔋 {t.battery20}
                        </button>
                        <button
                          type="button"
                          className={`pump-tab ${
                            selectedTankSize === 200 ? "active" : ""
                          }`}
                          onClick={() => setSelectedTankSize(200)}
                        >
                          🚜 {t.tractor200}
                        </button>
                      </div>
                    </div>

                    <div className="control-group">
                      <div className="unit-toggle-header">
                        <label>{language === "mr" ? "शेत क्षेत्र (जमीन प्रमाण):" : "Farm Land Area:"}</label>
                        <div className="unit-toggle-pills">
                          <button
                            type="button"
                            className={`unit-pill ${landUnit === "guntha" ? "active" : ""}`}
                            onClick={() => { setLandUnit("guntha"); setFarmAcres(10); }}
                          >
                            गुंठा (Guntha)
                          </button>
                          <button
                            type="button"
                            className={`unit-pill ${landUnit === "acre" ? "active" : ""}`}
                            onClick={() => { setLandUnit("acre"); setFarmAcres(1); }}
                          >
                            एकर (Acre)
                          </button>
                        </div>
                      </div>

                      <div className="acres-input-row">
                        {landUnit === "guntha" ? (
                          [5, 10, 20, 30].map((g) => (
                            <button
                              key={g}
                              type="button"
                              className={`acre-chip ${farmAcres === g ? "active" : ""}`}
                              onClick={() => setFarmAcres(g)}
                            >
                              {g} {language === "mr" ? "गुंठे" : "Gunthas"}
                            </button>
                          ))
                        ) : (
                          [0.5, 1, 2, 5].map((a) => (
                            <button
                              key={a}
                              type="button"
                              className={`acre-chip ${farmAcres === a ? "active" : ""}`}
                              onClick={() => setFarmAcres(a)}
                            >
                              {a} Acre
                            </button>
                          ))
                        )}
                      </div>
                    </div>
                  </div>

                  {/* Calculations Output */}
                  {(() => {
                    const activeChem =
                      result.treatment_advisory.chemical_treatments?.[0];
                    const dosePerL = activeChem?.dosage_per_liter || 2.0;
                    const dosePerTank = (
                      selectedTankSize * dosePerL
                    ).toFixed(1);
                    const spreaderVol =
                      selectedTankSize <= 20 ? 10 : 100;
                    const tanksPerAcre = Math.round(
                      140 / selectedTankSize
                    );
                    const effectiveAcres = landUnit === "guntha" ? farmAcres / 40 : farmAcres;
                    const totalTanks = Math.max(
                      1,
                      Math.round(effectiveAcres * tanksPerAcre)
                    );
                    const totalWaterLiters = totalTanks * selectedTankSize;
                    const totalChemWeightGrams = Math.round(totalWaterLiters * dosePerL);
                    const estCostPerTank = Math.round(
                      selectedTankSize * 1.85
                    );
                    const totalEstCost = totalTanks * estCostPerTank;

                    return (
                      <div className="tank-output-grid">
                        <div className="tank-metric-card primary">
                          <span className="tank-metric-label">
                            {t.chemicalDosePerTank}
                          </span>
                          <span className="tank-metric-val">
                            {dosePerTank} g / ml
                          </span>
                          <span className="tank-metric-sub">
                            {activeChem?.commercial_name ||
                              "Prescribed Fungicide"}
                          </span>
                        </div>

                        <div className="tank-metric-card">
                          <span className="tank-metric-label">
                            {t.spreaderDosePerTank}
                          </span>
                          <span className="tank-metric-val">
                            {spreaderVol} ml
                          </span>
                          <span className="tank-metric-sub">
                            Silicon Spreader (Rainfast)
                          </span>
                        </div>

                        <div className="tank-metric-card">
                          <span className="tank-metric-label">
                            {t.totalTanksNeeded}
                          </span>
                          <span className="tank-metric-val">
                            {totalTanks} Pumps ({totalWaterLiters}L)
                          </span>
                          <span className="tank-metric-sub">
                            {landUnit === "guntha" ? `${farmAcres} Guntha` : `${farmAcres} Acre`} canopy
                          </span>
                        </div>

                        <div className="tank-metric-card">
                          <span className="tank-metric-label">
                            {language === "mr" ? "एकूण अंदाजे खर्च" : "Total Chemical Budget"}
                          </span>
                          <span className="tank-metric-val">
                            ~₹{totalEstCost}
                          </span>
                          <span className="tank-metric-sub">
                            Total {totalChemWeightGrams}g chemical
                          </span>
                        </div>
                      </div>
                    );
                  })()}
                </div>

                {/* Chemical Treatments with Pre-Harvest Interval (PHI) Lock */}
                {result.treatment_advisory.chemical_treatments?.length >
                  0 && (
                  <div className="treatment-category-card chemical">
                    <div className="category-header">
                      <h4>🧪 {t.chemicalControls}</h4>
                      <span className="badge-tag chemical-tag">
                        Targeted Curative
                      </span>
                    </div>

                    {/* Pre-Harvest Interval (PHI) Safety Slider */}
                    <div className="phi-harvest-card">
                      <div className="phi-harvest-header">
                        <span className="phi-harvest-title">
                          ⏱️ {language === "mr" ? "काढणीसाठी शिल्लक दिवस (Harvest Countdown):" : "Days Remaining Until Harvest:"}
                        </span>
                        <span className="phi-days-badge">{daysToHarvest} {language === "mr" ? "दिवस" : "Days"}</span>
                      </div>
                      <input
                        type="range"
                        min="1"
                        max="30"
                        value={daysToHarvest}
                        onChange={(e) => setDaysToHarvest(Number(e.target.value))}
                        className="phi-slider"
                      />
                      <small className="phi-hint">
                        {language === "mr"
                          ? "काढणीच्या आधी रासायनिक औषधांचा अंश (MRL Residue) फळात राहू नये म्हणून प्रतीक्षा कालावधी (PHI) तपासला जातो."
                          : "Pre-Harvest Interval (PHI) ensures safe food consumption and prevents export rejection."}
                      </small>
                    </div>

                    <div className="treatment-items-grid">
                      {result.treatment_advisory.chemical_treatments.map(
                        (chem, idx) => {
                          const isPhiViolation = chem.phi_days && daysToHarvest < chem.phi_days;
                          return (
                            <div key={idx} className={`treatment-item-card ${isPhiViolation ? 'phi-violation' : ''}`}>
                              <div className="treatment-item-top">
                                <strong className="commercial-name">
                                  {chem.commercial_name}
                                </strong>
                                <span className="active-ingredient">
                                  ({chem.chemical_name})
                                </span>
                              </div>

                              <div className="treatment-specs">
                                <span className="dosage-pill">
                                  💧 {t.dosage}: {chem.dosage}
                                </span>

                                {chem.approx_price_inr && (
                                  <span className="price-pill">
                                    🏷️ {chem.approx_price_inr}
                                  </span>
                                )}

                                {chem.phi_days && (
                                  <span className={`phi-pill ${isPhiViolation ? 'phi-warn' : 'phi-safe'}`}>
                                    ⏱️ PHI: {chem.phi_days} days
                                  </span>
                                )}
                              </div>

                              {isPhiViolation && (
                                <div className="phi-hazard-alert">
                                  ⚠️ {language === "mr"
                                    ? `धोका: काढणीस फक्त ${daysToHarvest} दिवस शिल्लक आहेत (किमान प्रतीक्षा: ${chem.phi_days} दिवस). रासायनिक अवशेषांचा धोका असल्याने ही फवारणी करू नका! सेंद्रिय पर्याय वापरा.`
                                    : `RESIDUE HAZARD: Harvest in ${daysToHarvest} days (Minimum wait: ${chem.phi_days} days). Do NOT spray! Switch to 0-day bio-fungicides.`}
                                </div>
                              )}

                              <p className="treatment-notes">
                                {chem.instructions}
                              </p>
                            </div>
                          );
                        }
                      )}
                    </div>
                  </div>
                )}

                {/* Organic Treatments */}
                {result.treatment_advisory.organic_treatments?.length >
                  0 && (
                  <div className="treatment-category-card organic">
                    <div className="category-header">
                      <h4>🌱 {t.organicControls}</h4>
                      <span className="badge-tag organic-tag">
                        100% Eco-Safe Bio-Control
                      </span>
                    </div>

                    <div className="treatment-items-grid">
                      {result.treatment_advisory.organic_treatments.map(
                        (org, idx) => (
                          <div
                            key={idx}
                            className="treatment-item-card organic-item"
                          >
                            <div className="treatment-item-top">
                              <strong className="commercial-name">
                                {org.name}
                              </strong>
                            </div>

                            <div className="treatment-specs">
                              <span className="dosage-pill organic-dose">
                                🌿 {t.dosage}: {org.dosage}
                              </span>

                              {org.approx_price_inr && (
                                <span className="price-pill">
                                  🏷️ {org.approx_price_inr}
                                </span>
                              )}
                            </div>

                            <p className="treatment-notes">
                              {org.notes}
                            </p>
                          </div>
                        )
                      )}
                    </div>
                  </div>
                )}
              </div>
            )}

            <div className="disclaimer">
              <span>⚠️</span>
              <span>{t.disclaimer}</span>
            </div>
          </section>
        )}

        {/* Grad-CAM */}
        {gradcamImage && (
          <section className="gradcam-section">
            <div className="panel-header">
              <div>
                <div className="section-mini-label">
                  {t.explainableAI}
                </div>

                <h2>{t.gradcamTitle}</h2>
                <p>{t.gradcamDescription}</p>
              </div>

              <div className="step-number">04</div>
            </div>

            <div className="gradcam-content">
              <div className="gradcam-image-wrap">
                <img
                  src={gradcamImage}
                  alt={t.gradcamDescription}
                  className="gradcam-image"
                />
              </div>

              <div className="gradcam-info">
                <div className="gradcam-explanation-box">
                  <div className="explanation-icon">🧠</div>

                  <div>
                    <h3>{t.howAILooked}</h3>
                    <p>{t.gradcamExplanation}</p>
                  </div>
                </div>

                <div className="gradcam-points">
                  <div className="gradcam-point">
                    <span className="point-icon">01</span>

                    <div>
                      <strong>{t.prediction}</strong>
                      <p>{t.modelIdentifies}</p>
                    </div>
                  </div>

                  <div className="gradcam-point">
                    <span className="point-icon">02</span>

                    <div>
                      <strong>{t.attention}</strong>
                      <p>{t.heatmapShows}</p>
                    </div>
                  </div>

                  <div className="gradcam-point">
                    <span className="point-icon">03</span>

                    <div>
                      <strong>{t.interpretation}</strong>
                      <p>{t.warmerAreas}</p>
                    </div>
                  </div>
                </div>

                <div className="gradcam-note">
                  <span>💡</span>
                  <span>{t.gradcamNote}</span>
                </div>
              </div>
            </div>
          </section>
        )}

        {/* Project information */}
        {!selectedImage && (
          <section className="info-section">
            <div className="info-card">
              <div className="info-number">55</div>

              <div>
                <h3>{t.diseaseClasses}</h3>
                <p>{t.recognizesConditions}</p>
              </div>
            </div>

            <div className="info-card">
              <div className="info-number">95.58%</div>

              <div>
                <h3>{t.testAccuracy}</h3>
                <p>{t.untouchedTest}</p>
              </div>
            </div>

            <div className="info-card">
              <div className="info-number">🔥</div>

              <div>
                <h3>{t.explainableCardTitle}</h3>
                <p>{t.gradcamProvides}</p>
              </div>
            </div>
          </section>
        )}
          </>
        )}

        {/* Spray & Tank-Mix Tab */}
        {activeTab === "spray_mix" && (
          <>
            <section className="tankmix-checker-section">
              <h3>🧪 {language === "mr" ? "रासायनिक मिश्रण सुसंगतता व फवारणी (Tank-Mix & Spray Safety)" : "Chemical Tank-Mix & Spray Safety Checker"}</h3>
              <p>{language === "mr" ? "दोन औषधे किंवा खते एकाच पंपात मिसळण्यापूर्वी रासायनिक विरोध किंवा पाने जळण्याचा धोका तपासा." : "Verify whether two chemicals or foliar fertilizers can be mixed safely in the same spray tank."}</p>
              <div className="tankmix-select-grid">
                <div className="compat-field">
                  <label>{language === "mr" ? "औषध १ (Chemical 1):" : "Product 1:"}</label>
                  <select value={chem1} onChange={(e) => setChem1(e.target.value)}>
                    {chemicalsList.map((c) => (
                      <option key={c.id} value={c.id}>{c.name} ({c.category})</option>
                    ))}
                  </select>
                </div>
                <div className="compat-field">
                  <label>{language === "mr" ? "औषध २ (Chemical 2):" : "Product 2:"}</label>
                  <select value={chem2} onChange={(e) => setChem2(e.target.value)}>
                    {chemicalsList.map((c) => (
                      <option key={c.id} value={c.id}>{c.name} ({c.category})</option>
                    ))}
                  </select>
                </div>
                <button
                  type="button"
                  className="compat-check-btn"
                  onClick={handleCheckCompatibility}
                  disabled={checkingCompat}
                >
                  {checkingCompat ? "⏳ Checking..." : language === "mr" ? "सुसंगतता तपासा" : "Check Mix"}
                </button>
              </div>

              {compatibilityResult && (
                <div className="compat-result-card" style={{ borderColor: compatibilityResult.badge_color, background: compatibilityResult.badge_color + "15" }}>
                  <span className="compat-badge" style={{ background: compatibilityResult.badge_color }}>
                    {compatibilityResult.status}
                  </span>
                  <h4>{language === "mr" ? compatibilityResult.title_mr : compatibilityResult.title_en}</h4>
                  <p>{language === "mr" ? compatibilityResult.explanation_mr : compatibilityResult.explanation_en}</p>
                  <small>💡 {compatibilityResult.recommendation}</small>
                </div>
              )}
            </section>

            {/* Knapsack Pump & Water Budget Calculator Card */}
            <div className="treatments-section" style={{ marginTop: "24px" }}>
              <div className="tank-calculator-box">
                <div className="tank-calc-header">
                  <div>
                    <h4>🎒 {t.tankMixCalculatorTitle}</h4>
                    <p>{t.tankMixSubtitle}</p>
                  </div>
                  <span className="field-ready-badge">Farm Practical</span>
                </div>

                <div className="tank-calc-controls">
                  <div className="control-group">
                    <label>{t.selectSprayerType}</label>
                    <div className="pump-size-tabs">
                      <button
                        type="button"
                        className={`pump-tab ${selectedTankSize === 15 ? "active" : ""}`}
                        onClick={() => setSelectedTankSize(15)}
                      >
                        🎒 {t.knapsack15}
                      </button>
                      <button
                        type="button"
                        className={`pump-tab ${selectedTankSize === 20 ? "active" : ""}`}
                        onClick={() => setSelectedTankSize(20)}
                      >
                        🔋 {t.battery20}
                      </button>
                      <button
                        type="button"
                        className={`pump-tab ${selectedTankSize === 200 ? "active" : ""}`}
                        onClick={() => setSelectedTankSize(200)}
                      >
                        🚜 {t.tractor200}
                      </button>
                    </div>
                  </div>

                  <div className="control-group">
                    <div className="unit-toggle-header">
                      <label>{language === "mr" ? "शेत क्षेत्र (जमीन प्रमाण):" : "Farm Land Area:"}</label>
                      <div className="unit-toggle-pills">
                        <button
                          type="button"
                          className={`unit-pill ${landUnit === "guntha" ? "active" : ""}`}
                          onClick={() => { setLandUnit("guntha"); setFarmAcres(10); }}
                        >
                          गुंठा (Guntha)
                        </button>
                        <button
                          type="button"
                          className={`unit-pill ${landUnit === "acre" ? "active" : ""}`}
                          onClick={() => { setLandUnit("acre"); setFarmAcres(1); }}
                        >
                          एकर (Acre)
                        </button>
                      </div>
                    </div>

                    <div className="acres-input-row">
                      {landUnit === "guntha" ? (
                        [5, 10, 20, 30].map((g) => (
                          <button
                            key={g}
                            type="button"
                            className={`acre-chip ${farmAcres === g ? "active" : ""}`}
                            onClick={() => setFarmAcres(g)}
                          >
                            {g} {language === "mr" ? "गुंठे" : "Gunthas"}
                          </button>
                        ))
                      ) : (
                        [0.5, 1, 2, 5].map((a) => (
                          <button
                            key={a}
                            type="button"
                            className={`acre-chip ${farmAcres === a ? "active" : ""}`}
                            onClick={() => setFarmAcres(a)}
                          >
                            {a} Acre
                          </button>
                        ))
                      )}
                    </div>
                  </div>
                </div>

                {(() => {
                  const activeChem =
                    result?.treatment_advisory?.chemical_treatments?.[0] || {
                      commercial_name: "Mancozeb 75% WP",
                      dosage_per_liter: 2.0,
                    };
                  const dosePerL = activeChem.dosage_per_liter || 2.0;
                  const dosePerTank = (selectedTankSize * dosePerL).toFixed(1);
                  const spreaderVol = selectedTankSize <= 20 ? 10 : 100;
                  const tanksPerAcre = Math.round(140 / selectedTankSize);
                  const effectiveAcres = landUnit === "guntha" ? farmAcres / 40 : farmAcres;
                  const totalTanks = Math.max(1, Math.round(effectiveAcres * tanksPerAcre));
                  const totalWaterLiters = totalTanks * selectedTankSize;
                  const totalChemWeightGrams = Math.round(totalWaterLiters * dosePerL);
                  const estCostPerTank = Math.round(selectedTankSize * 1.85);
                  const totalEstCost = totalTanks * estCostPerTank;

                  return (
                    <div className="tank-output-grid">
                      <div className="tank-metric-card primary">
                        <span className="tank-metric-label">{t.chemicalDosePerTank}</span>
                        <span className="tank-metric-val">{dosePerTank} g / ml</span>
                        <span className="tank-metric-sub">{activeChem.commercial_name || "Prescribed Fungicide"}</span>
                      </div>
                      <div className="tank-metric-card">
                        <span className="tank-metric-label">{t.spreaderDosePerTank}</span>
                        <span className="tank-metric-val">{spreaderVol} ml</span>
                        <span className="tank-metric-sub">Silicon Spreader (Rainfast)</span>
                      </div>
                      <div className="tank-metric-card">
                        <span className="tank-metric-label">{t.totalTanksNeeded}</span>
                        <span className="tank-metric-val">{totalTanks} Pumps ({totalWaterLiters}L)</span>
                        <span className="tank-metric-sub">{landUnit === "guntha" ? `${farmAcres} Guntha` : `${farmAcres} Acre`} canopy</span>
                      </div>
                      <div className="tank-metric-card">
                        <span className="tank-metric-label">{language === "mr" ? "एकूण अंदाजे खर्च" : "Total Chemical Budget"}</span>
                        <span className="tank-metric-val">~₹{totalEstCost}</span>
                        <span className="tank-metric-sub">Total {totalChemWeightGrams}g chemical</span>
                      </div>
                    </div>
                  );
                })()}
              </div>

              {/* Pre-Harvest Interval (PHI) Harvest Safety Card */}
              <div className="phi-harvest-card" style={{ marginTop: "16px" }}>
                <div className="phi-harvest-header">
                  <span className="phi-harvest-title">
                    ⏱️ {language === "mr" ? "काढणीसाठी शिल्लक दिवस (Pre-Harvest Interval - PHI):" : "Days Remaining Until Crop Harvest:"}
                  </span>
                  <span className="phi-days-badge">{daysToHarvest} {language === "mr" ? "दिवस" : "Days"}</span>
                </div>
                <input
                  type="range"
                  min="1"
                  max="30"
                  value={daysToHarvest}
                  onChange={(e) => setDaysToHarvest(Number(e.target.value))}
                  className="phi-slider"
                />
                <small className="phi-hint">
                  {language === "mr"
                    ? "काढणीच्या १० ते १४ दिवस आधी रासायनिक फवारणी टाळावी, अन्यथा पिकावर विषारी औषध शिल्लक राहू शकते."
                    : "Ensure chemical spray is completely suspended before harvest to avoid chemical residue."}
                </small>
              </div>
            </div>
          </>
        )}

        {/* 7-Day Epidemic Forecast Strip */}
        {activeTab === "forecast" && (
          <>
            {forecastData && forecastData.forecast_days ? (
              <section className="forecast-section">
                <h3>📅 {language === "mr" ? `७ दिवसांचा हवामान व बुरशी प्रादुर्भाव अंदाज (${forecastData.district_mr})` : `7-Day Weather & Epidemic Forecast (${forecastData.district})`}</h3>
                <p>{language === "mr" ? "हवामानानुसार पुढील ७ दिवसांतील बुरशी रोगाचा संभाव्य धोका व फवारणीसाठी योग्य दिवस." : "Daily forecast of fungal infection pressure, rain wash-off risks, and optimal spray windows."}</p>
                <div className="forecast-grid">
                  {forecastData.forecast_days.map((day, i) => (
                    <div key={i} className="forecast-day-card">
                      <div className="forecast-day-date">{day.date}</div>
                      <div className="forecast-day-temp">{day.temp_range}</div>
                      <div className="forecast-day-rain">🌧️ {day.rain_mm}mm ({day.rain_probability}%)</div>
                      <span className="forecast-day-badge" style={{ background: day.badge_color }}>
                        {day.risk_badge}
                      </span>
                    </div>
                  ))}
                </div>
              </section>
            ) : (
              <div style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
                ⏳ {language === "mr" ? "हवामान अंदाज लोड होत आहे..." : "Loading 7-Day Forecast..."}
              </div>
            )}
          </>
        )}

        {/* Krishi Kendra Directory & Pricing Guide */}
        {activeTab === "mandi_kendras" && (
          <>
            {kendrasData ? (
              <section className="krishi-kendra-section">
                <h3>🏪 {language === "mr" ? `अधिकृत कृषी सेवा केंद्र व वाजवी दर (${selectedDistrict})` : `Registered Krishi Seva Kendras & Pricing (${selectedDistrict})`}</h3>
                <div className="kendras-grid">
                  {kendrasData.kendras.map((k, idx) => (
                    <div key={idx} className="kendra-card">
                      <strong>{k.name}</strong>
                      <p>📍 {k.address}</p>
                      <p>🏷️ {k.type}</p>
                      <a href={`tel:${k.phone}`}>📞 {k.phone}</a>
                    </div>
                  ))}
                </div>

                <h4>🏷️ {language === "mr" ? "प्रमाणित कीटकनाशक व बुरशीनाशक वाजवी दर मार्गदर्शक (Fair MRP Guide)" : "CIB&RC Agrochemical Fair MRP Benchmark"}</h4>
                <div className="pricing-table-wrap">
                  <table className="pricing-table">
                    <thead>
                      <tr>
                        <th>{language === "mr" ? "औषध घटक (Formulation)" : "Formulation"}</th>
                        <th>{language === "mr" ? "पॅकिंग (Pack)" : "Pack"}</th>
                        <th>{language === "mr" ? "वाजवी MRP दर" : "Fair Price (INR)"}</th>
                        <th>{language === "mr" ? "प्रसिद्ध ब्रँड्स" : "Brands"}</th>
                      </tr>
                    </thead>
                    <tbody>
                      {kendrasData.pricing_guide.map((p, idx) => (
                        <tr key={idx}>
                          <td><strong>{p.formulation}</strong></td>
                          <td>{p.pack_size}</td>
                          <td><span style={{ color: '#166534', fontWeight: 'bold' }}>{p.fair_mrp_inr}</span></td>
                          <td>{p.popular_brands}</td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>
              </section>
            ) : (
              <div style={{ textAlign: "center", padding: "40px", color: "#64748b" }}>
                ⏳ {language === "mr" ? "कृषी केंद्र माहिती लोड होत आहे..." : "Loading Krishi Kendra directory..."}
              </div>
            )}
          </>
        )}

        {/* Crop Recovery Comparison Tracker */}
        {activeTab === "recovery" && (
          <section className="recovery-tracker-section">
            <h3>📈 {language === "mr" ? "फवारणीनंतरचा गुण व रोगमुक्ती तपासणी (Recovery Tracker)" : "Crop Disease Recovery & Efficacy Tracker"}</h3>
            <p>{language === "mr" ? "फवारणीपूर्वीचा (Day 0) आणि फवारणीनंतरचा (Day 5) फोटो अपलोड करून रोग किती टक्के नियंत्रणात आला ते तपासा." : "Upload 'Before Spray' and 'After Spray' leaf photos to verify treatment efficacy and lesion suppression percentage."}</p>

            <div className="recovery-upload-grid">
              <label className="recovery-dropzone">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) setRecoveryBefore({ file: f, preview: URL.createObjectURL(f) });
                  }}
                />
                {recoveryBefore?.preview ? (
                  <img src={recoveryBefore.preview} alt="Before Spray" />
                ) : (
                  <div>
                    <span style={{ fontSize: "2rem" }}>📸</span>
                    <p><strong>{language === "mr" ? "१. फवारणीपूर्वीचा फोटो (Day 0)" : "1. Before Spray Photo"}</strong></p>
                  </div>
                )}
              </label>

              <label className="recovery-dropzone">
                <input
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    const f = e.target.files?.[0];
                    if (f) setRecoveryAfter({ file: f, preview: URL.createObjectURL(f) });
                  }}
                />
                {recoveryAfter?.preview ? (
                  <img src={recoveryAfter.preview} alt="After Spray" />
                ) : (
                  <div>
                    <span style={{ fontSize: "2rem" }}>🌿</span>
                    <p><strong>{language === "mr" ? "२. फवारणीनंतरचा फोटो (Day 4-7)" : "2. After Spray Photo"}</strong></p>
                  </div>
                )}
              </label>
            </div>

            <button
              type="button"
              className="recovery-compare-btn"
              onClick={handleCompareRecovery}
              disabled={!recoveryBefore || !recoveryAfter || recoveryLoading}
            >
              {recoveryLoading ? "⏳ Comparing..." : language === "mr" ? "गुण व सुधारणा तपासा" : "Compare Recovery Score"}
            </button>

            {recoveryError && <div className="phi-hazard-alert">⚠️ {recoveryError}</div>}

            {recoveryResult && (
              <div className="recovery-result-box">
                <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <h4>{recoveryResult.status_badge}</h4>
                  <strong style={{ color: "#166534", fontSize: "1.2rem" }}>
                    {recoveryResult.improvement_pct > 0 ? `+${recoveryResult.improvement_pct}% Improvement` : `${recoveryResult.improvement_pct}%`}
                  </strong>
                </div>
                <p>{language === "mr" ? recoveryResult.message_mr : recoveryResult.message_en}</p>
                <small>👉 {recoveryResult.actionable_next_step}</small>
              </div>
            )}
          </section>
        )}
      </main>

      {/* Camera modal */}
      {isCameraOpen && (
        <div
          className="camera-modal-overlay"
          onMouseDown={(event) => {
            if (event.target === event.currentTarget) {
              stopCamera();
            }
          }}
        >
          <section
            className="camera-modal"
            role="dialog"
            aria-modal="true"
            aria-labelledby="camera-modal-title"
          >
            <div className="camera-modal-header">
              <h2 id="camera-modal-title">
                {cameraText.title}
              </h2>

              <button
                type="button"
                className="camera-close-button"
                onClick={stopCamera}
                aria-label={cameraText.close}
                title={cameraText.close}
              >
                ×
              </button>
            </div>

            <p className="camera-instructions">
              {cameraText.hint}
            </p>

            {cameraError && (
              <div className="camera-error" role="alert">
                ⚠️ {cameraError}
              </div>
            )}

            <video
              ref={videoRef}
              className="camera-video"
              autoPlay
              playsInline
              muted
              aria-label={cameraText.title}
            />

            <div className="camera-modal-actions">
              <button
                type="button"
                className="camera-cancel-button"
                onClick={stopCamera}
              >
                {cameraText.cancel}
              </button>

              <button
                type="button"
                className="camera-capture-button"
                onClick={capturePhoto}
                disabled={!cameraReady || Boolean(cameraError)}
              >
                📸 {cameraText.capture}
              </button>
            </div>
          </section>
        </div>
      )}

      {/* Maharashtra Kisan Helpline Directory */}
      <section className="kisan-helpline-card">
        <h3>📞 {language === 'mr' ? 'शेतकरी मदत व संपर्क केंद्र (महाराष्ट्र)' : language === 'hi' ? 'किसान हेल्पलाइन एवं सहायता केंद्र' : 'Kisan Support & Agronomy Helplines (Maharashtra)'}</h3>
        <div className="helpline-grid">
          <a href="tel:18001801551" className="helpline-item">
            <span className="helpline-icon">🌾</span>
            <div>
              <strong>{language === 'mr' ? 'किसान कॉल सेंटर (टोल-फ्री)' : language === 'hi' ? 'किसान कॉल सेंटर (टोल-फ्री)' : 'Kisan Call Centre (Toll-Free)'}</strong>
              <span>📞 1800-180-1551</span>
            </div>
          </a>
          <a href="tel:18002334000" className="helpline-item">
            <span className="helpline-icon">🚜</span>
            <div>
              <strong>{language === 'mr' ? 'महाराष्ट्र कृषी विभाग हेल्पलाइन' : language === 'hi' ? 'महाराष्ट्र कृषि विभाग हेल्पलाइन' : 'Maharashtra Krishi Helpline'}</strong>
              <span>📞 1800-233-4000</span>
            </div>
          </a>
          <a href="tel:02426243208" className="helpline-item">
            <span className="helpline-icon">🏛️</span>
            <div>
              <strong>{language === 'mr' ? 'महात्मा फुले कृषी विद्यापीठ (राहुरी)' : language === 'hi' ? 'महात्मा फुले कृषि विश्वविद्यालय (राहुरी)' : 'MPKV Rahuri Agronomy Cell'}</strong>
              <span>📞 02426-243208</span>
            </div>
          </a>
          <a href="tel:02025537033" className="helpline-item">
            <span className="helpline-icon">🔬</span>
            <div>
              <strong>{language === 'mr' ? 'कृषी विज्ञान केंद्र (KVK Pune/Baramati)' : language === 'hi' ? 'कृषि विज्ञान केंद्र (KVK)' : 'Krishi Vigyan Kendra (KVK)'}</strong>
              <span>📞 020-25537033</span>
            </div>
          </a>
        </div>
      </section>

      <footer className="footer">
        {t.footerBrand}
      </footer>

      <ChatWidget
        plantResult={result}
        language={language}
        onLanguageChange={setLanguage}
      />
    </div>
  );
}

export default App;