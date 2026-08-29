import os


class CodeChunker:

    def create_chunks(self, file_path, functions):

        chunks = []

        for function in functions:

            chunk = {
                "content": function["code"],

                "metadata": {
                    "file_path": os.path.normpath(file_path),
                    "name": function["name"],
                    "type": function["type"],
                    "start_line": function["start_line"],
                    "end_line": function["end_line"],
                }
            }

            chunks.append(chunk)

        return chunks