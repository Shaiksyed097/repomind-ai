from backend.vectorstore.qdrant_store import QdrantVectorStore


store = QdrantVectorStore()

result = store.client.count(
    collection_name=store.collection_name,
    exact=True
)

print("\nTotal points in Qdrant:", result.count)

store.close()