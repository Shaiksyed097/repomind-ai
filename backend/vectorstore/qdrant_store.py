from qdrant_client import QdrantClient
from qdrant_client.models import (
    Distance,
    VectorParams,
    PointStruct,
    Filter,
    FieldCondition,
    MatchValue
)

import hashlib
import os


class QdrantVectorStore:

    def __init__(
        self,
        collection_name="repomind_code",
        vector_size=384,
        storage_path=r"C:\RepoMindData\qdrant"
    ):

        self.collection_name = collection_name

        self.client = QdrantClient(
            path=storage_path
        )

        self._create_collection(
            vector_size
        )

    # ============================================================
    # CREATE COLLECTION
    # ============================================================

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

    # ============================================================
    # REPOSITORY ID
    # ============================================================

    def _get_repo_id(self, file_path):

        normalized_path = str(
            file_path
        ).replace("\\", "/")

        parts = normalized_path.split("/")

        if "repos" in parts:

            repo_index = parts.index("repos")

            if repo_index + 1 < len(parts):

                return parts[
                    repo_index + 1
                ]

        # Fallback
        return "unknown_repo"

    # ============================================================
    # ADD CHUNKS
    # ============================================================

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

            file_path = metadata["file_path"]

            repo_id = self._get_repo_id(
                file_path
            )

            # ----------------------------------------------------
            # Unique ID
            # ----------------------------------------------------

            unique_key = (
                f"{repo_id}:"
                f"{file_path}:"
                f"{metadata['name']}:"
                f"{metadata['start_line']}:"
                f"{metadata['end_line']}"
            )

            point_id = hashlib.md5(
                unique_key.encode("utf-8")
            ).hexdigest()

            # ----------------------------------------------------
            # Store point
            # ----------------------------------------------------

            point = PointStruct(
                id=point_id,

                vector=embedding,

                payload={
                    "repo_id": repo_id,
                    "content": chunk["content"],
                    **metadata
                }
            )

            points.append(point)

        # --------------------------------------------------------
        # Insert into Qdrant
        # --------------------------------------------------------

        self.client.upsert(
            collection_name=self.collection_name,
            points=points
        )

        print(
            f"Inserted/updated "
            f"{len(points)} chunks in Qdrant."
        )

    # ============================================================
    # SEARCH
    # ============================================================

    def search(
        self,
        query_embedding,
        limit=3,
        repo_id=None
    ):

        # --------------------------------------------------------
        # Repository filter
        # --------------------------------------------------------

        query_filter = None

        if repo_id:

            query_filter = Filter(
                must=[
                    FieldCondition(
                        key="repo_id",
                        match=MatchValue(
                            value=repo_id
                        )
                    )
                ]
            )

        # --------------------------------------------------------
        # Search
        # --------------------------------------------------------

        results = self.client.query_points(
            collection_name=self.collection_name,

            query=query_embedding,

            query_filter=query_filter,

            limit=limit,

            with_payload=True
        )

        return results.points

    # ============================================================
    # GET REPOSITORY CHUNK COUNT
    # ============================================================

    def count_repository(
        self,
        repo_id
    ):

        result = self.client.count(
            collection_name=self.collection_name,

            count_filter=Filter(
                must=[
                    FieldCondition(
                        key="repo_id",
                        match=MatchValue(
                            value=repo_id
                        )
                    )
                ]
            ),

            exact=True
        )

        return result.count

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):

        self.client.close()