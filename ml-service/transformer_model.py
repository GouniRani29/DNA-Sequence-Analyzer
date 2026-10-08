import torch
import torch.nn as nn


# =========================================================
# DNA TRANSFORMER CLASSIFIER - VERSION 3
# =========================================================

class DNATransformerClassifier(nn.Module):

    def __init__(
        self,
        vocab_size,
        num_classes=7,
        max_length=1019,
        embedding_dim=128,
        num_heads=4,
        num_layers=2,
        feed_forward_dim=256,
        dropout=0.15
    ):

        super().__init__()

        # -------------------------------------------------
        # TOKEN EMBEDDING
        # -------------------------------------------------

        self.embedding = nn.Embedding(
            num_embeddings=vocab_size,
            embedding_dim=embedding_dim,
            padding_idx=0
        )

        # -------------------------------------------------
        # POSITION EMBEDDING
        # -------------------------------------------------

        self.position_embedding = nn.Embedding(
            num_embeddings=max_length,
            embedding_dim=embedding_dim
        )

        # -------------------------------------------------
        # DROPOUT
        # -------------------------------------------------

        self.embedding_dropout = nn.Dropout(
            dropout
        )

        # -------------------------------------------------
        # TRANSFORMER ENCODER
        # -------------------------------------------------

        encoder_layer = nn.TransformerEncoderLayer(
            d_model=embedding_dim,
            nhead=num_heads,
            dim_feedforward=feed_forward_dim,
            dropout=dropout,
            batch_first=True,
            activation="gelu"
        )

        self.transformer_encoder = nn.TransformerEncoder(
            encoder_layer,
            num_layers=num_layers
        )

        # -------------------------------------------------
        # NORMALIZATION
        # -------------------------------------------------

        self.layer_norm = nn.LayerNorm(
            embedding_dim
        )

        # -------------------------------------------------
        # CLASSIFIER
        # -------------------------------------------------

        self.dropout = nn.Dropout(
            dropout
        )

        self.classifier = nn.Linear(
            embedding_dim,
            num_classes
        )


    # =====================================================
    # FORWARD
    # =====================================================

    def forward(
        self,
        input_ids,
        attention_mask
    ):

        batch_size, sequence_length = input_ids.shape

        # -------------------------------------------------
        # POSITION IDs
        # -------------------------------------------------

        position_ids = torch.arange(
            sequence_length,
            device=input_ids.device
        )

        position_ids = position_ids.unsqueeze(0)

        position_ids = position_ids.expand(
            batch_size,
            sequence_length
        )

        # -------------------------------------------------
        # EMBEDDINGS
        # -------------------------------------------------

        token_embeddings = self.embedding(
            input_ids
        )

        position_embeddings = self.position_embedding(
            position_ids
        )

        x = (
            token_embeddings
            + position_embeddings
        )

        x = self.embedding_dropout(x)

        # -------------------------------------------------
        # PADDING MASK
        # -------------------------------------------------

        padding_mask = (
            attention_mask == 0
        )

        # -------------------------------------------------
        # TRANSFORMER
        # -------------------------------------------------

        x = self.transformer_encoder(
            x,
            src_key_padding_mask=padding_mask
        )

        x = self.layer_norm(x)

        # -------------------------------------------------
        # MASKED MEAN POOLING
        # -------------------------------------------------

        mask = attention_mask.unsqueeze(
            -1
        ).float()

        x = x * mask

        summed = x.sum(
            dim=1
        )

        count = mask.sum(
            dim=1
        ).clamp(
            min=1e-9
        )

        pooled = summed / count

        # -------------------------------------------------
        # CLASSIFICATION
        # -------------------------------------------------

        pooled = self.dropout(
            pooled
        )

        logits = self.classifier(
            pooled
        )

        return logits


# =========================================================
# TEST MODEL
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNA TRANSFORMER MODEL - VERSION 3")
    print("=" * 60)

    vocab_size = 4471

    model = DNATransformerClassifier(
        vocab_size=vocab_size
    )

    print("\nModel created successfully.")

    total_parameters = sum(
        parameter.numel()
        for parameter in model.parameters()
    )

    print("\nNumber of parameters:")

    print(total_parameters)

    # -----------------------------------------------------
    # TEST INPUT
    # -----------------------------------------------------

    input_ids = torch.randint(
        0,
        vocab_size,
        (2, 1019)
    )

    attention_mask = torch.ones(
        2,
        1019,
        dtype=torch.long
    )

    # -----------------------------------------------------
    # FORWARD PASS
    # -----------------------------------------------------

    output = model(
        input_ids,
        attention_mask
    )

    print("\nInput shape:")

    print(input_ids.shape)

    print("\nOutput shape:")

    print(output.shape)

    print("\nExpected output shape:")

    print("(batch_size, 7)")