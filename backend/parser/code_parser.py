from tree_sitter import Language, Parser
import tree_sitter_python


class PythonCodeParser:

    def __init__(self):

        self.language = Language(
            tree_sitter_python.language()
        )

        self.parser = Parser(self.language)

    def parse_file(self, file_path: str):

        with open(
            file_path,
            "rb"
        ) as f:

            source_code = f.read()

        tree = self.parser.parse(source_code)

        return tree, source_code

    def extract_functions(self, tree, source_code):

        functions = []

        def walk(node):

            if node.type == "function_definition":

                function_name = None

                for child in node.children:

                    if child.type == "identifier":

                        function_name = source_code[
                            child.start_byte:child.end_byte
                        ].decode("utf-8")

                        break

                function_code = source_code[
                    node.start_byte:node.end_byte
                ].decode("utf-8")

                functions.append({
                    "name": function_name,
                    "type": "function",
                    "start_line": node.start_point.row + 1,
                    "end_line": node.end_point.row + 1,
                    "code": function_code
                })

            for child in node.children:
                walk(child)

        walk(tree.root_node)

        return functions