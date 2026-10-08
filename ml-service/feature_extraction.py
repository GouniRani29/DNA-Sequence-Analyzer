import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer


# ----------------------------------------
# PROJECT PATH
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# ----------------------------------------
# LOAD DATA
# ----------------------------------------

def load_data():

    file_path = DATA_DIR / "human_data.txt"

    data = pd.read_table(file_path)

    return data


# ----------------------------------------
# CLEAN DNA
# ----------------------------------------

def clean_sequence(sequence):

    sequence = sequence.upper()

    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")

    return sequence


# ----------------------------------------
# CREATE K-MER STRING
# ----------------------------------------

def create_kmer_string(sequence, k=6):

    sequence = clean_sequence(sequence)

    kmers = []

    for i in range(len(sequence) - k + 1):

        kmers.append(sequence[i:i + k])

    return " ".join(kmers)


# ----------------------------------------
# CREATE FEATURE MATRIX
# ----------------------------------------

def create_features(data, k=6):

    sequences = data["sequence"].apply(
        lambda sequence: create_kmer_string(sequence, k)
    )

    vectorizer = CountVectorizer(
        analyzer="word",
        lowercase=False
    )

    X = vectorizer.fit_transform(sequences)

    y = data["class"]

    return X, y, vectorizer


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    data = load_data()

    print("Dataset shape:")
    print(data.shape)

    X, y, vectorizer = create_features(data, k=6)

    print("\n========== FEATURE MATRIX ==========")

    print("X shape:")
    print(X.shape)

    print("\nY shape:")
    print(y.shape)

    print("\nNumber of features:")
    print(len(vectorizer.get_feature_names_out()))

    print("\nFirst 20 features:")

    print(
        vectorizer.get_feature_names_out()[:20]
    )

    print("\nClass distribution:")

    print(y.value_counts().sort_index())