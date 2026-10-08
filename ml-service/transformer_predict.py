import torch

from transformer_model import DNATransformerClassifier
from transformer_tokenizer import DNATokenizer
from preprocess import clean_sequence


# =========================================================
# CONFIGURATION
# =========================================================

KMER_SIZE = 6

MAX_SEQUENCE_LENGTH = 1024

MAX_TOKENS = MAX_SEQUENCE_LENGTH - KMER_SIZE + 1

NUM_CLASSES = 7

MODEL_PATH = "transformer_best_model.pt"


# =========================================================
# DEVICE
# =========================================================

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

print("=" * 60)
print("DNA TRANSFORMER PREDICTION")
print("=" * 60)

print("\nDevice:")
print(DEVICE)


# =========================================================
# LOAD TOKENIZER
# =========================================================

print("\nLoading tokenizer...")

tokenizer = DNATokenizer(
    k=KMER_SIZE
)

print(
    "Vocabulary size:",
    len(tokenizer.token_to_id)
)


# =========================================================
# CREATE MODEL
# =========================================================

print("\nCreating Transformer model...")

model = DNATransformerClassifier(
    vocab_size=len(tokenizer.token_to_id),
    num_classes=NUM_CLASSES,
    max_length=MAX_TOKENS,
    embedding_dim=128,
    num_heads=4,
    num_layers=2,
    feed_forward_dim=256,
    dropout=0.15
)


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

print("\nLoading trained Transformer model...")

model.load_state_dict(
    torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )
)

model = model.to(DEVICE)

model.eval()

print("✓ Transformer model loaded successfully.")


# =========================================================
# VALIDATE DNA SEQUENCE
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
# PREPARE DNA SEQUENCE
# =========================================================

def prepare_sequence(sequence):

    # Clean sequence
    sequence = clean_sequence(sequence)

    # Validate
    if not validate_sequence(sequence):

        raise ValueError(
            "Invalid DNA sequence. "
            "Only A, T, G and C are allowed."
        )

    # Tokenize
    token_ids = tokenizer.encode(sequence)

    # Truncate
    token_ids = token_ids[:MAX_TOKENS]

    # Padding
    pad_id = tokenizer.token_to_id[
        tokenizer.PAD_TOKEN
    ]

    padding_length = (
        MAX_TOKENS - len(token_ids)
    )

    token_ids += [
        pad_id
    ] * padding_length

    # Attention mask
    attention_mask = [
        1 if token_id != pad_id else 0
        for token_id in token_ids
    ]

    # Convert to tensors
    input_ids = torch.tensor(
        [token_ids],
        dtype=torch.long
    ).to(DEVICE)

    attention_mask = torch.tensor(
        [attention_mask],
        dtype=torch.long
    ).to(DEVICE)

    return (
        input_ids,
        attention_mask,
        sequence
    )


# =========================================================
# PREDICTION FUNCTION
# =========================================================

def predict_gene_family(sequence):

    (
        input_ids,
        attention_mask,
        cleaned_sequence
    ) = prepare_sequence(sequence)

    with torch.no_grad():

        logits = model(
            input_ids,
            attention_mask
        )

        probabilities = torch.softmax(
            logits,
            dim=1
        )

        prediction = torch.argmax(
            probabilities,
            dim=1
        ).item()

        confidence = (
            probabilities[0][prediction].item()
            * 100
        )

    # -----------------------------------------------------
    # ALL CLASS PROBABILITIES
    # -----------------------------------------------------

    probability_dict = {}

    for index, probability in enumerate(
        probabilities[0]
    ):

        probability_dict[str(index)] = round(
            probability.item() * 100,
            2
        )

    return {

        "success": True,

        "predictedClass": prediction,

        "confidence": round(
            confidence,
            2
        ),

        "probabilities": probability_dict,

        "sequence": cleaned_sequence

    }


# =========================================================
# TEST MULTIPLE DNA SEQUENCES
# =========================================================

if __name__ == "__main__":

    print("\n" + "=" * 60)
    print("MULTI-SEQUENCE TEST")
    print("=" * 60)

    # -----------------------------------------------------
    # PUT DIFFERENT DNA SEQUENCES HERE
    # -----------------------------------------------------

    test_sequences = [

        "ATGCCCCAACTAAATACTACCGTATGGGCCACCATAATTACCCCATACTC",

        "ATGCGTACGTAGCTAGCTAGCGATCGATCGTAGCTAGCTAGCTAGCTA",

        "GCTAGCTAGCATCGATCGATCGATGCGTACGTACGTAGCTAGCTA",

        "TTTTTTTTTTTTTTTTTTTTCCCCCCCCCCCCCCCCCCCC",

        "GGGGGGGGGGGGGGGGGGGGAAAAAAAAAAAAAAAAAAAA"

    ]


    # -----------------------------------------------------
    # TEST EACH SEQUENCE
    # -----------------------------------------------------

    for i, sample_sequence in enumerate(
        test_sequences,
        start=1
    ):

        print("\n" + "-" * 60)

        print(
            f"TEST SEQUENCE {i}"
        )

        print("-" * 60)

        print(
            "\nDNA Sequence:"
        )

        print(sample_sequence)

        print(
            "\nSequence Length:",
            len(sample_sequence)
        )

        try:

            result = predict_gene_family(
                sample_sequence
            )

            print(
                "\nPrediction Result:"
            )

            print(
                "Predicted Class :",
                result["predictedClass"]
            )

            print(
                "Confidence      :",
                result["confidence"],
                "%"
            )

            print(
                "\nClass Probabilities:"
            )

            for class_id, probability in result[
                "probabilities"
            ].items():

                print(
                    f"Class {class_id}: "
                    f"{probability}%"
                )

        except Exception as error:

            print(
                "\nERROR:",
                error
            )


    print("\n" + "=" * 60)
    print("MULTI-SEQUENCE TEST COMPLETED")
    print("=" * 60)