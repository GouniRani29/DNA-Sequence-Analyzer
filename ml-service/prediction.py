import joblib
from pathlib import Path


# =========================================================
# PATH
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

MODEL_PATH = (
    BASE_DIR
    / "models"
    / "dna_xgboost_pipeline.pkl"
)


# =========================================================
# LOAD MODEL
# =========================================================

print("Loading trained XGBoost pipeline...")

model = joblib.load(MODEL_PATH)

print("Model loaded successfully.")


# =========================================================
# CLEAN DNA
# =========================================================

def clean_sequence(sequence):

    sequence = str(sequence).upper()

    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")

    return sequence


# =========================================================
# VALIDATE DNA
# =========================================================

def validate_sequence(sequence):

    valid_bases = {
        "A",
        "T",
        "G",
        "C"
    }

    if not sequence:

        return False

    return all(
        base in valid_bases
        for base in sequence
    )


# =========================================================
# CREATE K-MERS
# =========================================================

def create_kmer_string(sequence, k=6):

    sequence = clean_sequence(
        sequence
    )

    if len(sequence) < k:

        raise ValueError(
            f"DNA sequence must contain at least {k} bases."
        )

    kmers = []

    for i in range(
        len(sequence) - k + 1
    ):

        kmers.append(
            sequence[i:i + k]
        )

    return " ".join(kmers)


# =========================================================
# PREDICT
# =========================================================

def predict_gene_family(sequence):

    # -----------------------------------------------------
    # CLEAN
    # -----------------------------------------------------

    sequence = clean_sequence(
        sequence
    )


    # -----------------------------------------------------
    # VALIDATE
    # -----------------------------------------------------

    if not validate_sequence(
        sequence
    ):

        raise ValueError(
            "Invalid DNA sequence. "
            "Only A, T, G and C are allowed."
        )


    # -----------------------------------------------------
    # CREATE K-MERS
    # -----------------------------------------------------

    kmer_sequence = create_kmer_string(
        sequence,
        k=6
    )


    # -----------------------------------------------------
    # MODEL PREDICTION
    # -----------------------------------------------------

    prediction = model.predict(
        [kmer_sequence]
    )[0]


    # -----------------------------------------------------
    # PREDICTION PROBABILITIES
    # -----------------------------------------------------

    probabilities = model.predict_proba(
        [kmer_sequence]
    )[0]


    # -----------------------------------------------------
    # CONFIDENCE
    # -----------------------------------------------------

    confidence = float(
        max(probabilities) * 100
    )


    # -----------------------------------------------------
    # CLEAN PROBABILITIES
    # -----------------------------------------------------

    probability_dict = {}

    for index, probability in enumerate(
        probabilities
    ):

        probability_dict[
            str(index)
        ] = float(
            round(
                float(probability) * 100,
                2
            )
        )


    # -----------------------------------------------------
    # FINAL RESULT
    # -----------------------------------------------------

    return {

        "predictedClass": int(
            prediction
        ),

        "confidence": float(
            round(
                confidence,
                2
            )
        ),

        "probabilities": probability_dict

    }


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    sample_sequence = (
        "ATGCCCCAACTAAATACTACCGTATGG"
        "GCCACCAT AATTACCCCATACTC"
        .replace(" ", "")
    )

    result = predict_gene_family(
        sample_sequence
    )

    print(
        "\nPrediction Result:"
    )

    print(result)