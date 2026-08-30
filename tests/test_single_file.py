from backend.parser.code_parser import PythonCodeParser
from backend.chunking.code_chunker import CodeChunker


# ============================================================
# FILE TO TEST
# ============================================================

file_path = "data/repos/flask/src/flask/app.py"


# ============================================================
# INITIALIZE
# ============================================================

parser = PythonCodeParser()
chunker = CodeChunker()


# ============================================================
# PARSE
# ============================================================

print("Parsing app.py...")

tree, source_code = parser.parse_file(
    file_path
)

print("Parsing completed.")


# ============================================================
# EXTRACT FUNCTIONS
# ============================================================

functions = parser.extract_functions(
    tree,
    source_code
)


# ============================================================
# EXTRACT CLASSES
# ============================================================

classes = parser.extract_classes(
    tree,
    source_code
)


# ============================================================
# CREATE CHUNKS
# ============================================================

chunks = chunker.create_chunks(
    file_path,
    functions,
    classes
)


# ============================================================
# CHUNKING RESULT
# ============================================================

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


# ============================================================
# FIRST 5 CHUNKS
# ============================================================

print("\n" + "=" * 60)
print("FIRST 5 CHUNKS")
print("=" * 60)


for index, chunk in enumerate(
    chunks[:5],
    start=1
):

    metadata = chunk["metadata"]

    print("\n" + "-" * 50)

    print(
        f"Chunk {index}"
    )

    print(
        f"Name: "
        f"{metadata['name']}"
    )

    print(
        f"Type: "
        f"{metadata['type']}"
    )

    print(
        f"Lines: "
        f"{metadata['start_line']}-"
        f"{metadata['end_line']}"
    )


# ============================================================
# VERIFY CLASS CONTENT
# ============================================================

print("\n" + "=" * 60)
print("CLASS CHUNK CONTENT TEST")
print("=" * 60)


class_chunks = [
    chunk
    for chunk in chunks
    if chunk["metadata"]["type"] == "class"
]


if not class_chunks:

    print("❌ No class chunks found.")

else:

    for class_chunk in class_chunks:

        metadata = class_chunk["metadata"]

        content = class_chunk["content"]

        print("\n" + "-" * 50)

        print(
            f"Class: "
            f"{metadata['name']}"
        )

        print(
            f"File: "
            f"{metadata['file_path']}"
        )

        print(
            f"Lines: "
            f"{metadata['start_line']}-"
            f"{metadata['end_line']}"
        )

        print("\nFirst 20 lines of stored class content:")
        print("-" * 50)

        content_lines = content.splitlines()

        for line_number, line in enumerate(
            content_lines[:20],
            start=1
        ):

            print(
                f"{line_number:>3}: {line}"
            )


        # --------------------------------------------------------
        # Check Flask inheritance specifically
        # --------------------------------------------------------

        if "class Flask(App)" in content:

            print("\n✅ SUCCESS!")
            print(
                "The actual Flask class declaration "
                "is present in the chunk."
            )

            print(
                "\nFound:"
            )

            print(
                "    class Flask(App)"
            )

        elif "class Flask(" in content:

            print("\n⚠️ Flask class declaration found,")

            print(
                "but the inheritance is different "
                "from the expected 'class Flask(App)'."
            )

        else:

            print("\n❌ PROBLEM!")

            print(
                "The Flask class declaration was NOT "
                "found inside the class chunk."
            )


# ============================================================
# VERIFY CLASS METADATA
# ============================================================

print("\n" + "=" * 60)
print("CLASS METADATA TEST")
print("=" * 60)


for class_item in classes:

    print("\nClass:")
    print(
        class_item["name"]
    )

    print(
        f"Type: {class_item['type']}"
    )

    print(
        f"Start line: "
        f"{class_item['start_line']}"
    )

    print(
        f"End line: "
        f"{class_item['end_line']}"
    )

    print(
        f"Code length: "
        f"{len(class_item['code'])} characters"
    )


print("\n" + "=" * 60)
print("TEST COMPLETED")
print("=" * 60)