import pandas as pd
from pathlib import Path

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier


# ============================================
# PROJECT PATH
# ============================================

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR.parent / "data"


# ============================================
# LOAD DATA
# ============================================

def load_data():

    file_path = DATA_DIR / "human_data.txt"

    data = pd.read_table(file_path)

    return data


# ============================================
# CLEAN DNA
# ============================================

def clean_sequence(sequence):

    sequence = sequence.upper()

    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")

    return sequence


# ============================================
# CREATE K-MER STRING
# ============================================

def create_kmer_string(sequence, k=6):

    sequence = clean_sequence(sequence)

    kmers = []

    for i in range(len(sequence) - k + 1):

        kmers.append(sequence[i:i + k])

    return " ".join(kmers)


# ============================================
# PREPARE FEATURES
# ============================================

def prepare_features(data):

    print("\nCreating k-mer sequences...")

    kmer_sequences = data["sequence"].apply(
        lambda sequence: create_kmer_string(sequence, k=6)
    )

    print("Creating numerical feature matrix...")

    vectorizer = CountVectorizer(
        analyzer="word",
        lowercase=False
    )

    X = vectorizer.fit_transform(kmer_sequences)

    y = data["class"]

    return X, y, vectorizer


# ============================================
# EVALUATION FUNCTION
# ============================================

def evaluate_model(model, X_test, y_test, model_name):

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    precision = precision_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    recall = recall_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    f1 = f1_score(
        y_test,
        predictions,
        average="weighted",
        zero_division=0
    )

    print("\n========================================")
    print(model_name)
    print("========================================")

    print("Accuracy :", round(accuracy, 4))
    print("Precision:", round(precision, 4))
    print("Recall   :", round(recall, 4))
    print("F1 Score :", round(f1, 4))

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    return {
        "accuracy": accuracy,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }


# ============================================
# RANDOM FOREST
# ============================================

def train_random_forest(X_train, y_train):

    print("\nTraining Random Forest...")

    model = RandomForestClassifier(
        n_estimators=200,
        random_state=42,
        n_jobs=-1,
        class_weight="balanced"
    )

    model.fit(
        X_train,
        y_train
    )

    print("Random Forest training completed.")

    return model


# ============================================
# XGBOOST
# ============================================

def train_xgboost(X_train, y_train):

    print("\nTraining XGBoost...")

    model = XGBClassifier(
        n_estimators=300,
        max_depth=6,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="multi:softprob",
        num_class=7,
        eval_metric="mlogloss",
        random_state=42,
        n_jobs=-1
    )

    model.fit(
        X_train,
        y_train
    )

    print("XGBoost training completed.")

    return model


# ============================================
# MAIN
# ============================================

if __name__ == "__main__":

    print("========================================")
    print("AI DNA SEQUENCE CLASSIFICATION")
    print("========================================")

    # ----------------------------------------
    # Load data
    # ----------------------------------------

    data = load_data()

    print("\nDataset shape:")
    print(data.shape)

    # ----------------------------------------
    # Prepare features
    # ----------------------------------------

    X, y, vectorizer = prepare_features(data)

    print("\nFeature matrix:")
    print(X.shape)

    # ----------------------------------------
    # Train/Test split
    # ----------------------------------------

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print("Training samples:", X_train.shape[0])
    print("Testing samples :", X_test.shape[0])

    # ========================================
    # RANDOM FOREST
    # ========================================

    random_forest = train_random_forest(
        X_train,
        y_train
    )

    rf_results = evaluate_model(
        random_forest,
        X_test,
        y_test,
        "RANDOM FOREST RESULTS"
    )

    # ========================================
    # XGBOOST
    # ========================================

    xgb_model = train_xgboost(
        X_train,
        y_train
    )

    xgb_results = evaluate_model(
        xgb_model,
        X_test,
        y_test,
        "XGBOOST RESULTS"
    )

    # ========================================
    # FINAL COMPARISON
    # ========================================

    print("\n")
    print("========================================")
    print("MODEL COMPARISON")
    print("========================================")

    print(
        f"Random Forest Accuracy : "
        f"{rf_results['accuracy']:.4f}"
    )

    print(
        f"XGBoost Accuracy       : "
        f"{xgb_results['accuracy']:.4f}"
    )

    print(
        f"\nRandom Forest F1       : "
        f"{rf_results['f1']:.4f}"
    )

    print(
        f"XGBoost F1             : "
        f"{xgb_results['f1']:.4f}"
    )

    # ----------------------------------------
    # Determine winner
    # ----------------------------------------

    if xgb_results["f1"] > rf_results["f1"]:

        print("\n🏆 XGBoost performed better.")

    elif rf_results["f1"] > xgb_results["f1"]:

        print("\n🏆 Random Forest performed better.")

    else:

        print("\n🤝 Both models have the same F1 score.")