from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore
from backend.llm.mistral_model import MistralModel
from backend.rag.rag_prompt import RAGPrompt


class RAGPipeline:

    def __init__(self):

        self.embedding_model = CodeEmbeddingModel()

        self.vector_store = QdrantVectorStore()

        self.llm = MistralModel()

        self.prompt_builder = RAGPrompt()

    def ask(self, question, limit=3):

        # --------------------------------
        # 1. Convert question to embedding
        # --------------------------------

        query_embedding = (
            self.embedding_model.embed_text(
                question
            )
        )

        # --------------------------------
        # 2. Search Qdrant
        # --------------------------------

        results = self.vector_store.search(
            query_embedding,
            limit=limit
        )

        # --------------------------------
        # 3. Filter weak results
        # --------------------------------

        results = [
            result
            for result in results
            if result.score >= 0.30
        ]

        # --------------------------------
        # 4. Build RAG prompt
        # --------------------------------

        prompt = self.prompt_builder.build_prompt(
            question,
            results
        )

        # --------------------------------
        # 5. Generate answer
        # --------------------------------

        answer = self.llm.generate(
            prompt
        )

        return answer, results

    def close(self):

        self.vector_store.close()