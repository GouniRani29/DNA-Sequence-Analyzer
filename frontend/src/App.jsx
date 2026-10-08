import { useState } from "react";
import "./App.css";

import DNAAnalyzer from "./components/DNAAnalyzer";
import Login from "./components/Login";
import Register from "./components/Register";

function App() {
  const [showLogin, setShowLogin] = useState(false);
  const [showRegister, setShowRegister] = useState(false);
  const [user, setUser] = useState(null);

  // Login successful
  const handleLogin = (data) => {
    setUser(data);
    setShowLogin(false);
    setShowRegister(false);
  };

  // Logout
  const handleLogout = () => {
    localStorage.removeItem("userId");
    localStorage.removeItem("username");

    setUser(null);
  };

  // Go to home
  const goHome = () => {
    setShowLogin(false);
    setShowRegister(false);

    setTimeout(() => {
      document
        .getElementById("home")
        ?.scrollIntoView({ behavior: "smooth" });
    }, 100);
  };

  // ================= LOGIN PAGE =================
  if (showLogin) {
    return (
      <Login
        onLogin={handleLogin}
        onSignUp={() => {
          setShowLogin(false);
          setShowRegister(true);
        }}
        onBack={goHome}
      />
    );
  }

  // ================= REGISTER PAGE =================
  if (showRegister) {
    return (
      <Register
        onRegister={() => {
          setShowRegister(false);
          setShowLogin(true);
        }}
        onBackToLogin={() => {
          setShowRegister(false);
          setShowLogin(true);
        }}
        onBack={goHome}
      />
    );
  }

  return (
    <div className="app">

      {/* ================= NAVBAR ================= */}

      <nav className="navbar">

        <div className="logo">
          <span className="dna-icon">🧬</span>

          <span>
             DNA <b>Analyzer</b>
          </span>
        </div>

        <div className="nav-links">

          <a href="#home">Home</a>

          <a href="#about">About</a>

          <a href="#how">How It Works</a>

          <a href="#features">Features</a>

          <a href="#contact">Contact</a>

        </div>

        {!user ? (

          <button
            className="login-nav"
            onClick={() => setShowLogin(true)}
          >
            👤 Login
          </button>

        ) : (

          <button
            className="login-nav"
            onClick={handleLogout}
          >
            👤 Logout
          </button>

        )}

      </nav>


      {/* ================= HERO ================= */}

      <section className="hero" id="home">

        <div className="hero-content">

          <div className="badge">
            ✨ DNA Sequence Analyser
          </div>

          <h1>
            Unlock the Power of
            <br />
            DNA with <span>DeepLearning</span>
          </h1>

          <p>
            Upload your DNA sequence and get intelligent predictions
            using advanced Deep Learning and Transformer technology.
          </p>

          <div className="hero-buttons">

            <button
              className="primary-btn"
              onClick={() => {

                if (user) {

                  document
                    .getElementById("analyzer")
                    ?.scrollIntoView({
                      behavior: "smooth"
                    });

                } else {

                  setShowLogin(true);

                }

              }}
            >
              🚀 Get Started →
            </button>

            <button
              className="secondary-btn"
              onClick={() => {

                document
                  .getElementById("how")
                  ?.scrollIntoView({
                    behavior: "smooth"
                  });

              }}
            >
              ▶ How It Works
            </button>

          </div>


          {/* STATS */}

          <div className="stats">

            <div className="stat-card">
              <strong>4</strong>
              <small>Supported Formats</small>
            </div>

            <div className="stat-card">
              <strong>99.2%</strong>
              <small> Accuracy</small>
            </div>

            <div className="stat-card">
              <strong>2.4s</strong>
              <small>Avg. Analysis Time</small>
            </div>

            <div className="stat-card">
              <strong>100%</strong>
              <small>Secure & Private</small>
            </div>

          </div>

        </div>


        {/* DNA VISUAL */}

        <div className="dna-section">

          <div className="dna-glow"></div>

          <div className="dna">
            🧬
          </div>

          <div className="floating-card sequence-card">

            <small>
              ATGC Sequence
            </small>

            <p>
              ATGCGTACGTAGCTAGCT
            </p>

            <div className="graph">
              〰〰〰〰〰
            </div>

          </div>

          <div className="floating-card prediction-card">

            <small>
              DNA Prediction
            </small>

            <h3>
              Class 3
            </h3>

            <p>
              Confidence  <b>53.23%</b>
            </p>

          </div>

          <div className="floating-card analysis-card">

            <small>
              Analysis ID
            </small>

            <h3>
              #8
            </h3>

          </div>

          <div className="floating-card model-card">

            <small>
              Model
            </small>

            <h3>
              Transformer
            </h3>

          </div>

        </div>

      </section>


      {/* ================= ABOUT ================= */}

      <section className="info-section" id="about">

        <div className="section-label">
          🧬 ABOUT
        </div>

        <h2>
          Intelligent DNA Analysis
        </h2>

        <p>
           DNA Analyzer is designed to analyze DNA sequences using
          modern Deep Learning and Transformer technology.
        </p>

      </section>


      {/* ================= HOW IT WORKS ================= */}

      <section className="info-section" id="how">

        <div className="section-label">
          ⚡ HOW IT WORKS
        </div>

        <h2>
          Simple Three-Step Process
        </h2>

        <div className="steps">

          <div className="step-card">
            <span>01</span>
            <h3>Upload DNA</h3>
            <p>
              Upload your DNA sequence file or enter the sequence manually.
            </p>
          </div>

          <div className="step-card">
            <span>02</span>
            <h3>DNA Analysis</h3>
            <p>
              Our Deep Learning Transformer analyzes your DNA sequence.
            </p>
          </div>

          <div className="step-card">
            <span>03</span>
            <h3>View Prediction</h3>
            <p>
              Get the predicted class and confidence score.
            </p>
          </div>

        </div>

      </section>


      {/* ================= FEATURES ================= */}

      <section
        className="features"
        id="features"
      >

        <div className="section-label">
          ✨ FEATURES
        </div>

        <h2>
          Powerful DNA Analysis
        </h2>

        <p className="section-description">
          Everything you need for advanced DNA sequence analysis
        </p>


        <div className="feature-grid">

          <div className="feature-card">

            <div className="feature-icon purple">
              📁
            </div>

            <div>

              <h3>
                Upload DNA Files
              </h3>

              <p>
                Upload .txt, .fasta, .fa or .fna DNA files with ease.
              </p>

            </div>

          </div>


          <div className="feature-card">

            <div className="feature-icon green">
              🧬
            </div>

            <div>

              <h3>
                DNA Prediction
              </h3>

              <p>
                Analyze sequences using Deep Learning Transformer.
              </p>

            </div>

          </div>


          <div className="feature-card">

            <div className="feature-icon orange">
              📊
            </div>

            <div>

              <h3>
                Confidence Score
              </h3>

              <p>
                Get detailed confidence scores for every prediction.
              </p>

            </div>

          </div>


          <div className="feature-card">

            <div className="feature-icon blue">
              🛡️
            </div>

            <div>

              <h3>
                Secure & Private
              </h3>

              <p>
                Your DNA data is protected and securely processed.
              </p>

            </div>

          </div>

        </div>


        {/* CTA */}

        <div className="cta">

          <div>

            <h2>
              Ready to analyze your DNA?
            </h2>

            <p>
              Start exploring your DNA sequences.
            </p>

          </div>

          <div className="cta-buttons">

            <button
              className="primary-btn"
              onClick={() => {

                if (user) {

                  document
                    .getElementById("analyzer")
                    ?.scrollIntoView({
                      behavior: "smooth"
                    });

                } else {

                  setShowLogin(true);

                }

              }}
            >
              Get Started Now →
            </button>

            {!user && (

              <button
                className="cta-login"
                onClick={() => setShowLogin(true)}
              >
                👤 Login
              </button>

            )}

          </div>

        </div>

      </section>


      {/* ================= ANALYZER ================= */}

      <section
        className="analyzer-section"
        id="analyzer"
      >

        {user ? (

          <DNAAnalyzer />

        ) : (

          <div className="login-required">

            <div className="lock-icon">
              🔐
            </div>

            <h2>
              Login Required
            </h2>

            <p>
              Please login to start analyzing DNA sequences.
            </p>

            <button
              className="primary-btn"
              onClick={() => setShowLogin(true)}
            >
              Login to Continue →
            </button>

          </div>

        )}

      </section>


      {/* ================= CONTACT ================= */}

      <section
        className="contact-section"
        id="contact"
      >

        <div className="section-label">
          📩 CONTACT
        </div>

        <h2>
          Get in Touch
        </h2>

        <p>
          Have questions about  DNA Analyzer? We'd love to hear from you.
        </p>

      </section>


      {/* ================= FOOTER ================= */}

      <footer className="footer">

        <div>
          🧬 <strong> DNA Analyzer</strong>
        </div>

        <p>
           DNA sequence analyser Using DL.
        </p>

      </footer>

    </div>
  );
}

export default App;