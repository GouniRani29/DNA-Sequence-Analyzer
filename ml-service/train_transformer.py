import torch
import torch.nn as nn

from torch.utils.data import DataLoader

from sklearn.metrics import (
    accuracy_score,
    f1_score
)
from sklearn.utils.class_weight import compute_class_weight

import numpy as np

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

BATCH_SIZE = 32          # was 8 -> less noisy gradients, faster per-epoch wall time
EPOCHS = 80               # was 12 -> your run was still improving when it stopped
LEARNING_RATE = 0.0001
WEIGHT_DECAY = 0.01
PATIENCE = 8              # was 3 -> give it more room before stopping for real
NUM_CLASSES = 7
WARMUP_RATIO = 0.05       # fraction of total steps used for LR warmup


DEVICE = torch.device(
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)


print("=" * 60)
print("DNA TRANSFORMER TRAINING - VERSION 4")
print("=" * 60)

print("\nDevice:")
print(DEVICE)


# =========================================================
# CREATE DATASETS
# =========================================================

print("\nPreparing datasets...")

train_dataset, val_dataset, test_dataset = \
    create_datasets()


print("\nDataset sizes:")
print("Training   :", len(train_dataset))
print("Validation :", len(val_dataset))
print("Testing    :", len(test_dataset))


# =========================================================
# DATA LOADERS
# =========================================================

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True
)

val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)

test_loader = DataLoader(
    test_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False
)


# =========================================================
# CLASS WEIGHTS (fixes the class-4 / class-2 recall problem)
# =========================================================

print("\nComputing class weights...")

all_train_labels = [
    int(train_dataset[i]["label"])
    for i in range(len(train_dataset))
]

class_weights = compute_class_weight(
    class_weight="balanced",
    classes=np.arange(NUM_CLASSES),
    y=all_train_labels
)

class_weights = torch.tensor(
    class_weights, dtype=torch.float
).to(DEVICE)

print("Class weights:", class_weights.cpu().numpy())


# =========================================================
# CREATE MODEL
# =========================================================

print("\nCreating Transformer model...")

model = DNATransformerClassifier(
    vocab_size=len(tokenizer.token_to_id),
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
# LOSS FUNCTION (now class-weighted)
# =========================================================

criterion = nn.CrossEntropyLoss(weight=class_weights)


# =========================================================
# OPTIMIZER
# =========================================================

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=LEARNING_RATE,
    weight_decay=WEIGHT_DECAY
)


# =========================================================
# LR WARMUP (per-step, first WARMUP_RATIO of total steps)
# =========================================================

total_steps = len(train_loader) * EPOCHS
warmup_steps = max(1, int(WARMUP_RATIO * total_steps))
global_step = 0

def warmup_lr(step):
    return min(1.0, float(step + 1) / float(warmup_steps))

warmup_scheduler = torch.optim.lr_scheduler.LambdaLR(
    optimizer, lr_lambda=warmup_lr
)


# =========================================================
# PLATEAU SCHEDULER (kicks in after warmup finishes)
# =========================================================

scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(
    optimizer,
    mode="max",
    factor=0.5,
    patience=2
)


# =========================================================
# TRAINING
# =========================================================

best_val_accuracy = 0.0
epochs_without_improvement = 0

for epoch in range(EPOCHS):

    print("\n" + "=" * 60)
    print(f"EPOCH {epoch + 1}/{EPOCHS}")
    print("=" * 60)

    # =====================================================
    # TRAIN
    # =====================================================

    model.train()
    total_loss = 0.0
    all_predictions = []
    all_labels = []

    for batch in train_loader:

        input_ids = batch["input_ids"].to(DEVICE)
        attention_mask = batch["attention_mask"].to(DEVICE)
        labels = batch["label"].to(DEVICE)

        optimizer.zero_grad()

        outputs = model(input_ids, attention_mask)
        loss = criterion(outputs, labels)
        loss.backward()

        torch.nn.utils.clip_grad_norm_(
            model.parameters(), max_norm=1.0
        )

        optimizer.step()

        # step the warmup scheduler only until warmup is done
        if global_step < warmup_steps:
            warmup_scheduler.step()
        global_step += 1

        total_loss += loss.item()

        predictions = torch.argmax(outputs, dim=1)
        all_predictions.extend(predictions.detach().cpu().numpy())
        all_labels.extend(labels.detach().cpu().numpy())

    train_loss = total_loss / len(train_loader)
    train_accuracy = accuracy_score(all_labels, all_predictions)
    train_f1 = f1_score(
        all_labels, all_predictions, average="weighted", zero_division=0
    )

    print(f"\nTraining Loss : {train_loss:.4f}")
    print(f"Training Accuracy : {train_accuracy:.4f}")
    print(f"Training F1 : {train_f1:.4f}")

    # =====================================================
    # VALIDATION
    # =====================================================

    model.eval()
    val_predictions = []
    val_labels = []
    val_loss_total = 0.0

    with torch.no_grad():
        for batch in val_loader:
            input_ids = batch["input_ids"].to(DEVICE)
            attention_mask = batch["attention_mask"].to(DEVICE)
            labels = batch["label"].to(DEVICE)

            outputs = model(input_ids, attention_mask)
            loss = criterion(outputs, labels)
            val_loss_total += loss.item()

            predictions = torch.argmax(outputs, dim=1)
            val_predictions.extend(predictions.cpu().numpy())
            val_labels.extend(labels.cpu().numpy())

    val_loss = val_loss_total / len(val_loader)
    val_accuracy = accuracy_score(val_labels, val_predictions)
    val_f1 = f1_score(
        val_labels, val_predictions, average="weighted", zero_division=0
    )

    print(f"\nValidation Loss : {val_loss:.4f}")
    print(f"Validation Accuracy : {val_accuracy:.4f}")
    print(f"Validation F1 : {val_f1:.4f}")

    # =====================================================
    # LEARNING RATE (plateau scheduler, only after warmup)
    # =====================================================

    if global_step >= warmup_steps:
        scheduler.step(val_f1)

    current_lr = optimizer.param_groups[0]["lr"]
    print(f"\nLearning Rate : {current_lr:.8f}")

    # =====================================================
    # SAVE BEST MODEL
    # =====================================================

    if val_accuracy > best_val_accuracy:
        best_val_accuracy = val_accuracy
        epochs_without_improvement = 0
        torch.save(model.state_dict(), "transformer_best_model.pt")
        print("\n✓ Best Transformer model saved.")
    else:
        epochs_without_improvement += 1
        print("\nNo validation improvement.")

    # =====================================================
    # EARLY STOPPING
    # =====================================================

    if epochs_without_improvement >= PATIENCE:
        print("\nEarly stopping triggered.")
        break


# =========================================================
# TRAINING COMPLETE
# =========================================================

print("\n" + "=" * 60)
print("TRAINING COMPLETED")
print("=" * 60)

print(f"\nBest Validation Accuracy: {best_val_accuracy:.4f}")
print("\nSaved model:")
print("transformer_best_model.pt")
