
import joblib
import pandas as pd
from pathlib import Path

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

# Paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "models" / "dna_xgboost_pipeline.pkl"
DATA_PATH = BASE_DIR.parent / "data" / "human_data.txt"

# Load saved model
print("Loading saved XGBoost model...")
model = joblib.load(MODEL_PATH)
print("Model loaded successfully!")

# Load dataset
data = pd.read_table(DATA_PATH)
print("Dataset shape:", data.shape)

# Create overlapping 6-mers
def create_kmer_string(sequence, k=6):
    sequence = str(sequence).upper().replace(" ", "")
    return " ".join(
        sequence[i:i + k]
        for i in range(len(sequence) - k + 1)
    )

# Prepare data
X = data["sequence"].apply(create_kmer_string)
y = data["class"]

# Recreate test split
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

print("Test samples:", len(X_test))

# Predict using saved model (no fitting)
y_pred = model.predict(X_test.tolist())

# Calculate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(
    y_test, y_pred, average="weighted", zero_division=0
)
recall = recall_score(
    y_test, y_pred, average="weighted", zero_division=0
)
f1 = f1_score(
    y_test, y_pred, average="weighted", zero_division=0
)

# Display results
print("\n========== XGBOOST RESULTS ==========")
print(f"Accuracy : {accuracy * 100:.2f}%")
print(f"Precision: {precision * 100:.2f}%")
print(f"Recall   : {recall * 100:.2f}%")
print(f"F1 Score : {f1 * 100:.2f}%")

print("\nClassification Report:")
print(classification_report(
    y_test, y_pred, zero_division=0
))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))
