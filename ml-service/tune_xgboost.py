import pandas as pd
from pathlib import Path

from sklearn.model_selection import (
    train_test_split,
    RandomizedSearchCV,
    StratifiedKFold
)

from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    confusion_matrix
)

from xgboost import XGBClassifier

import joblib


# =========================================================
# PROJECT PATHS
# =========================================================

BASE_DIR = Path(__file__).resolve().parent

DATA_DIR = BASE_DIR.parent / "data"

MODEL_DIR = BASE_DIR / "models"

MODEL_DIR.mkdir(
    exist_ok=True
)


# =========================================================
# LOAD DATA
# =========================================================

def load_data():

    file_path = DATA_DIR / "human_data.txt"

    data = pd.read_table(file_path)

    return data


# =========================================================
# CLEAN DNA
# =========================================================

def clean_sequence(sequence):

    sequence = sequence.upper()

    sequence = sequence.replace(" ", "")
    sequence = sequence.replace("\n", "")
    sequence = sequence.replace("\r", "")

    return sequence


# =========================================================
# CREATE K-MER STRING
# =========================================================

def create_kmer_string(sequence, k=6):

    sequence = clean_sequence(sequence)

    kmers = []

    for i in range(len(sequence) - k + 1):

        kmers.append(
            sequence[i:i + k]
        )

    return " ".join(kmers)


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNA XGBOOST MODEL TUNING")
    print("=" * 60)

    # -----------------------------------------------------
    # LOAD DATA
    # -----------------------------------------------------

    data = load_data()

    print("\nDataset shape:")
    print(data.shape)

    # -----------------------------------------------------
    # CREATE K-MER TEXT
    # -----------------------------------------------------

    print("\nCreating 6-mer sequences...")

    data["kmer_sequence"] = data["sequence"].apply(
        lambda sequence: create_kmer_string(
            sequence,
            k=6
        )
    )

    X = data["kmer_sequence"]

    y = data["class"]

    # -----------------------------------------------------
    # TRAIN / TEST SPLIT
    # -----------------------------------------------------

    print("\nSplitting dataset...")

    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.20,
        random_state=42,
        stratify=y
    )

    print(
        "Training samples:",
        len(X_train)
    )

    print(
        "Testing samples:",
        len(X_test)
    )

    # -----------------------------------------------------
    # PIPELINE
    # -----------------------------------------------------

    pipeline = Pipeline(
        [
            (
                "vectorizer",

                CountVectorizer(
                    analyzer="word",
                    lowercase=False
                )
            ),

            (
                "model",

                XGBClassifier(
                    objective="multi:softprob",
                    num_class=7,
                    eval_metric="mlogloss",
                    random_state=42,
                    n_jobs=-1
                )
            )
        ]
    )

    # -----------------------------------------------------
    # PARAMETER SEARCH
    # -----------------------------------------------------

    parameter_grid = {

        "model__n_estimators": [
            200,
            300,
            400
        ],

        "model__max_depth": [
            4,
            6,
            8
        ],

        "model__learning_rate": [
            0.03,
            0.05,
            0.1
        ],

        "model__subsample": [
            0.8,
            1.0
        ],

        "model__colsample_bytree": [
            0.8,
            1.0
        ]
    }

    # -----------------------------------------------------
    # CROSS VALIDATION
    # -----------------------------------------------------

    cv = StratifiedKFold(
        n_splits=3,
        shuffle=True,
        random_state=42
    )

    # -----------------------------------------------------
    # RANDOMIZED SEARCH
    # -----------------------------------------------------

    print("\nStarting hyperparameter tuning...")

    search = RandomizedSearchCV(
        estimator=pipeline,
        param_distributions=parameter_grid,
        n_iter=8,
        scoring="f1_weighted",
        cv=cv,
        verbose=2,
        random_state=42,
        n_jobs=1
    )

    search.fit(
        X_train,
        y_train
    )

    # -----------------------------------------------------
    # BEST PARAMETERS
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("BEST PARAMETERS")
    print("=" * 60)

    print(
        search.best_params_
    )

    print("\nBest CV F1 Score:")

    print(
        round(
            search.best_score_,
            4
        )
    )

    # -----------------------------------------------------
    # FINAL TEST
    # -----------------------------------------------------

    print("\n" + "=" * 60)
    print("FINAL TEST SET EVALUATION")
    print("=" * 60)

    best_model = search.best_estimator_

    predictions = best_model.predict(
        X_test
    )

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

    print(
        "\nAccuracy :",
        round(accuracy, 4)
    )

    print(
        "Precision:",
        round(precision, 4)
    )

    print(
        "Recall   :",
        round(recall, 4)
    )

    print(
        "F1 Score :",
        round(f1, 4)
    )

    # -----------------------------------------------------
    # CLASSIFICATION REPORT
    # -----------------------------------------------------

    print("\nClassification Report:")

    print(
        classification_report(
            y_test,
            predictions,
            zero_division=0
        )
    )

    # -----------------------------------------------------
    # CONFUSION MATRIX
    # -----------------------------------------------------

    print("\nConfusion Matrix:")

    print(
        confusion_matrix(
            y_test,
            predictions
        )
    )

    # -----------------------------------------------------
    # SAVE COMPLETE PIPELINE
    # -----------------------------------------------------

    model_path = (
        MODEL_DIR /
        "dna_xgboost_pipeline.pkl"
    )

    joblib.dump(
        best_model,
        model_path
    )

    print("\n" + "=" * 60)

    print(
        "MODEL SAVED SUCCESSFULLY"
    )

    print("=" * 60)

    print(
        model_path
    )