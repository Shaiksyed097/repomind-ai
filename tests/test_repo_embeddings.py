from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker
from backend.embeddings.embedding_model import CodeEmbeddingModel


repository_path = "data/repos/flask"


# --------------------------------
# Initialize components
# --------------------------------

scanner = FileScanner(
    repository_path
)

parser = PythonCodeParser()

chunker = CodeChunker()

embedding_model = CodeEmbeddingModel()


# --------------------------------
# Find Python files
# --------------------------------

source_files = scanner.get_source_files()


all_chunks = []


print("\n" + "=" * 60)
print("CREATING FLASK REPOSITORY EMBEDDINGS")
print("=" * 60)


# --------------------------------
# Parse and chunk all files
# --------------------------------

for index, file_path in enumerate(
    source_files,
    start=1
):

    print(
        f"[{index}/{len(source_files)}] "
        f"{file_path}",
        flush=True
    )

    try:

        tree, source_code = parser.parse_file(
            file_path
        )

        functions = parser.extract_functions(
            tree,
            source_code
        )

        chunks = chunker.create_chunks(
            file_path,
            functions
        )

        all_chunks.extend(
            chunks
        )

    except Exception as error:

        print(
            f"    ERROR: {error}"
        )


print("\n" + "=" * 60)

print(
    f"Total chunks: {len(all_chunks)}"
)

print("=" * 60)


# --------------------------------
# Generate embeddings
# --------------------------------

print("\nGenerating embeddings...")

texts = [
    chunk["content"]
    for chunk in all_chunks
]

embeddings = [
    embedding_model.embed_text(text)
    for text in texts
]

print(
    f"Generated embeddings: "
    f"{len(embeddings)}"
)

print(
    f"Embedding dimensions: "
    f"{len(embeddings[0])}"
)