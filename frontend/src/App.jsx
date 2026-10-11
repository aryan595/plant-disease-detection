import { useEffect, useRef, useState } from "react";
import { LANGUAGES, TRANSLATIONS } from "./translations";
import "./App.css";
import ChatWidget from "./ChatWidget";

const LANGUAGE_STORAGE_KEY = "plantDiseaseDetector.language";
const CHAT_LANGUAGE_KEY = "plantHealthChat.language.v1";

function App() {
  const [language, setLanguage] = useState(() => {
    try {
      const saved = localStorage.getItem(LANGUAGE_STORAGE_KEY);
      return LANGUAGES.some((item) => item.value === saved) ? saved : "en";
    } catch {
      return "en";
    }
  });

  const t = TRANSLATIONS[language] || TRANSLATIONS.en;

  useEffect(() => {
    try {
      localStorage.setItem(LANGUAGE_STORAGE_KEY, language);
      localStorage.setItem(CHAT_LANGUAGE_KEY, language);
    } catch {
      // The app can still be used when browser storage is unavailable.
    }
  }, [language]);

  const [selectedImage, setSelectedImage] = useState(null);
  const [result, setResult] = useState(null);
  const [gradcamImage, setGradcamImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [isDragging, setIsDragging] = useState(false);

  const fileInputRef = useRef(null);

  // Reset everything
  const handleReset = () => {
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

  // Process uploaded file
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

  // File picker
  const handleImageChange = (event) => {
    const file = event.target.files[0];
    processFile(file);
  };

  const openFilePicker = () => {
    if (loading) {
      return;
    }

    fileInputRef.current?.click();
  };

  // Drag and drop
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

    const file = event.dataTransfer.files[0];
    processFile(file);
  };

  // Analyze image
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
      console.error(err);
      setError(err.message || t.couldNotAnalyze);
    } finally {
      setLoading(false);
    }
  };

  // Translate result status
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
                <option
                  key={item.value}
                  value={item.value}
                >
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

            {/* Upload and preview area */}
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
                    {isDragging
                      ? t.dropHere
                      : t.dragDrop}
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

            {/* Selected file */}
            {selectedImage && (
              <div className="selected-file">
                <span>📄</span>

                <span className="file-name">
                  {selectedImage.file.name}
                </span>
              </div>
            )}

            {/* Action buttons */}
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

            {/* Successful analysis message */}
            {result && !loading && (
              <div className="analysis-complete-note">
                {t.analysisSuccess} {t.useAction}{" "}
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
                    <span className="label">
                      {t.plant}
                    </span>

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

                  {result.top_3.map(
                    (prediction, index) => (
                      <div
                        className={`prediction-item ${
                          index === 0 ? "top-result" : ""
                        }`}
                        key={index}
                      >
                        <span>
                          <span className="prediction-rank">
                            {index + 1}
                          </span>

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
                    )
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

        {/* Error message */}
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

            {/* Description */}
            <div className="description-card">
              <div className="description-label">
                {result.is_healthy
                  ? t.healthAssessment
                  : t.conditionOverview}
              </div>

              <h3>{result.disease}</h3>

              <p>{result.description}</p>
            </div>

            {/* Information cards */}
            <div className="disease-info-grid">
              {/* Symptoms */}
              <div className="disease-info-card">
                <div className="disease-card-top">
                  <div className="disease-card-icon">
                    🔎
                  </div>
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
                  <div className="disease-card-icon">
                    🛠️
                  </div>
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
                  <div className="disease-card-icon">
                    🛡️
                  </div>
                </div>

                <h3>{t.prevention}</h3>

                <ul>
                  {result.prevention.map((item, index) => (
                    <li key={index}>{item}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Disclaimer */}
            <div className="disclaimer">
              <span>⚠️</span>
              <span>{t.disclaimer}</span>
            </div>
          </section>
        )}

        {/* Grad-CAM explanation */}
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
              {/* Image */}
              <div className="gradcam-image-wrap">
                <img
                  src={gradcamImage}
                  alt={t.gradcamDescription}
                  className="gradcam-image"
                />
              </div>

              {/* Explanation */}
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

        {/* Initial project information */}
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

      {/* Footer */}
      <footer className="footer">
        {t.footerBrand}
      </footer>

      <ChatWidget
        plantResult={result}
        language={language}
        // onLanguageChange={setLanguage}
      />
    </div>
  );
}

export default App;