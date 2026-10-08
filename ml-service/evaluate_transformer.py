import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from transformer_dataset import (
    create_datasets,
    tokenizer
)

from transformer_model import (
    DNATransformerClassifier
)


# =========================================================
# CONFIGURATION
# =========================================================

BATCH_SIZE = 8

DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

MODEL_PATH = "transformer_best_model.pt"


# =========================================================
# HEADER
# =========================================================

print("=" * 60)
print("DNA TRANSFORMER EVALUATION")
print("=" * 60)

print("\nDevice:")
print(DEVICE)


# =========================================================
# LOAD DATASET
# =========================================================

print("\nLoading datasets...")

train_dataset, val_dataset, test_dataset = create_datasets()

print("\nDataset sizes:")

print(
    "Training   :",
    len(train_dataset)
)

print(
    "Validation :",
    len(val_dataset)
)

print(
    "Testing    :",
    len(test_dataset)
)


# =========================================================
# TEST DATA LOADER
# =========================================================

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# =========================================================
# CREATE TRANSFORMER MODEL
# =========================================================
# IMPORTANT:
# These values MUST match the model used during training.
#
# Saved model:
# embedding_dim     = 128
# num_heads         = 4
# num_layers        = 2
# feed_forward_dim  = 256
# dropout           = 0.15
# =========================================================

print("\nCreating Transformer model...")

model = DNATransformerClassifier(
    vocab_size=len(
        tokenizer.token_to_id
    ),

    num_classes=7,

    max_length=1019,

    embedding_dim=128,

    num_heads=4,

    num_layers=2,

    feed_forward_dim=256,

    dropout=0.15
)

model = model.to(DEVICE)


# =========================================================
# LOAD TRAINED MODEL
# =========================================================

print("\nLoading trained Transformer model...")

try:

    state_dict = torch.load(
        MODEL_PATH,
        map_location=DEVICE
    )

    model.load_state_dict(
        state_dict
    )

    print(
        "Model loaded successfully."
    )

except Exception as e:

    print(
        "\nERROR: Could not load Transformer model."
    )

    print("\nReason:")
    print(e)

    raise


# =========================================================
# EVALUATION MODE
# =========================================================

model.eval()


# =========================================================
# PREDICTION
# =========================================================

all_predictions = []
all_labels = []

print(
    "\nRunning test predictions..."
)


with torch.no_grad():

    for batch in test_loader:

        # -------------------------------------------------
        # INPUT IDS
        # -------------------------------------------------

        input_ids = batch[
            "input_ids"
        ].to(DEVICE)

        # -------------------------------------------------
        # ATTENTION MASK
        # -------------------------------------------------

        attention_mask = batch[
            "attention_mask"
        ].to(DEVICE)

        # -------------------------------------------------
        # LABELS
        # -------------------------------------------------

        labels = batch[
            "label"
        ].to(DEVICE)

        # -------------------------------------------------
        # MODEL PREDICTION
        # -------------------------------------------------

        outputs = model(
            input_ids,
            attention_mask
        )

        # -------------------------------------------------
        # GET PREDICTED CLASS
        # -------------------------------------------------

        predictions = torch.argmax(
            outputs,
            dim=1
        )

        # -------------------------------------------------
        # STORE RESULTS
        # -------------------------------------------------

        all_predictions.extend(
            predictions.cpu().numpy()
        )

        all_labels.extend(
            labels.cpu().numpy()
        )


print(
    "Test predictions completed."
)


# =========================================================
# CALCULATE METRICS
# =========================================================

accuracy = accuracy_score(
    all_labels,
    all_predictions
)

precision = precision_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

recall = recall_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)

f1 = f1_score(
    all_labels,
    all_predictions,
    average="weighted",
    zero_division=0
)


# =========================================================
# DISPLAY RESULTS
# =========================================================

print("\n" + "=" * 60)

print(
    "TRANSFORMER TEST RESULTS"
)

print("=" * 60)

print(
    f"\nAccuracy : {accuracy:.4f}"
)

print(
    f"Precision: {precision:.4f}"
)

print(
    f"Recall   : {recall:.4f}"
)

print(
    f"F1 Score : {f1:.4f}"
)


# =========================================================
# CLASSIFICATION REPORT
# =========================================================

print(
    "\nClassification Report:"
)

print(
    classification_report(
        all_labels,
        all_predictions,
        digits=4,
        zero_division=0
    )
)


# =========================================================
# CONFUSION MATRIX
# =========================================================

print(
    "\nConfusion Matrix:"
)

cm = confusion_matrix(
    all_labels,
    all_predictions
)

print(cm)


# =========================================================
# COMPLETE
# =========================================================

print(
    "\n" + "=" * 60
)

print(
    "TRANSFORMER EVALUATION COMPLETED"
)

print(
    "=" * 60
)