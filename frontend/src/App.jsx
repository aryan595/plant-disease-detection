import { useRef, useState } from "react";
import "./App.css";
import ChatWidget from "./ChatWidget";


function App() {

  const [selectedImage, setSelectedImage] = useState(null);

  const [result, setResult] = useState(null);

  const [gradcamImage, setGradcamImage] = useState(null);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState(null);

  const [isDragging, setIsDragging] = useState(false);

  const fileInputRef = useRef(null);


  // =========================================
  // Reset everything
  // =========================================

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


  // =========================================
  // Process uploaded file
  // =========================================

  const processFile = (file) => {

    if (!file) {
      return;
    }


    const allowedTypes = [
      "image/jpeg",
      "image/png",
      "image/webp",
    ];


    // -------------------------------------
    // File type validation
    // -------------------------------------

    if (!allowedTypes.includes(file.type)) {

      setError(
        "Invalid file type. Please select a JPG, PNG, or WEBP image."
      );

      return;
    }


    // -------------------------------------
    // File size validation
    // -------------------------------------

    const maxFileSize =
      10 * 1024 * 1024;


    if (file.size > maxFileSize) {

      setError(
        "Image is too large. Maximum allowed size is 10 MB."
      );

      return;
    }


    // -------------------------------------
    // Create preview
    // -------------------------------------

    const imageUrl =
      URL.createObjectURL(file);


    const image =
      new Image();


    image.onload = () => {

      const maxDimension = 6000;


      if (
        image.width > maxDimension ||
        image.height > maxDimension
      ) {

        URL.revokeObjectURL(imageUrl);

        setError(
          "Image dimensions are too large. Maximum allowed dimensions are 6000 × 6000 pixels."
        );

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

      setError(
        "The selected file is not a valid image."
      );

    };


    image.src = imageUrl;

  };


  // =========================================
  // File picker
  // =========================================

  const handleImageChange = (event) => {

    const file =
      event.target.files[0];

    processFile(file);

  };


  const openFilePicker = () => {

    if (loading) {
      return;
    }

    fileInputRef.current?.click();

  };


  // =========================================
  // Drag & Drop
  // =========================================

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


    const file =
      event.dataTransfer.files[0];


    processFile(file);

  };


  // =========================================
  // Analyze image
  // =========================================

  const handlePredict = async () => {

    if (!selectedImage || loading || result) {
      return;
    }


    setLoading(true);

    setError(null);


    try {

      const formData =
        new FormData();


      formData.append(
        "file",
        selectedImage.file
      );


      const response =
        await fetch(
          "http://127.0.0.1:8000/analyze",
          {
            method: "POST",
            body: formData,
          }
        );


      if (!response.ok) {

        let message =
          "Analysis request failed.";


        try {

          const errorData =
            await response.json();


          if (errorData.detail) {

            message =
              errorData.detail;

          }

        } catch {

          // Keep default error message

        }


        throw new Error(message);

      }


      const data =
        await response.json();


      setResult(data);

      setGradcamImage(
        data.gradcam_image || null
      );

    } catch (err) {

      console.error(err);

      setError(
        err.message ||
        "Could not analyze the image. Make sure FastAPI is running."
      );

    } finally {

      setLoading(false);

    }

  };


  // =========================================
  // Result status text
  // =========================================

  const getStatusText = () => {

    if (!result) {
      return "";
    }


    if (
      result.confidence_status === "healthy"
    ) {

      return "✓ Healthy";

    }


    if (
      result.confidence_status === "low"
    ) {

      return "⚠ Low Confidence";

    }


    return "✓ High Confidence";

  };


  // =========================================
  // Render
  // =========================================

  return (

    <div className="app">


      {/* =====================================
          Header
          ===================================== */}

      <header className="header">

        <div>

          <div className="logo">
            🌱 Plant Disease Detector
          </div>


          <div className="header-subtitle">
            AI-powered plant health analysis
          </div>

        </div>


        <div className="model-badge">
          EfficientNet-B0
        </div>

      </header>


      <main className="main-content">


        {/* ===================================
            Hero
            =================================== */}

        <section className="hero">

          <div className="hero-badge">
            🌿 AI Plant Analysis
          </div>


          <h1>
            Detect Plant Diseases
          </h1>


          <p>
            Upload a leaf image and let our AI
            identify possible plant diseases.
          </p>

        </section>


        {/* ===================================
            Main workspace
            =================================== */}

        <section className="workspace">


          {/* =================================
              Image panel
              ================================= */}

          <div className="image-panel">


            <div className="panel-header">

              <div>

                <h2>
                  Leaf Image
                </h2>


                <p>
                  Upload an image to begin analysis
                </p>

              </div>


              <div className="step-number">
                01
              </div>

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
                isDragging
                  ? "dragging"
                  : ""
              } ${
                loading
                  ? "disabled"
                  : ""
              } ${
                selectedImage
                  ? "has-image"
                  : ""
              }`}

              onClick={
                selectedImage
                  ? undefined
                  : openFilePicker
              }

              onDragOver={handleDragOver}

              onDragLeave={handleDragLeave}

              onDrop={handleDrop}

              role={
                selectedImage
                  ? undefined
                  : "button"
              }

              tabIndex={
                selectedImage
                  ? -1
                  : 0
              }

              onKeyDown={(event) => {

                if (
                  !selectedImage &&
                  (
                    event.key === "Enter" ||
                    event.key === " "
                  )
                ) {

                  openFilePicker();

                }

              }}
            >


              {!selectedImage && (

                <>

                  <div className="upload-icon">

                    {isDragging
                      ? "📥"
                      : "🍃"
                    }

                  </div>


                  <h3>

                    {isDragging
                      ? "Drop your image here"
                      : "Drag & drop a leaf image"
                    }

                  </h3>


                  <p>
                    or click to browse your files
                  </p>


                  <span className="upload-button">
                    Choose Image
                  </span>


                  <span className="upload-formats">
                    JPG • PNG • WEBP • Max 10 MB
                  </span>

                </>

              )}


              {selectedImage && (

                <img
                  src={selectedImage.preview}
                  alt="Selected plant leaf"
                  className="main-preview-image"
                />

              )}

            </div>


            {/* Selected file */}

            {selectedImage && (

              <div className="selected-file">

                <span>
                  📄
                </span>


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
                  🖼️ Change Image
                </button>


                <button
                  type="button"
                  className={`predict-button ${
                    result
                      ? "analyzed"
                      : ""
                  }`}
                  onClick={handlePredict}
                  disabled={
                    loading ||
                    Boolean(result)
                  }
                >

                  {loading
                    ? "⏳ Analyzing..."
                    : result
                      ? "✓ Analysis Complete"
                      : "🔍 Analyze Leaf"
                  }

                </button>

              </div>

            )}


            {/* Small hint after successful analysis */}

            {result && !loading && (

              <div className="analysis-complete-note">

                ✓ Analysis completed successfully.
                Use <strong>New Analysis</strong> to test
                another leaf.

              </div>

            )}

          </div>


          {/* =================================
              Result panel
              ================================= */}

          <div className="result-panel">


            {/* Empty */}

            {!result && !loading && (

              <div className="empty-result">

                <div className="empty-icon">
                  🧠
                </div>


                <h2>
                  Analysis Result
                </h2>


                <p>
                  Your prediction will appear here
                  after you analyze a leaf image.
                </p>

              </div>

            )}


            {/* Loading */}

            {loading && (

              <div className="loading-result">

                <div className="loading-spinner">
                  ⟳
                </div>


                <h2>
                  Analyzing your leaf
                </h2>


                <p>
                  EfficientNet-B0 is examining the
                  image and generating the prediction.
                </p>


                <div className="loading-progress">

                  <div className="loading-progress-fill" />

                </div>


                <span className="loading-caption">
                  Running model inference + Grad-CAM
                </span>

              </div>

            )}


            {/* Result */}

            {result && (

              <div className="result-content">


                <div className="panel-header">

                  <div>

                    <h2>
                      Analysis Result
                    </h2>


                    <p>
                      AI-assisted plant assessment
                    </p>

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


                {/* Plant + condition */}

                <div className="prediction-summary">


                  <div className="prediction-main">

                    <span className="label">
                      Plant
                    </span>


                    <strong>
                      {result.plant}
                    </strong>

                  </div>


                  <div className="prediction-main">

                    <span className="label">

                      {result.is_healthy
                        ? "Health Status"
                        : "Detected Condition"
                      }

                    </span>


                    <strong>

                      {result.is_healthy
                        ? "Healthy"
                        : result.disease
                      }

                    </strong>

                  </div>

                </div>


                {/* Confidence */}

                <div className="confidence-box">

                  <div className="confidence-header">

                    <span>
                      Model Confidence
                    </span>


                    <strong>
                      {Number(
                        result.confidence
                      ).toFixed(2)}%
                    </strong>

                  </div>


                  <div className="confidence-bar">

                    <div
                      className="confidence-fill"
                      style={{
                        width: `${Math.min(
                          Number(
                            result.confidence
                          ),
                          100
                        )}%`,
                      }}
                    />

                  </div>

                </div>


                {/* Warning */}

                {result.confidence_warning && (

                  <div className="confidence-warning">

                    <span>
                      ⚠️
                    </span>


                    <p>
                      {result.confidence_warning}
                    </p>

                  </div>

                )}


                {/* Healthy message */}

                {result.is_healthy && (

                  <div className="healthy-message">

                    <span>
                      🌿
                    </span>


                    <div>

                      <strong>
                        No disease detected
                      </strong>


                      <p>
                        The model classified this
                        leaf as healthy.
                      </p>

                    </div>

                  </div>

                )}


                {/* Top predictions */}

                <div className="top-predictions">

                  <div className="subsection-header">

                    <h3>
                      Top Predictions
                    </h3>


                    <span>
                      Model ranking
                    </span>

                  </div>


                  {result.top_3.map(
                    (prediction, index) => (

                      <div
                        className={`prediction-item ${
                          index === 0
                            ? "top-result"
                            : ""
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
                  ↺ New Analysis
                </button>

              </div>

            )}

          </div>

        </section>


        {/* =====================================
            Error message
            ===================================== */}

        {error && (

          <div className="error-message">
            ⚠️ {error}
          </div>

        )}


        {/* =====================================
            Disease information
            ===================================== */}

        {result && (

          <section className="disease-info-section">


            <div className="section-heading">

              <div>

                <h2>

                  {result.is_healthy
                    ? "🌿 Plant Health Information"
                    : "🌿 About the Disease"
                  }

                </h2>


                <p>
                  Information related to the
                  detected plant condition.
                </p>

              </div>


              <div className="step-number">
                03
              </div>

            </div>


            {/* Description */}

            <div className="description-card">

              <div className="description-label">

                {result.is_healthy
                  ? "HEALTH ASSESSMENT"
                  : "CONDITION OVERVIEW"
                }

              </div>


              <h3>
                {result.disease}
              </h3>


              <p>
                {result.description}
              </p>

            </div>


            {/* Information cards */}

            <div className="disease-info-grid">


              {/* Symptoms / indicators */}

              <div className="disease-info-card">

                <div className="disease-card-top">

                  <div className="disease-card-icon">
                    🔎
                  </div>

                </div>


                <h3>

                  {result.is_healthy
                    ? "Healthy Indicators"
                    : "Common Symptoms"
                  }

                </h3>


                <ul>

                  {result.symptoms.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              {/* Management */}

              <div className="disease-info-card">

                <div className="disease-card-top">

                  <div className="disease-card-icon">
                    🛠️
                  </div>

                </div>


                <h3>
                  Management
                </h3>


                <ul>

                  {result.management.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              {/* Prevention */}

              <div className="disease-info-card">

                <div className="disease-card-top">

                  <div className="disease-card-icon">
                    🛡️
                  </div>

                </div>


                <h3>
                  Prevention
                </h3>


                <ul>

                  {result.prevention.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>

            </div>


            {/* Disclaimer */}

            <div className="disclaimer">

              <span>
                ⚠️
              </span>


              <span>

                This result is an AI-assisted prediction,
                not a definitive plant disease diagnosis.
                Confirm important decisions with a qualified
                agricultural or plant-disease professional.

              </span>

            </div>

          </section>

        )}


        {/* =====================================
            Grad-CAM explanation
            ===================================== */}

        {gradcamImage && (

          <section className="gradcam-section">


            <div className="panel-header">

              <div>

                <div className="section-mini-label">
                  EXPLAINABLE AI
                </div>


                <h2>
                  🔥 Grad-CAM Explanation
                </h2>


                <p>
                  See which regions of the leaf
                  influenced the model's prediction.
                </p>

              </div>


              <div className="step-number">
                04
              </div>

            </div>


            <div className="gradcam-content">


              {/* Image */}

              <div className="gradcam-image-wrap">

                <img
                  src={gradcamImage}
                  alt="Grad-CAM explanation showing areas that influenced the prediction"
                  className="gradcam-image"
                />

              </div>


              {/* Explanation */}

              <div className="gradcam-info">


                <div className="gradcam-explanation-box">

                  <div className="explanation-icon">
                    🧠
                  </div>


                  <div>

                    <h3>
                      How the AI looked at the leaf
                    </h3>


                    <p>
                      Grad-CAM highlights the image
                      regions that had the strongest
                      influence on the model's decision.
                    </p>

                  </div>

                </div>


                <div className="gradcam-points">

                  <div className="gradcam-point">

                    <span className="point-icon">
                      01
                    </span>


                    <div>

                      <strong>
                        Prediction
                      </strong>


                      <p>
                        The model identifies the most
                        likely plant condition.
                      </p>

                    </div>

                  </div>


                  <div className="gradcam-point">

                    <span className="point-icon">
                      02
                    </span>


                    <div>

                      <strong>
                        Attention
                      </strong>


                      <p>
                        The heatmap shows regions that
                        contributed to that prediction.
                      </p>

                    </div>

                  </div>


                  <div className="gradcam-point">

                    <span className="point-icon">
                      03
                    </span>


                    <div>

                      <strong>
                        Interpretation
                      </strong>


                      <p>
                        Warmer areas generally indicate
                        stronger model influence.
                      </p>

                    </div>

                  </div>

                </div>


                <div className="gradcam-note">

                  <span>
                    💡
                  </span>


                  <span>
                    Grad-CAM is an explanation aid,
                    not proof that a particular region
                    contains the disease.
                  </span>

                </div>

              </div>

            </div>

          </section>

        )}


        {/* =====================================
            Initial project information
            ===================================== */}

        {!selectedImage && (

          <section className="info-section">


            <div className="info-card">

              <div className="info-number">
                55
              </div>


              <div>

                <h3>
                  Disease Classes
                </h3>


                <p>
                  Recognizes 55 plant health
                  conditions.
                </p>

              </div>

            </div>


            <div className="info-card">

              <div className="info-number">
                95.58%
              </div>


              <div>

                <h3>
                  Test Accuracy
                </h3>


                <p>
                  Performance on our untouched
                  test dataset.
                </p>

              </div>

            </div>


            <div className="info-card">

              <div className="info-number">
                🔥
              </div>


              <div>

                <h3>
                  Explainable AI
                </h3>


                <p>
                  Grad-CAM provides visual
                  explanations.
                </p>

              </div>

            </div>

          </section>

        )}

      </main>


      {/* =====================================
          Footer
          ===================================== */}

      <footer className="footer">

        Plant Disease Detector

      </footer>

      <ChatWidget plantResult={result} />

    </div>

  );
}


export default App;