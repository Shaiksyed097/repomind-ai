from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker
from backend.embeddings.embedding_model import CodeEmbeddingModel
from backend.vectorstore.qdrant_store import QdrantVectorStore


# --------------------------------
# 1. Scan repository
# --------------------------------

scanner = FileScanner("data/test_project")

files = scanner.get_source_files()

print("\nPython files found:\n")

for file in files:
    print(file)


# --------------------------------
# 2. Initialize components
# --------------------------------

parser = PythonCodeParser()

chunker = CodeChunker()

embedding_model = CodeEmbeddingModel()

vector_store = QdrantVectorStore()


# --------------------------------
# 3. Process files
# --------------------------------

for file in files:

    print("\n" + "=" * 60)
    print("Processing:", file)
    print("=" * 60)

    # Parse file
    tree, source_code = parser.parse_file(file)

    functions = parser.extract_functions(
        tree,
        source_code
    )

    # Create chunks
    chunks = chunker.create_chunks(
        file,
        functions
    )

    print(
        f"\nCreated {len(chunks)} chunks."
    )

    # Generate embeddings
    embeddings = embedding_model.embed_chunks(
        chunks
    )

    print(
        f"Generated {len(embeddings)} embeddings."
    )

    # Store in Qdrant
    vector_store.add_chunks(
        chunks,
        embeddings
    )


# --------------------------------
# 4. Close Qdrant
# --------------------------------

vector_store.close()

print("\nRepoMind ingestion completed!")