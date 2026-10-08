from pathlib import Path
import pandas as pd


# ----------------------------------------
# PROJECT PATHS
# ----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# ----------------------------------------
# LOAD DATASETS
# ----------------------------------------

human_path = DATA_DIR / "human_data.txt"
chimp_path = DATA_DIR / "chimp_data.txt"
dog_path = DATA_DIR / "dog_data.txt"


human_data = pd.read_table(human_path)
chimp_data = pd.read_table(chimp_path)
dog_data = pd.read_table(dog_path)


# ----------------------------------------
# BASIC INFORMATION
# ----------------------------------------

print("\n========== HUMAN DATA ==========")

print("Shape:", human_data.shape)

print("\nColumns:")
print(human_data.columns.tolist())

print("\nFirst 5 rows:")
print(human_data.head())

print("\nMissing values:")
print(human_data.isnull().sum())

print("\nClass distribution:")
print(human_data["class"].value_counts().sort_index())


print("\n========== CHIMP DATA ==========")

print("Shape:", chimp_data.shape)

print("\nClass distribution:")
print(chimp_data["class"].value_counts().sort_index())


print("\n========== DOG DATA ==========")

print("Shape:", dog_data.shape)

print("\nClass distribution:")
print(dog_data["class"].value_counts().sort_index())


# ----------------------------------------
# DNA SEQUENCE EXAMPLE
# ----------------------------------------

sample_sequence = human_data.iloc[0]["sequence"]

print("\n========== SAMPLE DNA ==========")

print("Sequence:")
print(sample_sequence)

print("\nSequence length:")
print(len(sample_sequence))


# ----------------------------------------
# NUCLEOTIDE COUNTS
# ----------------------------------------

sequence = sample_sequence.upper()

print("\n========== NUCLEOTIDE COUNTS ==========")

print("A:", sequence.count("A"))
print("T:", sequence.count("T"))
print("G:", sequence.count("G"))
print("C:", sequence.count("C"))


# ----------------------------------------
# GC / AT CONTENT
# ----------------------------------------

length = len(sequence)

gc_count = sequence.count("G") + sequence.count("C")
at_count = sequence.count("A") + sequence.count("T")

gc_content = (gc_count / length) * 100
at_content = (at_count / length) * 100

print("\nGC Content:", round(gc_content, 2), "%")
print("AT Content:", round(at_content, 2), "%")
# ----------------------------------------
# K-MER EXTRACTION
# ----------------------------------------

def get_kmers(sequence, size=6):

    sequence = sequence.lower()

    kmers = []

    for i in range(len(sequence) - size + 1):
        kmer = sequence[i:i + size]
        kmers.append(kmer)

    return kmers


sample = "ATGCGATCG"

kmers = get_kmers(sample, size=3)

print("\n========== K-MER EXAMPLE ==========")

print("Original DNA:")
print(sample)

print("3-mers:")
print(kmers)