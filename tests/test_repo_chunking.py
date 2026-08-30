from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker


repository_path = "data/repos/flask"


scanner = FileScanner(repository_path)
source_files = scanner.get_source_files()

parser = PythonCodeParser()
chunker = CodeChunker()

all_chunks = []

print("\n" + "=" * 60)
print("CHUNKING GITHUB REPOSITORY")
print("=" * 60)

print(
    f"\nFound {len(source_files)} Python files."
)

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

        all_chunks.extend(chunks)

        print(
            f"    Functions: {len(functions)} | "
            f"Chunks: {len(chunks)}",
            flush=True
        )

    except Exception as error:

        print(
            f"    ERROR: {error}",
            flush=True
        )


print("\n" + "=" * 60)

print(
    f"Total Python files: {len(source_files)}"
)

print(
    f"Total chunks: {len(all_chunks)}"
)

print("=" * 60)