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

    # ============================================================
    # PARSE FILE
    # ============================================================

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

    # ============================================================
    # GET NODE NAME
    # ============================================================

    def _get_node_name(
        self,
        node,
        source_code
    ):

        for child in node.children:

            if child.type == "identifier":

                return source_code[
                    child.start_byte:
                    child.end_byte
                ].decode(
                    "utf-8",
                    errors="replace"
                )

        return "unknown"

    # ============================================================
    # GET LINE NUMBERS
    # ============================================================

    def _get_line_numbers(
        self,
        node,
        source_code
    ):

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

        return start_line, end_line

    # ============================================================
    # GET CLASS DECLARATION
    # ============================================================

    def _get_class_declaration(
        self,
        node,
        source_code
    ):

        # --------------------------------------------------------
        # Find class body
        # --------------------------------------------------------

        body_node = None

        for child in node.children:

            if child.type == "block":

                body_node = child
                break

        # --------------------------------------------------------
        # If body exists, everything before the body is the
        # class declaration.
        # --------------------------------------------------------

        if body_node:

            declaration = source_code[
                node.start_byte:
                body_node.start_byte
            ].decode(
                "utf-8",
                errors="replace"
            ).strip()

        else:

            declaration = source_code[
                node.start_byte:
                node.end_byte
            ].decode(
                "utf-8",
                errors="replace"
            ).strip()

        return declaration

    # ============================================================
    # EXTRACT FUNCTIONS
    # ============================================================

    def extract_functions(
        self,
        tree,
        source_code
    ):

        functions = []

        def visit(
            node,
            current_class=None
        ):

            # ----------------------------------------------------
            # Track class context
            # ----------------------------------------------------

            if node.type == "class_definition":

                class_name = self._get_node_name(
                    node,
                    source_code
                )

                for child in node.children:

                    visit(
                        child,
                        class_name
                    )

                return

            # ----------------------------------------------------
            # Function definition
            # ----------------------------------------------------

            if node.type == "function_definition":

                function_name = self._get_node_name(
                    node,
                    source_code
                )

                function_code = source_code[
                    node.start_byte:
                    node.end_byte
                ].decode(
                    "utf-8",
                    errors="replace"
                )

                start_line, end_line = (
                    self._get_line_numbers(
                        node,
                        source_code
                    )
                )

                # ------------------------------------------------
                # Detect method vs normal function
                # ------------------------------------------------

                if current_class:

                    function_type = "method"

                else:

                    function_type = "function"

                functions.append({

                    "name": function_name,

                    "type": function_type,

                    "class_name": current_class,

                    "start_line": start_line,

                    "end_line": end_line,

                    "code": function_code

                })

                # ------------------------------------------------
                # Continue searching nested functions
                # ------------------------------------------------

                for child in node.children:

                    visit(
                        child,
                        current_class
                    )

                return

            # ----------------------------------------------------
            # Normal traversal
            # ----------------------------------------------------

            for child in node.children:

                visit(
                    child,
                    current_class
                )

        visit(
            tree.root_node
        )

        return functions

    # ============================================================
    # EXTRACT CLASSES
    # ============================================================

    def extract_classes(
        self,
        tree,
        source_code
    ):

        classes = []

        def visit(node):

            if node.type == "class_definition":

                class_name = self._get_node_name(
                    node,
                    source_code
                )

                class_code = source_code[
                    node.start_byte:
                    node.end_byte
                ].decode(
                    "utf-8",
                    errors="replace"
                )

                start_line, end_line = (
                    self._get_line_numbers(
                        node,
                        source_code
                    )
                )

                declaration = (
                    self._get_class_declaration(
                        node,
                        source_code
                    )
                )

                classes.append({

                    "name": class_name,

                    "type": "class",

                    "start_line": start_line,

                    "end_line": end_line,

                    "declaration": declaration,

                    "code": class_code

                })

            for child in node.children:

                visit(child)

        visit(
            tree.root_node
        )

        return classes