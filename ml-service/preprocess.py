import pandas as pd
from pathlib import Path


# ----------------------------------------
# PROJECT PATH
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# ----------------------------------------
# LOAD HUMAN DATA
# ----------------------------------------

def load_human_data():

    file_path = DATA_DIR / "human_data.txt"

    data = pd.read_table(file_path)

    return data


# ----------------------------------------
# CLEAN DNA SEQUENCE
# ----------------------------------------

def clean_sequence(sequence):

    sequence = sequence.upper()

    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")

    return sequence


# ----------------------------------------
# VALIDATE DNA
# ----------------------------------------

def is_valid_sequence(sequence):

    valid_bases = {"A", "T", "G", "C"}

    return all(base in valid_bases for base in sequence)


# ----------------------------------------
# CREATE K-MERS
# ----------------------------------------

def create_kmers(sequence, k=6):

    sequence = clean_sequence(sequence)

    kmers = []

    for i in range(len(sequence) - k + 1):

        kmer = sequence[i:i + k]

        kmers.append(kmer)

    return kmers


# ----------------------------------------
# TEST
# ----------------------------------------

if __name__ == "__main__":

    data = load_human_data()

    print("Dataset shape:", data.shape)

    print("\nColumns:")
    print(data.columns.tolist())

    sample_sequence = data.iloc[0]["sequence"]

    print("\nOriginal sequence:")
    print(sample_sequence[:100])

    cleaned = clean_sequence(sample_sequence)

    print("\nCleaned sequence:")
    print(cleaned[:100])

    print("\nSequence valid:")
    print(is_valid_sequence(cleaned))

    kmers = create_kmers(cleaned, k=6)

    print("\nNumber of 6-mers:")
    print(len(kmers))

    print("\nFirst 10 k-mers:")
    print(kmers[:10])
    