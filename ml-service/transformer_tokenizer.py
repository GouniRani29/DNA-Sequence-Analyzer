from preprocess import load_human_data, clean_sequence, create_kmers


# =========================================================
# DNA TOKENIZER
# =========================================================

class DNATokenizer:

    def __init__(self, k=6):
        self.k = k

        # Special tokens
        self.PAD_TOKEN = "<PAD>"
        self.UNK_TOKEN = "<UNK>"

        self.token_to_id = {
            self.PAD_TOKEN: 0,
            self.UNK_TOKEN: 1
        }

        self.id_to_token = {
            0: self.PAD_TOKEN,
            1: self.UNK_TOKEN
        }

        self.build_vocabulary()

    # =====================================================
    # BUILD 6-MER VOCABULARY
    # =====================================================

    def build_vocabulary(self):

        data = load_human_data()

        vocabulary = set()

        for sequence in data["sequence"]:

            sequence = clean_sequence(sequence)

            if not sequence:
                continue

            kmers = create_kmers(
                sequence,
                self.k
            )

            for kmer in kmers:
                vocabulary.add(kmer)

        for kmer in sorted(vocabulary):

            token_id = len(self.token_to_id)

            self.token_to_id[kmer] = token_id
            self.id_to_token[token_id] = kmer

    # =====================================================
    # ENCODE
    # =====================================================

    def encode(self, sequence):

        sequence = clean_sequence(sequence)

        kmers = create_kmers(
            sequence,
            self.k
        )

        token_ids = []

        for kmer in kmers:

            token_id = self.token_to_id.get(
                kmer,
                self.token_to_id[self.UNK_TOKEN]
            )

            token_ids.append(token_id)

        return token_ids

    # =====================================================
    # DECODE
    # =====================================================

    def decode(self, token_ids):

        tokens = []

        for token_id in token_ids:

            token = self.id_to_token.get(
                token_id,
                self.UNK_TOKEN
            )

            tokens.append(token)

        return tokens


# =========================================================
# TEST
# =========================================================

if __name__ == "__main__":

    print("=" * 60)
    print("DNA TRANSFORMER TOKENIZER")
    print("=" * 60)

    tokenizer = DNATokenizer(k=6)

    print("\nVocabulary size:")
    print(len(tokenizer.token_to_id))

    data = load_human_data()

    sample_sequence = data.iloc[0]["sequence"]

    print("\nOriginal DNA:")
    print(sample_sequence[:100])

    token_ids = tokenizer.encode(
        sample_sequence
    )

    print("\nFirst 20 token IDs:")
    print(token_ids[:20])

    decoded_tokens = tokenizer.decode(
        token_ids[:20]
    )

    print("\nFirst 20 tokens:")
    print(decoded_tokens)