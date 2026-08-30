from backend.ingestion.file_scanner import FileScanner
from backend.parser.code_parser import PythonCodeParser


repository_path = "data/repos/flask"


scanner = FileScanner(
    repository_path
)

source_files = scanner.get_source_files()


parser = PythonCodeParser()


total_functions = 0


print("\n" + "=" * 60)
print("PARSING GITHUB REPOSITORY")
print("=" * 60)


for file_path in source_files:

    try:

        tree, source_code = parser.parse_file(
            file_path
        )

        functions = parser.extract_functions(
            tree,
            source_code
        )

        total_functions += len(functions)

        print(
            f"\nFile: {file_path}"
        )

        print(
            f"Functions found: "
            f"{len(functions)}"
        )

    except Exception as error:

        print(
            f"\nError parsing: {file_path}"
        )

        print(error)


print("\n" + "=" * 60)

print(
    f"Total Python files: "
    f"{len(source_files)}"
)

print(
    f"Total functions found: "
    f"{total_functions}"
)

print("=" * 60)