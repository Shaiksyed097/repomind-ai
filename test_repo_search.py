from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore


# --------------------------------
# Initialize
# --------------------------------

embedding_model = CodeEmbeddingModel()

vector_store = QdrantVectorStore()


# --------------------------------
# Ask question
# --------------------------------

query = input(
    "\nAsk something about Flask: "
)


# --------------------------------
# Create query embedding
# --------------------------------

query_embedding = (
    embedding_model.embed_text(query)
)


# --------------------------------
# Search Qdrant
# --------------------------------

results = vector_store.search(
    query_embedding,
    limit=5
)


# --------------------------------
# Display results
# --------------------------------

print("\n" + "=" * 60)
print("FLASK SEARCH RESULTS")
print("=" * 60)


for index, result in enumerate(
    results,
    start=1
):

    payload = result.payload

    print("\n" + "-" * 60)

    print(
        f"Result {index}"
    )

    print(
        f"Score: {result.score:.4f}"
    )

    print(
        f"File: {payload.get('file_path')}"
    )

    print(
        f"Function: {payload.get('name')}"
    )

    print(
        f"Lines: "
        f"{payload.get('start_line')}-"
        f"{payload.get('end_line')}"
    )

    print("\nCode:")

    print(
        payload.get("content")
    )


vector_store.close()