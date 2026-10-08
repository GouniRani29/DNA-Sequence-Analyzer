import torch
from torch.utils.data import Dataset, DataLoader
from sklearn.model_selection import train_test_split

from preprocess import load_human_data, clean_sequence
from transformer_tokenizer import DNATokenizer


# =========================================================
# CONFIGURATION
# =========================================================

KMER_SIZE = 6

# Maximum DNA sequence length
MAX_SEQUENCE_LENGTH = 1024

# 6-mer tokens for 1024 DNA bases
MAX_TOKENS = MAX_SEQUENCE_LENGTH - KMER_SIZE + 1


# =========================================================
# LOAD TOKENIZER
# =========================================================

tokenizer = DNATokenizer(k=KMER_SIZE)


# =========================================================
# DNA DATASET
# =========================================================

class DNADataset(Dataset):

    def __init__(self, sequences, labels):

        self.sequences = sequences
        self.labels = labels

    def __len__(self):

        return len(self.sequences)

    def __getitem__(self, index):

        sequence = clean_sequence(
            self.sequences[index]
        )

        token_ids = tokenizer.encode(
            sequence
        )

        # -----------------------------------------------
        # TRUNCATE
        # -----------------------------------------------

        token_ids = token_ids[:MAX_TOKENS]

        # -----------------------------------------------
        # PADDING
        # -----------------------------------------------

        padding_length = (
            MAX_TOKENS - len(token_ids)
        )

        token_ids += [
            tokenizer.token_to_id[
                tokenizer.PAD_TOKEN
            ]
        ] * padding_length

        # -----------------------------------------------
        # ATTENTION MASK
        # -----------------------------------------------

        attention_mask = [
            1 if token_id != tokenizer.token_to_id[
                tokenizer.PAD_TOKEN
            ]
            else 0
            for token_id in token_ids
        ]

        return {
            "input_ids": torch.tensor(
                token_ids,
                dtype=torch.long
            ),

            "attention_mask": torch.tensor(
                attention_mask,
                dtype=torch.long
            ),

            "label": torch.tensor(
                self.labels[index],
                dtype=torch.long
            )
        }


# =========================================================
# LOAD AND PREPARE DATA
# =========================================================

def prepare_data():

    data = load_human_data()

    sequences = []

    labels = []

    for _, row in data.iterrows():

        sequence = clean_sequence(
            row["sequence"]
        )

        label = int(row["class"])

        sequences.append(sequence)

        labels.append(label)

    return sequences, labels


# =========================================================
# TRAIN / VALIDATION / TEST SPLIT
# =========================================================

def create_datasets():

    sequences, labels = prepare_data()

    # -----------------------------------------------------
    # 70% TRAIN / 30% TEMPORARY
    # -----------------------------------------------------

    train_sequences, temp_sequences, \
    train_labels, temp_labels = train_test_split(
        sequences,
        labels,
        test_size=0.30,
        random_state=42,
        stratify=labels
    )

    # -----------------------------------------------------
    # 15% VALIDATION / 15% TEST
    # -----------------------------------------------------

    val_sequences, test_sequences, \
    val_labels, test_labels = train_test_split(
        temp_sequences,
        temp_labels,
        test_size=0.50,
        random_state=42,
        stratify=temp_labels
    )

    # -----------------------------------------------------
    # CREATE DATASETS
    # -----------------------------------------------------

    train_dataset = DNADataset(
        train_sequences,
        train_labels
    )

    val_dataset = DNADataset(
        val_sequences,
        val_labels
    )

    test_dataset = DNADataset(
        test_sequences,
        test_labels
    )

    return (
        train_dataset,
        val_dataset,
        test_dataset
    )


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNA TRANSFORMER DATASET")
    print("=" * 60)

    print("\nMaximum DNA length:")
    print(MAX_SEQUENCE_LENGTH)

    print("\nMaximum number of 6-mer tokens:")
    print(MAX_TOKENS)

    print("\nVocabulary size:")
    print(len(tokenizer.token_to_id))

    train_dataset, val_dataset, test_dataset = \
        create_datasets()

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

    # -----------------------------------------------------
    # CHECK ONE SAMPLE
    # -----------------------------------------------------

    sample = train_dataset[0]

    print("\nSample:")
    print(
        "Input IDs shape:",
        sample["input_ids"].shape
    )

    print(
        "Attention mask shape:",
        sample["attention_mask"].shape
    )

    print(
        "Label:",
        sample["label"].item()
    )