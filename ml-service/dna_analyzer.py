def clean_sequence(sequence):

    sequence = sequence.upper()

    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")
    sequence = sequence.replace(" ", "")

    return sequence


def validate_sequence(sequence):

    valid_bases = {"A", "T", "G", "C"}

    return all(base in valid_bases for base in sequence)


def analyze_sequence(sequence):

    sequence = clean_sequence(sequence)

    if not validate_sequence(sequence):
        raise ValueError(
            "Invalid DNA sequence. Only A, T, G and C are allowed."
        )

    length = len(sequence)

    if length == 0:
        raise ValueError("DNA sequence cannot be empty.")

    adenine = sequence.count("A")
    thymine = sequence.count("T")
    guanine = sequence.count("G")
    cytosine = sequence.count("C")

    gc_count = guanine + cytosine
    at_count = adenine + thymine

    gc_content = (gc_count / length) * 100
    at_content = (at_count / length) * 100

    return {
        "sequenceLength": length,
        "adenine": adenine,
        "thymine": thymine,
        "guanine": guanine,
        "cytosine": cytosine,
        "gcContent": round(gc_content, 2),
        "atContent": round(at_content, 2)
    }


if __name__ == "__main__":

    test_sequence = "ATGCGATCGATCG"

    result = analyze_sequence(test_sequence)

    print(result)