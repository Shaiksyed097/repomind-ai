from backend.rag.rag_prompt import RAGPrompt


class FakePayload:

    def __init__(self):

        self.payload = {
            "file_path": "data/test_project/app.py",
            "name": "add",
            "start_line": 1,
            "end_line": 2,
            "content": """def add(a, b):
    return a + b"""
        }


prompt_builder = RAGPrompt()

question = "Which function performs addition?"

results = [
    FakePayload()
]


prompt = prompt_builder.build_prompt(
    question,
    results
)


print("\nGENERATED RAG PROMPT:")
print("=" * 60)
print(prompt)
