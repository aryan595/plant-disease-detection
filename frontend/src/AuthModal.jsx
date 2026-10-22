import { useState, useEffect, useRef } from "react";
import { getAuthText } from "./authLocalization";
import "./AuthModal.css";

// Official Google "G" multicolor SVG icon
export function GoogleIcon({ className = "google-svg-icon", size = 20 }) {
  return (
    <svg className={className} width={size} height={size} viewBox="0 0 24 24" aria-hidden="true">
      <path
        fill="#4285F4"
        d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"
      />
      <path
        fill="#34A853"
        d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"
      />
      <path
        fill="#FBBC05"
        d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"
      />
      <path
        fill="#EA4335"
        d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"
      />
    </svg>
  );
}

// Safely decodes Google JWT credential token
function parseJwt(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map((c) => "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2))
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch (err) {
    console.warn("Failed to parse JWT payload:", err);
    return null;
  }
}

export default function AuthModal({
  isOpen,
  onClose,
  initialMode = "signin",
  onLoginSuccess,
  language = "en",
  currentDistrict = "Pune",
  districts = [],
}) {
  const t = getAuthText(language);
  const [mode, setMode] = useState(initialMode); // "signin" | "signup"
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [fullName, setFullName] = useState("");
  const [primaryCrop, setPrimaryCrop] = useState("Tomato");
  const [userDistrict, setUserDistrict] = useState(currentDistrict);
  const [rememberMe, setRememberMe] = useState(true);
  const [loading, setLoading] = useState(false);
  const [errorMessage, setErrorMessage] = useState("");
  const [showDemoChooser, setShowDemoChooser] = useState(false);
  const [customGoogleEmail, setCustomGoogleEmail] = useState("");
  const [customGoogleName, setCustomGoogleName] = useState("");

  const modalRef = useRef(null);
  const googleBtnRef = useRef(null);

  // Sync mode if initialMode changes
  useEffect(() => {
    setMode(initialMode);
    setErrorMessage("");
    setShowDemoChooser(false);
  }, [initialMode, isOpen]);

  // Sync district if currentDistrict changes
  useEffect(() => {
    if (currentDistrict) setUserDistrict(currentDistrict);
  }, [currentDistrict]);

  // Escape key listener for accessible dismissal
  useEffect(() => {
    if (!isOpen) return;

    const handleKeyDown = (e) => {
      if (e.key === "Escape") {
        onClose();
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isOpen, onClose]);

  // Google Identity Services (GIS) integration
  useEffect(() => {
    if (!isOpen) return;

    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

    // Check if Google GIS library is ready and a Client ID is provided
    if (googleClientId && window.google?.accounts?.id && googleBtnRef.current) {
      try {
        window.google.accounts.id.initialize({
          client_id: googleClientId,
          callback: (response) => {
            if (response.credential) {
              const decoded = parseJwt(response.credential);
              if (decoded) {
                const googleUser = {
                  id: decoded.sub || `google_${Date.now()}`,
                  name: decoded.name || "Google Farmer",
                  email: decoded.email || "farmer@gmail.com",
                  picture: decoded.picture || null,
                  provider: "google",
                  district: userDistrict,
                  primaryCrop: primaryCrop,
                  verified: true,
                  token: response.credential,
                  createdAt: new Date().toISOString(),
                };
                saveAndComplete(googleUser);
              }
            }
          },
          auto_select: false,
        });

        // Render official button into target
        window.google.accounts.id.renderButton(googleBtnRef.current, {
          theme: "filled_blue",
          size: "large",
          width: 320,
          text: mode === "signup" ? "signup_with" : "signin_with",
          shape: "pill",
        });
      } catch (err) {
        console.warn("Google GIS initialization error:", err);
      }
    }
  }, [isOpen, mode, userDistrict, primaryCrop]);

  const saveAndComplete = (user) => {
    try {
      localStorage.setItem("agrisense_user", JSON.stringify(user));
    } catch (e) {
      console.warn("Could not save user to localStorage:", e);
    }
    setLoading(false);
    onLoginSuccess(user);
    onClose();
  };

  // Trigger Google Login
  const handleGoogleClick = () => {
    setErrorMessage("");
    const googleClientId = import.meta.env.VITE_GOOGLE_CLIENT_ID;

    // If real Google Client ID is configured and GIS is available, trigger One Tap / popup
    if (googleClientId && window.google?.accounts?.id) {
      try {
        window.google.accounts.id.prompt();
        return;
      } catch (err) {
        console.warn("Google Prompt failed, falling back to account chooser:", err);
      }
    }

    // Otherwise show the Google Account Selector (works instantly in dev / local environment)
    setShowDemoChooser(true);
  };

  // Instant sign in as Google Demo Farmer
  const handleDemoGoogleSignIn = (farmerType = "default") => {
    setLoading(true);
    setTimeout(() => {
      const demoUser = {
        id: "google_109283746501928374650",
        name: farmerType === "custom" && customGoogleName ? customGoogleName : "Ramesh Patil",
        email:
          farmerType === "custom" && customGoogleEmail
            ? customGoogleEmail
            : "ramesh.patil.farmer@gmail.com",
        picture: "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80",
        provider: "google",
        district: userDistrict || "Pune",
        primaryCrop: primaryCrop || "Tomato",
        verified: true,
        role: "farmer",
        createdAt: new Date().toISOString(),
      };
      saveAndComplete(demoUser);
    }, 450);
  };

  // Handle standard email form submit
  const handleEmailSubmit = (e) => {
    e.preventDefault();
    setErrorMessage("");

    if (!email.trim() || !email.includes("@")) {
      setErrorMessage("Please enter a valid email address.");
      return;
    }

    if (!password || password.length < 6) {
      setErrorMessage("Password must be at least 6 characters.");
      return;
    }

    if (mode === "signup" && !fullName.trim()) {
      setErrorMessage("Please enter your full name.");
      return;
    }

    setLoading(true);

    setTimeout(() => {
      const user = {
        id: `user_${Date.now()}`,
        name: mode === "signup" ? fullName.trim() : email.split("@")[0].replace(/[._]/g, " "),
        email: email.trim(),
        picture: null,
        provider: "email",
        district: userDistrict,
        primaryCrop: primaryCrop,
        verified: false,
        role: "farmer",
        createdAt: new Date().toISOString(),
      };
      saveAndComplete(user);
    }, 500);
  };

  if (!isOpen) return null;

  return (
    <div
      className="auth-modal-backdrop"
      onClick={(e) => {
        if (e.target === e.currentTarget) onClose();
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby="auth-modal-title"
    >
      <div className="auth-modal-card" ref={modalRef}>
        {/* Close Button */}
        <button
          type="button"
          className="auth-close-btn"
          onClick={onClose}
          aria-label={t.close}
          title={t.close}
        >
          ✕
        </button>

        {/* Left Side: AgriSense Brand Showcase */}
        <div className="auth-brand-panel">
          <div className="auth-brand-header">
            <span className="auth-sprout-badge">🌱 AgriSense PRO</span>
            <h2>{t.heroTitle}</h2>
            <p className="auth-brand-tagline">{t.welcomeSubtitle}</p>
          </div>

          <div className="auth-benefits-list">
            <div className="auth-benefit-item">
              <span className="benefit-check">✓</span>
              <span>{t.benefit1}</span>
            </div>
            <div className="auth-benefit-item">
              <span className="benefit-check">✓</span>
              <span>{t.benefit2}</span>
            </div>
            <div className="auth-benefit-item">
              <span className="benefit-check">✓</span>
              <span>{t.benefit3}</span>
            </div>
            <div className="auth-benefit-item">
              <span className="benefit-check">✓</span>
              <span>{t.benefit4}</span>
            </div>
          </div>

          <div className="auth-farm-pill">
            <span className="farm-pill-dot">●</span>
            <span>Maharashtra Agronomy & PMFBY Standard Aligned</span>
          </div>

          <div className="auth-brand-footer">
            <small>{t.secureNote}</small>
          </div>
        </div>

        {/* Right Side: Auth Form */}
        <div className="auth-form-panel">
          {/* Top Mode Tabs */}
          <div className="auth-tabs-wrapper" role="tablist">
            <button
              type="button"
              role="tab"
              aria-selected={mode === "signin"}
              className={`auth-tab-btn ${mode === "signin" ? "active" : ""}`}
              onClick={() => {
                setMode("signin");
                setErrorMessage("");
                setShowDemoChooser(false);
              }}
            >
              {t.signIn}
            </button>
            <button
              type="button"
              role="tab"
              aria-selected={mode === "signup"}
              className={`auth-tab-btn ${mode === "signup" ? "active" : ""}`}
              onClick={() => {
                setMode("signup");
                setErrorMessage("");
                setShowDemoChooser(false);
              }}
            >
              {t.createAccount}
            </button>
          </div>

          <div className="auth-heading-group">
            <h3 id="auth-modal-title">
              {mode === "signup" ? t.createAccount : t.signIn}
            </h3>
            <p className="auth-subtext">
              {mode === "signup"
                ? "Join thousands of farmers using AI plant disease protection"
                : "Sign in with Google to access your crop diagnosis history"}
            </p>
          </div>

          {errorMessage && (
            <div className="auth-error-banner" role="alert">
              <span>⚠</span>
              <span>{errorMessage}</span>
            </div>
          )}

          {/* Primary Action: Google Sign In / Sign Up */}
          <div className="google-auth-cluster">
            {/* GIS Container (if real Google Client ID provided) */}
            <div id="google-gis-btn-slot" ref={googleBtnRef} className="google-gis-container" />

            {/* Always visible responsive Google Button */}
            <button
              type="button"
              className="google-auth-button"
              onClick={handleGoogleClick}
              disabled={loading}
            >
              <GoogleIcon size={20} />
              <span>
                {mode === "signup" ? t.signUpWithGoogle : t.continueWithGoogle}
              </span>
            </button>
          </div>

          {/* Google Account Selector Dialog (Instant Demo or Custom Google ID) */}
          {showDemoChooser && (
            <div className="google-demo-picker-card">
              <div className="demo-picker-header">
                <GoogleIcon size={18} />
                <strong>{t.demoAccountTitle}</strong>
              </div>
              <p className="demo-picker-hint">
                Select an account to sign in immediately with Google credentials:
              </p>

              <button
                type="button"
                className="demo-account-option-btn primary-demo"
                onClick={() => handleDemoGoogleSignIn("default")}
                disabled={loading}
              >
                <div className="demo-avatar-circle">RP</div>
                <div className="demo-account-info">
                  <strong>Ramesh Patil</strong>
                  <span>ramesh.patil.farmer@gmail.com</span>
                </div>
                <span className="demo-select-arrow">→</span>
              </button>

              <div className="custom-google-box">
                <label className="auth-label">{t.customGoogleTitle}</label>
                <div className="custom-google-inputs">
                  <input
                    type="text"
                    className="auth-input"
                    placeholder="Your Name (e.g. Aryan)"
                    value={customGoogleName}
                    onChange={(e) => setCustomGoogleName(e.target.value)}
                  />
                  <input
                    type="email"
                    className="auth-input"
                    placeholder="your.email@gmail.com"
                    value={customGoogleEmail}
                    onChange={(e) => setCustomGoogleEmail(e.target.value)}
                  />
                  <button
                    type="button"
                    className="custom-google-submit-btn"
                    onClick={() => handleDemoGoogleSignIn("custom")}
                    disabled={!customGoogleEmail.includes("@")}
                  >
                    Sign In with this Google Account
                  </button>
                </div>
              </div>

              <div className="google-setup-tip">
                💡 <em>Tip:</em> To use official Google Cloud OAuth popup, add your{" "}
                <code>VITE_GOOGLE_CLIENT_ID</code> in <code>frontend/.env</code>.
              </div>
            </div>
          )}

          {/* Divider */}
          <div className="auth-divider">
            <span>{t.orWithEmail}</span>
          </div>

          {/* Email / Password Form */}
          <form className="auth-email-form" onSubmit={handleEmailSubmit}>
            {mode === "signup" && (
              <div className="auth-field">
                <label className="auth-label" htmlFor="auth-fullname">
                  {t.fullName}
                </label>
                <input
                  id="auth-fullname"
                  type="text"
                  className="auth-input"
                  placeholder={t.fullNamePlaceholder}
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                  required
                />
              </div>
            )}

            <div className="auth-field">
              <label className="auth-label" htmlFor="auth-email">
                {t.email}
              </label>
              <input
                id="auth-email"
                type="email"
                className="auth-input"
                placeholder={t.emailPlaceholder}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                autoComplete="email"
                required
              />
            </div>

            <div className="auth-field">
              <div className="auth-label-row">
                <label className="auth-label" htmlFor="auth-password">
                  {t.password}
                </label>
                {mode === "signin" && (
                  <button
                    type="button"
                    className="auth-forgot-link"
                    onClick={() => alert(t.forgotPasswordNotice)}
                  >
                    {t.forgotPassword}
                  </button>
                )}
              </div>
              <div className="password-input-wrap">
                <input
                  id="auth-password"
                  type={showPassword ? "text" : "password"}
                  className="auth-input"
                  placeholder={t.passwordPlaceholder}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  autoComplete={mode === "signup" ? "new-password" : "current-password"}
                  required
                />
                <button
                  type="button"
                  className="password-toggle-btn"
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label="Toggle password visibility"
                >
                  {showPassword ? "👁" : "👁‍🗨"}
                </button>
              </div>
            </div>

            {mode === "signup" && (
              <div className="auth-fields-row">
                <div className="auth-field">
                  <label className="auth-label">{t.primaryCrop}</label>
                  <select
                    className="auth-select"
                    value={primaryCrop}
                    onChange={(e) => setPrimaryCrop(e.target.value)}
                  >
                    <option value="Tomato">Tomato (टमाटर / टोमॅटो)</option>
                    <option value="Potato">Potato (आलू / बटाटा)</option>
                    <option value="Grape">Grape (अंगूर / द्राक्षे)</option>
                    <option value="Soybean">Soybean (सोयाबीन)</option>
                    <option value="Cotton">Cotton (कपास / कापूस)</option>
                    <option value="Sugarcane">Sugarcane (गन्ना / ऊस)</option>
                    <option value="Other">Other Crops (इतर)</option>
                  </select>
                </div>

                <div className="auth-field">
                  <label className="auth-label">{t.district}</label>
                  <select
                    className="auth-select"
                    value={userDistrict}
                    onChange={(e) => setUserDistrict(e.target.value)}
                  >
                    {districts && districts.length > 0 ? (
                      districts.map((d) => (
                        <option key={d.id || d.name} value={d.name}>
                          {d.name}
                        </option>
                      ))
                    ) : (
                      <>
                        <option value="Pune">Pune (पुणे)</option>
                        <option value="Nashik">Nashik (नाशिक)</option>
                        <option value="Kolhapur">Kolhapur (कोल्हापूर)</option>
                        <option value="Satara">Satara (सातारा)</option>
                        <option value="Nagpur">Nagpur (नागपूर)</option>
                      </>
                    )}
                  </select>
                </div>
              </div>
            )}

            <div className="auth-remember-row">
              <label className="checkbox-label">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(e) => setRememberMe(e.target.checked)}
                />
                <span>{t.rememberMe}</span>
              </label>
            </div>

            <button type="submit" className="auth-submit-btn" disabled={loading}>
              {loading ? "Processing..." : mode === "signup" ? t.submitSignUp : t.submitSignIn}
            </button>
          </form>

          {/* Toggle between sign in and sign up */}
          <div className="auth-footer-toggle">
            {mode === "signin" ? (
              <p>
                {t.newToAgriSense.split("?")[0]}?{" "}
                <button
                  type="button"
                  className="auth-switch-link"
                  onClick={() => {
                    setMode("signup");
                    setErrorMessage("");
                    setShowDemoChooser(false);
                  }}
                >
                  {t.createAccount}
                </button>
              </p>
            ) : (
              <p>
                {t.alreadyHaveAccount.split("?")[0]}?{" "}
                <button
                  type="button"
                  className="auth-switch-link"
                  onClick={() => {
                    setMode("signin");
                    setErrorMessage("");
                    setShowDemoChooser(false);
                  }}
                >
                  {t.signIn}
                </button>
              </p>
            )}
          </div>

          <div className="auth-back-link-wrap">
            <button type="button" className="auth-back-btn" onClick={onClose}>
              {t.backToDashboard}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
