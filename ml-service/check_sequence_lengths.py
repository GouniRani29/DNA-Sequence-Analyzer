
from preprocess import load_human_data, clean_sequence

# =========================================================
# LOAD DATASET
# =========================================================

data = load_human_data()

print("Dataset shape:")
print(data.shape)

# =========================================================
# CALCULATE SEQUENCE LENGTHS
# =========================================================

lengths = []

for sequence in data["sequence"]:

    sequence = clean_sequence(sequence)

    lengths.append(len(sequence))

# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\nSequence Length Statistics")
print("--------------------------")

print("Minimum length :", min(lengths))
print("Maximum length :", max(lengths))
print("Average length :", round(sum(lengths) / len(lengths), 2))

# =========================================================
# IMPORTANT PERCENTILES
# =========================================================

sorted_lengths = sorted(lengths)

def percentile(values, percentage):

    index = int(
        len(values) * percentage / 100
    )

    if index >= len(values):
        index = len(values) - 1

    return values[index]


print("\nPercentiles")
print("-----------")

print("50% :", percentile(sorted_lengths, 50))
print("75% :", percentile(sorted_lengths, 75))
print("90% :", percentile(sorted_lengths, 90))
print("95% :", percentile(sorted_lengths, 95))
print("99% :", percentile(sorted_lengths, 99))