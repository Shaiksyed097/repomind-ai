from sentence_transformers import SentenceTransformer


class CodeEmbeddingModel:

    def __init__(
        self,
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    ):

        self.model_name = model_name

        self.model = None

    # ============================================================
    # LOAD MODEL
    # ============================================================

    def _load_model(self):

        if self.model is None:

            print(
                "Loading embedding model..."
            )

            self.model = SentenceTransformer(
                self.model_name
            )

            print(
                "Embedding model loaded."
            )

    # ============================================================
    # EMBED SINGLE TEXT
    # ============================================================

    def embed_text(
        self,
        text
    ):

        self._load_model()

        embedding = self.model.encode(
            text,
            normalize_embeddings=True
        )

        return embedding.tolist()

    # ============================================================
    # EMBED CHUNKS
    # ============================================================

    def embed_chunks(
        self,
        chunks
    ):

        self._load_model()

        texts = [
            chunk["content"]
            for chunk in chunks
        ]

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True
        )

        return embeddings.tolist()