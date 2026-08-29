from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker


file_path = "data/repos/flask/src/flask/app.py"


parser = PythonCodeParser()
chunker = CodeChunker()


print("Parsing app.py...")

tree, source_code = parser.parse_file(
    file_path
)

print("Parsing completed.")


functions = parser.extract_functions(
    tree,
    source_code
)

classes = parser.extract_classes(
    tree,
    source_code
)


chunks = chunker.create_chunks(
    file_path,
    functions,
    classes
)


print("\n" + "=" * 60)
print("CHUNKING RESULT")
print("=" * 60)

print(
    f"Functions: {len(functions)}"
)

print(
    f"Classes: {len(classes)}"
)

print(
    f"Total chunks: {len(chunks)}"
)


print("\n" + "=" * 60)
print("FIRST 5 CHUNKS")
print("=" * 60)


for index, chunk in enumerate(
    chunks[:5],
    start=1
):

    print("\n" + "-" * 50)

    print(
        f"Chunk {index}"
    )

    print(
        f"Name: "
        f"{chunk['metadata']['name']}"
    )

    print(
        f"Type: "
        f"{chunk['metadata']['type']}"
    )

    print(
        f"Lines: "
        f"{chunk['metadata']['start_line']}-"
        f"{chunk['metadata']['end_line']}"
    )