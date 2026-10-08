import { useState } from "react";
import "./DNAAnalyzer.css";

function DNAAnalyzer() {
    const [sequence, setSequence] = useState("");
    const [fileName, setFileName] = useState("");
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState("");
    const classNames = {
  0: "G protein-coupled receptors (GPCRs)",
  1: "Tyrosine Kinase",
  2: "Tyrosine Phosphatase",
  3: "Synthetase",
  4: "Synthase",
  5: "Ion Channel",
  6: "Transcription Factor"
};

    // ================================
    // HANDLE TEXT INPUT
    // ================================
    const handleSequenceChange = (e) => {
        setSequence(e.target.value);
        setFileName("");
        setResult(null);
        setError("");
    };

    // ================================
    // HANDLE FILE UPLOAD
    // ================================
    const handleFileUpload = (e) => {
        const file = e.target.files[0];

        if (!file) {
            return;
        }

        setError("");
        setResult(null);
        setFileName(file.name);

        const allowedExtensions = [
            ".txt",
            ".fasta",
            ".fa",
            ".fna"
        ];

        const fileNameLower = file.name.toLowerCase();

        const validFile = allowedExtensions.some(
            (extension) =>
                fileNameLower.endsWith(extension)
        );

        if (!validFile) {
            setError(
                "Invalid file. Please upload a .txt, .fasta, .fa or .fna file."
            );

            setFileName("");
            return;
        }

        const reader = new FileReader();

        reader.onload = (event) => {
            let content = event.target.result;

            // ================================
            // REMOVE FASTA HEADER
            // ================================
            if (
                fileNameLower.endsWith(".fasta") ||
                fileNameLower.endsWith(".fa") ||
                fileNameLower.endsWith(".fna")
            ) {
                content = content
                    .split("\n")
                    .filter(
                        (line) =>
                            !line.trim().startsWith(">")
                    )
                    .join("");
            }

            // ================================
            // CLEAN DNA
            // ================================
            content = content
                .replace(/\s/g, "")
                .toUpperCase();

            // ================================
            // VALIDATE DNA
            // ================================
            const validDNA = /^[ATGC]+$/.test(content);

            if (!validDNA) {
                setError(
                    "Invalid DNA file. The file must contain only A, T, G and C bases."
                );

                setSequence("");
                setFileName("");

                return;
            }

            setSequence(content);
        };

        reader.onerror = () => {
            setError(
                "Unable to read the selected file."
            );
        };

        reader.readAsText(file);
    };

    // ================================
    // ANALYZE DNA
    // ================================
    const analyzeDNA = async () => {
        if (!sequence.trim()) {
            setError(
                "Please enter a DNA sequence or upload a DNA file."
            );

            return;
        }

        setLoading(true);
        setError("");
        setResult(null);

        try {
            const response = await fetch(
                "http://localhost:8080/analysis",
                {
                    method: "POST",

                    headers: {
                        "Content-Type": "application/json"
                    },

                    body: JSON.stringify({
                        sequence: sequence
                    })
                }
            );

            if (!response.ok) {
                throw new Error(
                    "DNA analysis failed."
                );
            }

            const data = await response.json();

            setResult(data);

        } catch (error) {
            setError(
                error.message ||
                "Something went wrong."
            );

        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="dna-page">

            {/* ================================
                ANALYZER HEADER
            ================================= */}

            <div className="dna-header">

                <div className="dna-title-row">
                    <span className="dna-title-icon">
                        🧬
                    </span>

                    <div>
                        <h1>
                             DNA Sequence Analyzer
                        </h1>

                        <p>
                            Analyze DNA sequences using a
                            Deep Learning Transformer model
                        </p>
                    </div>
                </div>

            </div>


            {/* ================================
                ANALYZER CARD
            ================================= */}

            <div className="dna-card">

                {/* ================================
                    FILE UPLOAD
                ================================= */}

                <div className="input-section">

                    <h2>
                        Upload DNA File
                    </h2>

                    <p className="section-help">
                        Supported formats: .txt, .fasta, .fa, .fna
                    </p>

                    <div className="file-upload-box">

                        <label
                            htmlFor="dna-file"
                            className="file-button"
                        >
                            📁 Choose DNA File
                        </label>

                        <input
                            id="dna-file"
                            type="file"
                            accept=".txt,.fasta,.fa,.fna"
                            onChange={handleFileUpload}
                        />

                        {!fileName && (
                            <span className="file-placeholder">
                                No file chosen
                            </span>
                        )}

                    </div>


                    {fileName && (
                        <div className="selected-file">
                            ✓ Selected file:
                            <strong> {fileName}</strong>
                        </div>
                    )}

                </div>


                {/* ================================
                    OR DIVIDER
                ================================= */}

                <div className="or-divider">

                    <span></span>

                    <strong>OR</strong>

                    <span></span>

                </div>


                {/* ================================
                    TEXT INPUT
                ================================= */}

                <div className="input-section">

                    <h2>
                        Enter DNA Sequence
                    </h2>

                    <p className="section-help">
                        Enter a DNA sequence containing only A, T, G and C bases.
                    </p>

                    <textarea
                        value={sequence}
                        onChange={handleSequenceChange}
                        placeholder="Example: ATGCGTACGTAGCTAGCTAG..."
                        className="dna-textarea"
                    ></textarea>


                    <div className="sequence-info">

                        <span>
                            Sequence Length
                        </span>

                        <strong>
                            {sequence.length}
                        </strong>

                    </div>

                </div>


                {/* ================================
                    ERROR MESSAGE
                ================================= */}

                {error && (
                    <div className="dna-error">
                        ⚠️ {error}
                    </div>
                )}


                {/* ================================
                    ANALYZE BUTTON
                ================================= */}

                <button
                    className="analyze-button"
                    onClick={analyzeDNA}
                    disabled={loading}
                >
                    {loading
                        ? "⏳ Analyzing DNA..."
                        : "🧬 Analyze DNA →"
                    }
                </button>


                {/* ================================
                    RESULT
                ================================= */}

                {result && (
                    <div className="result-card">

                        <div className="result-header">

                            <span className="result-icon">
                                🤖
                            </span>

                            <div>
                                <h2>
                                    Prediction Result
                                </h2>

                                <p>
                                    DNA analysis completed successfully
                                </p>
                            </div>

                        </div>


                        <div className="result-grid">

                            <div className="result-item">

    <span>
    Predicted Class
</span>

<strong>
    {result.prediction} - {classNames[result.prediction]}
</strong>

</div>


                            <div className="result-item">

                                <span>
                                    Confidence
                                </span>

                                <strong>
                                    {result.confidence}%
                                </strong>

                            </div>


                            <div className="result-item">

                                <span>
                                    Sequence Length
                                </span>

                                <strong>
                                    {sequence.length}
                                </strong>

                            </div>

                        </div>

                    </div>
                )}

            </div>

        </div>
    );
}

export default DNAAnalyzer;