import { useEffect, useRef, useState } from "react";
import { LANGUAGES, TRANSLATIONS } from "./translations";
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

  const [isCameraOpen, setIsCameraOpen] = useState(false);
  const [cameraReady, setCameraReady] = useState(false);
  const [cameraError, setCameraError] = useState("");

  const fileInputRef = useRef(null);
  const videoRef = useRef(null);
  const cameraStreamRef = useRef(null);
  const cameraRequestRef = useRef(0);

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

  // Validate a file, create its preview, and prepare it for analysis.
  const processFile = (file) => {
    if (!file) {
      return;
    }

    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];

    if (!allowedTypes.includes(file.type)) {
      setError(t.invalidFileType);
      return;
    }

    const maxFileSize = 10 * 1024 * 1024;

    if (file.size > maxFileSize) {
      setError(t.fileTooLarge);
      return;
    }

    const imageUrl = URL.createObjectURL(file);
    const image = new Image();

    image.onload = () => {
      const maxDimension = 6000;

      if (
        image.width > maxDimension ||
        image.height > maxDimension
      ) {
        URL.revokeObjectURL(imageUrl);
        setError(t.imageDimensionsTooLarge);
        return;
      }

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
    } catch (err) {
      console.error("Plant analysis error:", err);

      setError(err.message || t.couldNotAnalyze);
    } finally {
      setLoading(false);
    }
  };

  // Translate the result status.
  const getStatusText = () => {
    if (!result) {
      return "";
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
      <header className="header">
        <div>
          <div className="logo">{t.appTitle}</div>

          <div className="header-subtitle">
            {t.appSubtitle}
          </div>
        </div>

        <div className="header-actions">
          <div className="language-control">
            <label htmlFor="app-language">
              {t.language}
            </label>

            <select
              id="app-language"
              className="language-selector"
              value={language}
              onChange={(event) =>
                setLanguage(event.target.value)
              }
              aria-label={t.language}
            >
              {LANGUAGES.map((item) => (
                <option key={item.value} value={item.value}>
                  {item.label}
                </option>
              ))}
            </select>
          </div>

          <div className="model-badge">
            EfficientNet-B0
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
                <img
                  src={selectedImage.preview}
                  alt={t.selectedLeafAlt}
                  className="main-preview-image"
                />
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
            {!result && !loading && (
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
                    <strong>{result.plant}</strong>
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
                        : result.disease}
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
                        {prediction.plant}
                        {" — "}
                        {prediction.disease}
                      </span>

                      <strong>
                        {Number(
                          prediction.confidence
                        ).toFixed(2)}%
                      </strong>
                    </div>
                  ))}
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

        {/* General errors */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

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

              <h3>{result.disease}</h3>
              <p>{result.description}</p>
            </div>

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
                  {result.symptoms.map((item, index) => (
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
                  {result.management.map((item, index) => (
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
                  {result.prevention.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>

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

      <footer className="footer">
        {t.footerBrand}
      </footer>

      <ChatWidget
        plantResult={result}
        language={language}
      />
    </div>
  );
}

export default App;