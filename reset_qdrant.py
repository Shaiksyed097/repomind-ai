from backend.vectorstore.qdrant_store import QdrantVectorStore


store = QdrantVectorStore()

store.client.delete_collection(
    collection_name=store.collection_name
)

store.close()

print("Qdrant collection deleted successfully!")