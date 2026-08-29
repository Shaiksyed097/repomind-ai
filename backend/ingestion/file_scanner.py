import os


SUPPORTED_EXTENSIONS = {
    ".py"
}


class FileScanner:

    def __init__(self, repository_path):
        self.repository_path = repository_path

    def get_source_files(self):

        source_files = []

        for root, dirs, files in os.walk(
            self.repository_path
        ):

            # Ignore Git and virtual environments
            dirs[:] = [
                d for d in dirs
                if d not in {
                    ".git",
                    ".venv",
                    "venv",
                    "__pycache__"
                }
            ]

            for file in files:

                extension = os.path.splitext(
                    file
                )[1]

                if extension in SUPPORTED_EXTENSIONS:

                    source_files.append(
                        os.path.join(root, file)
                    )

        return source_files