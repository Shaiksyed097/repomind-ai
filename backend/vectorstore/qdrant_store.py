from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct
)
import hashlib


class QdrantVectorStore:

    def __init__(
        self,
        collection_name="repomind_code",
        vector_size=384,
        storage_path="data/qdrant"
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            path=storage_path
        )

        self._create_collection(
            vector_size
        )

    def _create_collection(self, vector_size):

        collections = self.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if self.collection_name not in collection_names:

            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(
                    size=vector_size,
                    distance=Distance.COSINE
                )
            )

            print(
                f"Created collection: "
                f"{self.collection_name}"
            )

    def add_chunks(
        self,
        chunks,
        embeddings
    ):

        points = []

        for chunk, embedding in zip(
            chunks,
            embeddings
        ):

            metadata = chunk["metadata"]

            unique_key = (
                f"{metadata['file_path']}:"
                f"{metadata['name']}:"
                f"{metadata['start_line']}:"
                f"{metadata['end_line']}"
            )

            point_id = hashlib.md5(
                unique_key.encode("utf-8")
            ).hexdigest()

            point = PointStruct(
                id=point_id,
                vector=embedding,
                payload={
                    "content": chunk["content"],
                    **metadata
                }
            )

            points.append(point)

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(
            f"Inserted/updated {len(points)} "
            f"chunks in Qdrant."
        )

    def search(
        self,
        query_embedding,
        limit=3
    ):

        results = self.client.query_points(
            collection_name=self.collection_name,
            query=query_embedding,
            limit=limit,
            with_payload=True
        )

        return results.points

    def close(self):

        self.client.close()