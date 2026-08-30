import os

from backend.ingestion.repo_loader import RepoLoader
from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker
from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore


REPOSITORY_URL = "https://github.com/pallets/flask"


print("=" * 70)
print("REPOMIND DIRECT RE-INDEX TEST")
print("=" * 70)


# ============================================================
# 1. CLONE
# ============================================================

print("\n[1/5] Loading repository...")

loader = RepoLoader(
    base_path=r"C:\RepoMindData\repos"
)

repository_path = loader.clone_repository(
    REPOSITORY_URL
)

print(
    f"Repository path:\n{repository_path}"
)


# ============================================================
# 2. SCAN
# ============================================================

print("\n[2/5] Scanning Python files...")

scanner = FileScanner(
    repository_path
)

source_files = scanner.get_source_files()

print(
    f"Python files found: {len(source_files)}"
)


# ============================================================
# 3. PARSE + CHUNK
# ============================================================

print("\n[3/5] Parsing and chunking...")

parser = PythonCodeParser()

chunker = CodeChunker()

all_chunks = []


for index, file_path in enumerate(
    source_files,
    start=1
):

    print(
        f"[{index}/{len(source_files)}] "
        f"{file_path}"
    )

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


print(
    f"\nTotal chunks: {len(all_chunks)}"
)


# ============================================================
# 4. VERIFY FLASK CHUNK BEFORE QDRANT
# ============================================================

print("\n[4/5] Verifying Flask class chunk...")

flask_chunks = [

    chunk
    for chunk in all_chunks

    if (
        chunk["metadata"].get("name")
        == "Flask"
        and
        chunk["metadata"].get("type")
        == "class"
        and
        "/src/flask/app.py"
        in chunk["metadata"].get(
            "file_path",
            ""
        ).replace(
            "\\",
            "/"
        )
    )

]


if not flask_chunks:

    print(
        "\n❌ Flask class chunk was NOT found."
    )

    raise SystemExit(1)


flask_chunk = flask_chunks[0]


print("\nFlask chunk found!")

print(
    f"File: "
    f"{flask_chunk['metadata']['file_path']}"
)

print(
    f"Lines: "
    f"{flask_chunk['metadata']['start_line']}-"
    f"{flask_chunk['metadata']['end_line']}"
)

print("\nFirst 500 characters:")
print("-" * 70)

print(
    flask_chunk["content"][:500]
)

print("-" * 70)


if "class Flask(App)" not in (
    flask_chunk["content"]
):

    print(
        "\n❌ ERROR:"
    )

    print(
        "The Flask class declaration is missing "
        "from the chunk."
    )

    raise SystemExit(1)


print(
    "\n✅ Flask chunk contains:"
)

print(
    "class Flask(App):"
)


# ============================================================
# 5. EMBEDDINGS + QDRANT
# ============================================================

print("\n[5/5] Creating embeddings...")

embedding_model = (
    CodeEmbeddingModel()
)

embeddings = (
    embedding_model.embed_chunks(
        all_chunks
    )
)

print(
    f"Generated embeddings: "
    f"{len(embeddings)}"
)

print(
    f"Embedding dimensions: "
    f"{len(embeddings[0])}"
)


print("\nStoring chunks in Qdrant...")

vector_store = (
    QdrantVectorStore()
)

vector_store.add_chunks(
    all_chunks,
    embeddings
)


# ============================================================
# IMMEDIATELY VERIFY QDRANT
# ============================================================

print(
    "\nVerifying Flask chunk directly "
    "from Qdrant..."
)

query_embedding = (
    embedding_model.embed_text(
        "What does the Flask class inherit from?"
    )
)

results = vector_store.search(
    query_embedding,
    limit=5
)


print("\n" + "=" * 70)
print("QDRANT VERIFICATION")
print("=" * 70)


for index, result in enumerate(
    results,
    start=1
):

    payload = (
        result.payload or {}
    )

    print(
        f"\nRESULT {index}"
    )

    print(
        f"Score: {result.score:.4f}"
    )

    print(
        f"Name: {payload.get('name')}"
    )

    print(
        f"Type: {payload.get('type')}"
    )

    print(
        f"File: {payload.get('file_path')}"
    )

    print(
        f"Lines: "
        f"{payload.get('start_line')}-"
        f"{payload.get('end_line')}"
    )

    print("\nContent:")

    print(
        payload.get(
            "content",
            ""
        )[:500]
    )


vector_store.close()


print("\n" + "=" * 70)
print("DIRECT RE-INDEX TEST COMPLETED")
print("=" * 70)