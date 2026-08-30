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

    # ============================================================
    # NORMALIZE PATH
    # ============================================================

    def _normalize_path(
        self,
        file_path
    ):

        return str(
            file_path or ""
        ).replace(
            "\\",
            "/"
        ).lower()

    # ============================================================
    # CHECK TEST / EXAMPLE FILE
    # ============================================================

    def _is_test_or_example(
        self,
        result
    ):

        payload = (
            result.payload or {}
        )

        file_path = self._normalize_path(
            payload.get(
                "file_path",
                ""
            )
        )

        return (
            "/tests/" in file_path
            or "/test/" in file_path
            or "/examples/" in file_path
            or "/example/" in file_path
        )

    # ============================================================
    # CHECK DEFINITION QUESTION
    # ============================================================

    def _is_definition_question(
        self,
        question
    ):

        question = question.lower()

        keywords = [

            "inherit",
            "inherits",
            "inheritance",

            "parent class",
            "base class",

            "extends",

            "where is",
            "defined",

            "definition",

            "class",

            "implementation",

            "implemented",

            "constructor",

            "init",

            "initialization"
        ]

        return any(
            keyword in question
            for keyword in keywords
        )

    # ============================================================
    # CHECK PRODUCTION SOURCE
    # ============================================================

    def _is_production_source(
        self,
        result
    ):

        return not self._is_test_or_example(
            result
        )

    # ============================================================
    # RERANK RESULTS
    # ============================================================

    def _rerank_results(
        self,
        question,
        results
    ):

        if not results:

            return []

        definition_question = (
            self._is_definition_question(
                question
            )
        )

        reranked = []

        for result in results:

            payload = (
                result.payload or {}
            )

            file_path = self._normalize_path(
                payload.get(
                    "file_path",
                    ""
                )
            )

            name = str(
                payload.get(
                    "name",
                    ""
                )
            ).lower()

            score = float(
                result.score
            )

            # ====================================================
            # PRODUCTION SOURCE BOOST
            # ====================================================

            if definition_question:

                if self._is_production_source(
                    result
                ):

                    score += 0.15

                else:

                    score -= 0.15

            # ====================================================
            # EXACT SYMBOL MATCH
            # ====================================================

            question_lower = (
                question.lower()
            )

            if name and name in question_lower:

                score += 0.05

            # ====================================================
            # SOURCE DIRECTORY BOOST
            # ====================================================

            if "/src/" in file_path:

                score += 0.05

            # ====================================================
            # SAVE SCORE
            # ====================================================

            result._repomind_score = score

            reranked.append(
                result
            )

        # ========================================================
        # SORT
        # ========================================================

        reranked.sort(
            key=lambda result:
            result._repomind_score,
            reverse=True
        )

        return reranked

    # ============================================================
    # ASK
    # ============================================================

    def ask(
        self,
        question,
        limit=3
    ):

        # ========================================================
        # 1. EMBED QUESTION
        # ========================================================

        query_embedding = (
            self.embedding_model.embed_text(
                question
            )
        )

        # ========================================================
        # 2. RETRIEVE MANY CANDIDATES
        #
        # IMPORTANT:
        # Do NOT retrieve only 3.
        #
        # We retrieve 15 so that relevant production code
        # isn't lost before filtering tests/examples.
        # ========================================================

        results = (
            self.vector_store.search(
                query_embedding,
                limit=15
            )
        )

        # ========================================================
        # 3. REMOVE WEAK RESULTS
        # ========================================================

        results = [
            result
            for result in results
            if result.score >= 0.30
        ]

        # ========================================================
        # 4. RERANK
        # ========================================================

        results = self._rerank_results(
            question,
            results
        )

        # ========================================================
        # 5. KEEP BEST RESULTS
        # ========================================================

        results = results[:limit]

        # ========================================================
        # 6. BUILD PROMPT
        # ========================================================

        prompt = (
            self.prompt_builder.build_prompt(
                question,
                results
            )
        )

        # ========================================================
        # 7. GENERATE ANSWER
        # ========================================================

        answer = self.llm.generate(
            prompt
        )

        return answer, results

    # ============================================================
    # CLOSE
    # ============================================================

    def close(self):

        self.vector_store.close()