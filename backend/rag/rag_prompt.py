class RAGPrompt:

    def build_prompt(
        self,
        question,
        results
    ):

        context_parts = []

        # ========================================================
        # BUILD RETRIEVED CONTEXT
        # ========================================================

        for index, result in enumerate(
            results
        ):

            payload = result.payload

            file_path = payload.get(
                "file_path",
                "Unknown"
            )

            name = payload.get(
                "name",
                "Unknown"
            )

            item_type = payload.get(
                "type",
                "Unknown"
            )

            class_name = payload.get(
                "class_name"
            )

            start_line = payload.get(
                "start_line",
                "?"
            )

            end_line = payload.get(
                "end_line",
                "?"
            )

            content = payload.get(
                "content",
                ""
            )

            # ----------------------------------------------------
            # Class
            # ----------------------------------------------------

            if item_type == "class":

                context = f"""
Source {index + 1}

Type: Class

File: {file_path}

Class: {name}

Lines: {start_line}-{end_line}

Repository code:
{content}
"""

            # ----------------------------------------------------
            # Method
            # ----------------------------------------------------

            elif item_type == "method":

                context = f"""
Source {index + 1}

Type: Method

File: {file_path}

Class: {class_name}

Method: {name}

Lines: {start_line}-{end_line}

Repository code:
{content}
"""

            # ----------------------------------------------------
            # Function
            # ----------------------------------------------------

            else:

                context = f"""
Source {index + 1}

Type: Function

File: {file_path}

Function: {name}

Lines: {start_line}-{end_line}

Repository code:
{content}
"""

            context_parts.append(
                context
            )

        context = "\n".join(
            context_parts
        )

        # ========================================================
        # RAG PROMPT
        # ========================================================

        prompt = f"""
You are RepoMind, an AI assistant for
understanding source code repositories.

Your job is to answer the user's question
using ONLY the retrieved repository context.

IMPORTANT RULES:

1. Do not invent information.

2. Do not use your general knowledge if the
   retrieved repository context does not support
   the answer.

3. Prefer exact code declarations over guesses.

4. When a class inheritance relationship is
   present in a class declaration, use it.

5. When a method belongs to a class, mention
   the parent class.

6. Always mention the relevant file path.

7. Always mention line numbers when available.

8. If the retrieved context is insufficient,
   respond exactly with:

"I don't have enough information in the
retrieved code to answer that."

9. Keep the answer concise and technical.

10. If useful, show the relevant code snippet.

------------------------------------------------------------
RETRIEVED REPOSITORY CONTEXT
------------------------------------------------------------

{context}

------------------------------------------------------------
USER QUESTION
------------------------------------------------------------

{question}

------------------------------------------------------------
ANSWER
------------------------------------------------------------
"""

        return prompt