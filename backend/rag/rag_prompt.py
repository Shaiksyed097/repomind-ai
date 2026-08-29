class RAGPrompt:

    def build_prompt(self, question, results):

        context_parts = []

        for index, result in enumerate(results):

            payload = result.payload

            context = f"""
Source {index + 1}

File: {payload['file_path']}
Function: {payload['name']}
Lines: {payload['start_line']}-{payload['end_line']}

Code:
{payload['content']}
"""

            context_parts.append(context)

        context = "\n".join(context_parts)

        prompt = f"""
You are RepoMind, an AI assistant that answers
questions about source code.

Answer the user's question using ONLY the
provided repository context.

If the context does not contain enough
information to answer the question, say:

"I don't have enough information in the
retrieved code to answer that."

Do not invent files, functions, variables,
behavior, or implementation details.

Always mention the relevant file and line
numbers when they are available.

Repository Context:
{context}

User Question:
{question}

Answer:
"""

        return prompt