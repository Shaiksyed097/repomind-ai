from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore


# ============================================================
# TEST QUESTION
# ============================================================

question = "What does the Flask class inherit from?"


print("=" * 60)
print("REPOMIND QDRANT SEARCH TEST")
print("=" * 60)

print()
print("Question:")
print(question)


# ============================================================
# LOAD EMBEDDING MODEL
# ============================================================

print()
print("Loading embedding model...")

embedding_model = CodeEmbeddingModel()

query_embedding = (
    embedding_model.embed_text(
        question
    )
)

print(
    f"Embedding dimensions: "
    f"{len(query_embedding)}"
)


# ============================================================
# CONNECT TO QDRANT
# ============================================================

print()
print("Connecting to Qdrant...")

vector_store = QdrantVectorStore()


# ============================================================
# SEARCH
# ============================================================

print()
print("Searching Qdrant...")

results = vector_store.search(
    query_embedding,
    limit=5
)


# ============================================================
# DISPLAY RESULTS
# ============================================================

print()
print("=" * 60)
print("SEARCH RESULTS")
print("=" * 60)


if not results:

    print()
    print("❌ No results returned.")

else:

    for index, result in enumerate(
        results,
        start=1
    ):

        payload = (
            result.payload or {}
        )

        print()
        print("-" * 60)

        print(
            f"RESULT {index}"
        )

        print("-" * 60)

        print(
            f"Score: "
            f"{result.score:.4f}"
        )

        print(
            f"Name: "
            f"{payload.get('name')}"
        )

        print(
            f"Type: "
            f"{payload.get('type')}"
        )

        print(
            f"File: "
            f"{payload.get('file_path')}"
        )

        print(
            f"Class: "
            f"{payload.get('class_name')}"
        )

        print(
            f"Lines: "
            f"{payload.get('start_line')}-"
            f"{payload.get('end_line')}"
        )

        print()
        print("CONTENT:")
        print("-" * 60)

        content = payload.get(
            "content",
            ""
        )

        # Print only first 1000 characters
        # so the terminal doesn't become huge.

        print(
            content[:1000]
        )

        if len(content) > 1000:

            print()
            print(
                "... [content truncated]"
            )


# ============================================================
# CLEANUP
# ============================================================

vector_store.close()


print()
print("=" * 60)
print("QDRANT TEST COMPLETED")
print("=" * 60)