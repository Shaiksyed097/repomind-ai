from backend.ingestion.file_scanner import FileScanner


repository_path = "data/repos/flask"

scanner = FileScanner(
    repository_path
)

source_files = scanner.get_source_files()


print("\nPython files found:")

for file_path in source_files:

    print(file_path)

print(
    f"\nTotal Python files: "
    f"{len(source_files)}"
)