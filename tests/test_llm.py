from backend.llm.mistral_model import MistralModel


model = MistralModel()


prompt = """
Explain what this Python function does:

def add(a, b):
    return a + b
"""


answer = model.generate(prompt)


print("\nLLM RESPONSE:")
print(answer)