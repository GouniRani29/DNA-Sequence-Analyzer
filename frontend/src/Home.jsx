
import "./App.css";

function Home({ onLogin, onGetStarted }) {
    return (
        <div className="home-page">

            {/* NAVBAR */}
            <nav className="navbar">

                <div className="logo">
                    🧬 DNA Analyzer
                </div>

                <div className="nav-links">
                    <button onClick={onGetStarted}>
                        Home
                    </button>

                    <button>
                        About
                    </button>

                    <button>
                        How It Works
                    </button>

                    <button
                        className="nav-login"
                        onClick={onLogin}
                    >
                        Login
                    </button>
                </div>

            </nav>


            {/* HERO SECTION */}
            <section className="hero">

                <div className="hero-content">

                    <h1>
                        Transformer-Based
                        <br />
                        DNA Sequence Analysis
                    </h1>

                    <p>
                        Analyze DNA sequences using
                        advanced Deep Learning and
                        Transformer technology.
                    </p>

                    <div className="hero-buttons">

                        <button
                            className="get-started"
                            onClick={onGetStarted}
                        >
                            Get Started →
                        </button>

                        <button
                            className="login-button"
                            onClick={onLogin}
                        >
                            Login
                        </button>

                    </div>

                </div>


                {/* DNA VISUAL */}
                <div className="hero-visual">

                    <div className="dna-card">

                        <div className="dna-icon">
                            🧬
                        </div>

                        <h2>
                            DNA Analyzer
                        </h2>

                        <p>
                            Upload your DNA file and
                            get a sequence prediction.
                        </p>

                        <div className="feature">
                            ✓ Multiple DNA file formats
                        </div>

                        <div className="feature">
                            ✓ Transformer-based prediction
                        </div>

                        <div className="feature">
                            ✓ Confidence score
                        </div>

                    </div>

                </div>

            </section>


            {/* FEATURES */}
            <section className="features">

                <h2>
                    Powerful DNA Analysis
                </h2>

                <div className="feature-container">

                    <div className="feature-box">
                        <div>📁</div>
                        <h3>Upload DNA Files</h3>
                        <p>
                            Upload .txt, .fasta, .fa
                            or .fna DNA files.
                        </p>
                    </div>

                    <div className="feature-box">
                        <div>🧬</div>
                        <h3>Sequence Prediction</h3>
                        <p>
                            Analyze DNA sequences using
                            a Deep Learning Transformer.
                        </p>
                    </div>

                    <div className="feature-box">
                        <div>📊</div>
                        <h3>Confidence Score</h3>
                        <p>
                            View the confidence of
                            the sequence prediction.
                        </p>
                    </div>

                </div>

            </section>

        </div>
    );
}

export default Home;
