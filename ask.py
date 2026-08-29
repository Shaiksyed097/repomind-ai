from backend.rag.rag_pipeline import RAGPipeline


pipeline = RAGPipeline()


question = input(
    "\nAsk RepoMind a question: "
)


answer, results = pipeline.ask(
    question
)


print("\n" + "=" * 60)
print("REPO-MIND ANSWER")
print("=" * 60)

print(answer)


print("\n" + "=" * 60)
print("SOURCES")
print("=" * 60)


for index, result in enumerate(results):

    payload = result.payload

    print(
        f"\n[{index + 1}] "
        f"{payload['file_path']} "
        f"({payload['start_line']}-"
        f"{payload['end_line']})"
    )

    print(
        f"Function: {payload['name']}"
    )


pipeline.close()