from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore


# --------------------------------
# 1. Initialize components
# --------------------------------

embedding_model = CodeEmbeddingModel()

vector_store = QdrantVectorStore()


# --------------------------------
# 2. Get user query
# --------------------------------

query = input(
    "\nAsk RepoMind something about the code: "
)


# --------------------------------
# 3. Convert query to embedding
# --------------------------------

query_embedding = embedding_model.embed_text(
    query
)


# --------------------------------
# 4. Search Qdrant
# --------------------------------

results = vector_store.search(
    query_embedding,
    limit=3
)


# --------------------------------
# 5. Display results
# --------------------------------

print("\n" + "=" * 60)
print("SEARCH RESULTS")
print("=" * 60)

for index, result in enumerate(results):

    payload = result.payload

    print("\n" + "-" * 60)

    print(
        f"Result {index + 1}"
    )

    print(
        f"Score: {result.score:.4f}"
    )

    print(
        f"File: {payload['file_path']}"
    )

    print(
        f"Function: {payload['name']}"
    )

    print(
        f"Lines: "
        f"{payload['start_line']}-"
        f"{payload['end_line']}"
    )

    print("\nCode:")

    print(payload["content"])


# --------------------------------
# 6. Close Qdrant
# --------------------------------

vector_store.close()
