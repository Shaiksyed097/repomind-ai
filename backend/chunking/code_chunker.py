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

        # ============================================================
        # CLASS CHUNKS
        # ============================================================

        for class_item in classes:

            class_code = class_item.get(
                "code",
                ""
            )

            class_name = class_item.get(
                "name",
                "Unknown"
            )

            start_line = class_item.get(
                "start_line",
                0
            )

            end_line = class_item.get(
                "end_line",
                0
            )

            # --------------------------------------------------------
            # Store the ACTUAL class declaration/code.
            #
            # Previously we only stored:
            #
            # "Class Flask is defined in ..."
            #
            # That caused the LLM to know where the class was,
            # but not what the class actually inherits from.
            # --------------------------------------------------------

            chunk = {

                "content": class_code,

                "metadata": {

                    "file_path": file_path,

                    "name": class_name,

                    "type": "class",

                    "start_line": start_line,

                    "end_line": end_line,

                }
            }

            chunks.append(
                chunk
            )

        # ============================================================
        # FUNCTION / METHOD CHUNKS
        # ============================================================

        for function in functions:

            function_code = function.get(
                "code",
                ""
            )

            function_name = function.get(
                "name",
                "Unknown"
            )

            function_type = function.get(
                "type",
                "function"
            )

            start_line = function.get(
                "start_line",
                0
            )

            end_line = function.get(
                "end_line",
                0
            )

            chunk = {

                "content": function_code,

                "metadata": {

                    "file_path": file_path,

                    "name": function_name,

                    "type": function_type,

                    "start_line": start_line,

                    "end_line": end_line,

                }
            }

            chunks.append(
                chunk
            )

        return chunks