import os


class CodeChunker:

    def create_chunks(
        self,
        file_path,
        functions,
        classes=None
    ):

        chunks = []

        if classes is None:
            classes = []

        file_path = os.path.normpath(
            file_path
        )

        # --------------------------------
        # Class metadata chunks
        # --------------------------------

        for class_item in classes:

            chunk = {
                "content": (
                    f"Class {class_item['name']} "
                    f"is defined in {file_path} "
                    f"from line "
                    f"{class_item['start_line']} "
                    f"to line "
                    f"{class_item['end_line']}."
                ),

                "metadata": {
                    "file_path": file_path,
                    "name": class_item["name"],
                    "type": "class",
                    "start_line": class_item["start_line"],
                    "end_line": class_item["end_line"],
                }
            }

            chunks.append(chunk)

        # --------------------------------
        # Function / method chunks
        # --------------------------------

        for function in functions:

            chunk = {
                "content": function["code"],

                "metadata": {
                    "file_path": file_path,
                    "name": function["name"],
                    "type": function["type"],
                    "start_line": function["start_line"],
                    "end_line": function["end_line"],
                }
            }

            chunks.append(chunk)

        return chunks