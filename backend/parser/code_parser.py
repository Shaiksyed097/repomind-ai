from tree_sitter import Language, Parser
import tree_sitter_python


class PythonCodeParser:

    def __init__(self):

        self.language = Language(
            tree_sitter_python.language()
        )

        self.parser = Parser(
            self.language
        )

    def parse_file(self, file_path: str):

        with open(
            file_path,
            "rb"
        ) as f:

            source_code = f.read()

        tree = self.parser.parse(
            source_code
        )

        return tree, source_code

    def extract_functions(
        self,
        tree,
        source_code
    ):

        functions = []

        stack = [tree.root_node]

        while stack:

            node = stack.pop()

            if node.type == "function_definition":

                function_name = None

                for child in node.children:

                    if child.type == "identifier":

                        function_name = source_code[
                            child.start_byte:
                            child.end_byte
                        ].decode("utf-8")

                        break

                function_code = source_code[
                    node.start_byte:
                    node.end_byte
                ].decode("utf-8")

                start_line = (
                    source_code[
                        :node.start_byte
                    ].count(b"\n") + 1
                )

                end_line = (
                    source_code[
                        :node.end_byte
                    ].count(b"\n") + 1
                )

                functions.append({
                    "name": function_name,
                    "type": "function",
                    "start_line": start_line,
                    "end_line": end_line,
                    "code": function_code
                })

            for child in reversed(
                node.children
            ):

                stack.append(child)

        return functions

    def extract_classes(
        self,
        tree,
        source_code
    ):

        classes = []

        stack = [tree.root_node]

        while stack:

            node = stack.pop()

            if node.type == "class_definition":

                class_name = None

                for child in node.children:

                    if child.type == "identifier":

                        class_name = source_code[
                            child.start_byte:
                            child.end_byte
                        ].decode("utf-8")

                        break

                class_code = source_code[
                    node.start_byte:
                    node.end_byte
                ].decode("utf-8")

                start_line = (
                    source_code[
                        :node.start_byte
                    ].count(b"\n") + 1
                )

                end_line = (
                    source_code[
                        :node.end_byte
                    ].count(b"\n") + 1
                )

                classes.append({
                    "name": class_name,
                    "type": "class",
                    "start_line": start_line,
                    "end_line": end_line,
                    "code": class_code
                })

            for child in reversed(
                node.children
            ):

                stack.append(child)

        return classes