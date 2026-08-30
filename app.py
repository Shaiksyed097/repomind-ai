import os
import streamlit as st

from backend.ingestion.repo_loader import RepoLoader
from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker
from backend.vectorstore.qdrant_store import QdrantVectorStore
from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.rag.rag_pipeline import RAGPipeline


# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="RepoMind AI",
    page_icon="🧠",
    layout="wide"
)


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        font-size: 48px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .subtitle {
        font-size: 18px;
        color: #9ca3af;
        margin-bottom: 35px;
    }

    .step-card {
        background: #16191f;
        border: 1px solid #30343b;
        border-radius: 12px;
        padding: 20px;
        min-height: 160px;
    }

    .step-number {
        color: #4da3ff;
        font-weight: 700;
        font-size: 14px;
    }

    .step-title {
        font-size: 22px;
        font-weight: 700;
        margin-top: 10px;
    }

    .step-description {
        color: #9ca3af;
        margin-top: 10px;
        line-height: 1.5;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# SESSION STATE
# ============================================================

if "index_checked" not in st.session_state:
    st.session_state["index_checked"] = False

if "indexed" not in st.session_state:
    st.session_state["indexed"] = False

if "existing_index" not in st.session_state:
    st.session_state["existing_index"] = False

if "chunks" not in st.session_state:
    st.session_state["chunks"] = 0

if "source_files" not in st.session_state:
    st.session_state["source_files"] = 0

if "indexed_repo_name" not in st.session_state:
    st.session_state["indexed_repo_name"] = "Unknown"

if "repository_path" not in st.session_state:
    st.session_state["repository_path"] = None

if "repository_url" not in st.session_state:
    st.session_state["repository_url"] = ""

if "answer" not in st.session_state:
    st.session_state["answer"] = None

if "results" not in st.session_state:
    st.session_state["results"] = []


# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🧠 RepoMind AI</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'AI-powered assistant for understanding GitHub repositories.'
    '</div>',
    unsafe_allow_html=True
)


# ============================================================
# RESTORE EXISTING INDEX
# ============================================================

def restore_existing_index():

    try:

        store = QdrantVectorStore()

        collections = store.client.get_collections()

        collection_names = {
            collection.name
            for collection in collections.collections
        }

        if "repomind_code" not in collection_names:

            store.close()

            return

        # --------------------------------------------------------
        # Count chunks
        # --------------------------------------------------------

        count_result = store.client.count(
            collection_name="repomind_code",
            exact=True
        )

        # --------------------------------------------------------
        # Get repository name and Python file count
        # --------------------------------------------------------

        repo_name = None

        python_files = set()

        try:

            offset = None

            while True:

                points, offset = store.client.scroll(
                    collection_name="repomind_code",
                    limit=256,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )

                for point in points:

                    payload = point.payload or {}

                    file_path = payload.get(
                        "file_path",
                        ""
                    )

                    if file_path:

                        python_files.add(
                            os.path.normpath(
                                str(file_path)
                            )
                        )

                        normalized_path = (
                            str(file_path)
                            .replace("\\", "/")
                        )

                        parts = normalized_path.split("/")

                        if "repos" in parts:

                            repo_index = parts.index(
                                "repos"
                            )

                            if repo_index + 1 < len(parts):

                                repo_name = parts[
                                    repo_index + 1
                                ]

                if offset is None:

                    break

        except Exception:

            pass

        store.close()

        # --------------------------------------------------------
        # Save state
        # --------------------------------------------------------

        st.session_state["indexed"] = True

        st.session_state["existing_index"] = True

        st.session_state["chunks"] = (
            count_result.count
        )

        st.session_state["source_files"] = (
            len(python_files)
        )

        if repo_name:

            st.session_state[
                "indexed_repo_name"
            ] = repo_name

    except Exception:

        pass


# ============================================================
# CHECK INDEX ONLY ONCE
# ============================================================

if not st.session_state["index_checked"]:

    restore_existing_index()

    st.session_state["index_checked"] = True


# ============================================================
# HOW IT WORKS
# ============================================================

st.subheader(
    "⚙️ How RepoMind Works"
)


steps = [

    (
        "STEP 1",
        "📦 Clone",
        "Download the GitHub repository."
    ),

    (
        "STEP 2",
        "🔎 Scan",
        "Find supported Python source files."
    ),

    (
        "STEP 3",
        "🌳 Parse",
        "Understand functions, methods and classes."
    ),

    (
        "STEP 4",
        "🧩 Chunk",
        "Split code into meaningful context-aware chunks."
    ),

    (
        "STEP 5",
        "🧠 Index",
        "Create embeddings and store them in Qdrant."
    )

]


cols = st.columns(5)


for col, step in zip(
    cols,
    steps
):

    number, title, description = step

    with col:

        st.markdown(
            f"""
            <div class="step-card">

                <div class="step-number">
                    {number}
                </div>

                <div class="step-title">
                    {title}
                </div>

                <div class="step-description">
                    {description}
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


st.divider()


# ============================================================
# REPOSITORY SECTION
# ============================================================

st.subheader(
    "📦 Repository"
)


repository_url = st.text_input(
    "GitHub Repository URL",
    value=st.session_state.get(
        "repository_url",
        ""
    ),
    placeholder="https://github.com/pallets/flask"
)


# ============================================================
# EXISTING INDEX MESSAGE
# ============================================================

if st.session_state.get(
    "existing_index",
    False
):

    repo_name = st.session_state.get(
        "indexed_repo_name",
        "repository"
    )

    chunk_count = st.session_state.get(
        "chunks",
        0
    )

    source_file_count = st.session_state.get(
        "source_files",
        0
    )

    st.success(
        f"✅ Existing index detected: "
        f"**{repo_name}** "
        f"({chunk_count} chunks, "
        f"{source_file_count} Python files). "
        f"You can ask questions without re-indexing."
    )


# ============================================================
# INDEX REPOSITORY
# ============================================================

if st.button(
    "🚀 Index Repository",
    type="primary"
):

    if not repository_url.strip():

        st.warning(
            "Please enter a GitHub repository URL."
        )

    else:

        try:

            progress = st.progress(0)

            status = st.empty()

            # ==================================================
            # STEP 1 — CLONE
            # ==================================================

            status.info(
                "📥 Step 1/5 — Cloning repository..."
            )

            loader = RepoLoader(
                base_path=r"C:\RepoMindData\repos"
            )

            repository_path = (
                loader.clone_repository(
                    repository_url.strip()
                )
            )

            progress.progress(15)


            # ==================================================
            # STEP 2 — SCAN
            # ==================================================

            status.info(
                "🔎 Step 2/5 — Scanning Python files..."
            )

            scanner = FileScanner(
                repository_path
            )

            source_files = (
                scanner.get_source_files()
            )

            if not source_files:

                st.error(
                    "No supported Python files were found."
                )

                st.stop()

            progress.progress(30)


            # ==================================================
            # INITIALIZE PARSER / CHUNKER
            # ==================================================

            parser = PythonCodeParser()

            chunker = CodeChunker()

            all_chunks = []


            # ==================================================
            # STEP 3 + 4 — PARSE AND CHUNK
            # ==================================================

            total_files = len(
                source_files
            )

            for index, file_path in enumerate(
                source_files,
                start=1
            ):

                status.info(
                    f"🌳 Step 3/5 — Processing "
                    f"{index}/{total_files}: "
                    f"{os.path.basename(file_path)}"
                )

                try:

                    tree, source_code = (
                        parser.parse_file(
                            file_path
                        )
                    )

                    functions = (
                        parser.extract_functions(
                            tree,
                            source_code
                        )
                    )

                    classes = (
                        parser.extract_classes(
                            tree,
                            source_code
                        )
                    )

                    chunks = (
                        chunker.create_chunks(
                            file_path,
                            functions,
                            classes
                        )
                    )

                    all_chunks.extend(
                        chunks
                    )

                except Exception as file_error:

                    st.warning(
                        f"Could not process "
                        f"{file_path}: "
                        f"{file_error}"
                    )

                progress.progress(
                    30
                    + int(
                        (index / total_files)
                        * 35
                    )
                )


            # ==================================================
            # STEP 5 — EMBEDDINGS
            # ==================================================

            status.info(
                f"🧠 Step 5/5 — Creating embeddings "
                f"for {len(all_chunks)} chunks..."
            )

            embedding_model = (
                CodeEmbeddingModel()
            )

            embeddings = (
                embedding_model.embed_chunks(
                    all_chunks
                )
            )

            progress.progress(80)


            # ==================================================
            # STORE IN QDRANT
            # ==================================================

            status.info(
                "🗄️ Storing code in Qdrant..."
            )

            vector_store = (
                QdrantVectorStore()
            )

            vector_store.add_chunks(
                all_chunks,
                embeddings
            )

            vector_store.close()

            progress.progress(100)


            # ==================================================
            # SAVE STATE
            # ==================================================

            st.session_state[
                "repository_path"
            ] = repository_path

            st.session_state[
                "repository_url"
            ] = repository_url.strip()

            st.session_state[
                "indexed"
            ] = True

            st.session_state[
                "existing_index"
            ] = True

            st.session_state[
                "index_checked"
            ] = True

            st.session_state[
                "source_files"
            ] = len(
                source_files
            )

            st.session_state[
                "chunks"
            ] = len(
                all_chunks
            )

            st.session_state[
                "indexed_repo_name"
            ] = os.path.basename(
                repository_path
            )


            # ==================================================
            # SUCCESS
            # ==================================================

            status.success(
                "✅ Repository indexed successfully!"
            )

            st.success(
                f"Indexed {len(source_files)} "
                f"Python files and "
                f"{len(all_chunks)} code chunks."
            )

        except Exception as error:

            st.error(
                f"❌ Indexing failed: {error}"
            )


# ============================================================
# REPOSITORY OVERVIEW
# ============================================================

if st.session_state.get(
    "indexed",
    False
):

    st.divider()

    st.subheader(
        "📊 Repository Overview"
    )

    repo_name = st.session_state.get(
        "indexed_repo_name",
        "Unknown"
    )

    source_file_count = st.session_state.get(
        "source_files",
        0
    )

    chunk_count = st.session_state.get(
        "chunks",
        0
    )


    # --------------------------------------------------------
    # Dashboard metrics
    # --------------------------------------------------------

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(
            "📁 Repository",
            repo_name
        )

    with col2:

        st.metric(
            "🐍 Python Files",
            source_file_count
        )

    with col3:

        st.metric(
            "🧩 Code Chunks",
            chunk_count
        )

    with col4:

        st.metric(
            "📐 Vector Size",
            "384"
        )


    st.write("")

    st.write(
        "**Vector Store:** Qdrant"
    )

    st.write(
        "**Embedding Model:** "
        "`all-MiniLM-L6-v2`"
    )

    st.write(
        "**Similarity:** Cosine Similarity"
    )

    st.write(
        "**Index Status:** 🟢 Ready"
    )


# ============================================================
# ASK REPOMIND
# ============================================================

st.divider()

st.subheader(
    "💬 Ask RepoMind"
)

st.caption(
    "Ask a question about the indexed repository."
)


question = st.text_input(
    "Ask a question about the repository",
    placeholder=(
        "Where is the Flask application class defined?"
    ),
    key="repo_question"
)


# ============================================================
# ASK BUTTON
# ============================================================

if st.button(
    "🔎 Ask RepoMind"
):

    if not st.session_state.get(
        "indexed",
        False
    ):

        st.warning(
            "Please index a repository first."
        )

    elif not question.strip():

        st.warning(
            "Please enter a question."
        )

    else:

        try:

            with st.spinner(
                "Searching repository and generating answer..."
            ):

                rag_pipeline = (
                    RAGPipeline()
                )

                answer, results = (
                    rag_pipeline.ask(
                        question.strip(),
                        limit=3
                    )
                )

                rag_pipeline.close()


            st.session_state[
                "answer"
            ] = answer

            st.session_state[
                "results"
            ] = results


        except Exception as error:

            st.error(
                f"❌ Error while answering: {error}"
            )


# ============================================================
# DISPLAY ANSWER
# ============================================================

if st.session_state.get(
    "answer"
):

    st.divider()

    st.subheader(
        "🤖 RepoMind Answer"
    )

    st.markdown(
        st.session_state["answer"]
    )


    # ========================================================
    # SOURCES
    # ========================================================

    results = st.session_state.get(
        "results",
        []
    )


    if results:

        st.subheader(
            "📚 Sources"
        )


        for index, result in enumerate(
            results,
            start=1
        ):

            payload = (
                result.payload or {}
            )

            score = getattr(
                result,
                "score",
                None
            )

            file_path = payload.get(
                "file_path",
                "Unknown"
            )

            name = payload.get(
                "name",
                "Unknown"
            )

            item_type = payload.get(
                "type",
                "Unknown"
            )

            start_line = payload.get(
                "start_line",
                "?"
            )

            end_line = payload.get(
                "end_line",
                "?"
            )

            # ------------------------------------------------
            # Source title
            # ------------------------------------------------

            if score is not None:

                source_title = (
                    f"Source {index}: "
                    f"{name} — {score:.3f}"
                )

            else:

                source_title = (
                    f"Source {index}: "
                    f"{name}"
                )


            with st.expander(
                source_title
            ):

                st.write(
                    f"**Type:** `{item_type}`"
                )

                st.write(
                    f"**File:** "
                    f"`{file_path}`"
                )

                st.write(
                    f"**Lines:** "
                    f"{start_line}-{end_line}"
                )

                if score is not None:

                    st.write(
                        f"**Similarity:** "
                        f"{score:.4f}"
                    )

                # --------------------------------------------
                # Class information
                # --------------------------------------------

                class_name = payload.get(
                    "class_name"
                )

                if class_name:

                    st.write(
                        f"**Class:** "
                        f"`{class_name}`"
                    )

                # --------------------------------------------
                # Code
                # --------------------------------------------

                st.code(
                    payload.get(
                        "content",
                        ""
                    ),
                    language="python"
                )


    else:

        st.info(
            "No sufficiently relevant "
            "code chunks were found."
        )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "RepoMind AI • GitHub Repository RAG Assistant"
)