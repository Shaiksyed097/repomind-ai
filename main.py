from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser


# Scan the test repository
scanner = FileScanner("data/test_project")

files = scanner.get_source_files()

print("\nPython files found:\n")

for file in files:
    print(file)


# Parse the Python files
parser = PythonCodeParser()

for file in files:

    print("\n" + "=" * 60)
    print("Parsing:", file)
    print("=" * 60)

    tree, source_code = parser.parse_file(file)

    functions = parser.extract_functions(
        tree,
        source_code
    )

    print("\nFunctions found:\n")

    for function in functions:

        print("-" * 50)
        print("Name:", function["name"])
        print("Type:", function["type"])

        print(
            "Lines:",
            function["start_line"],
            "-",
            function["end_line"]
        )

        print("\nCode:")
        print(function["code"])