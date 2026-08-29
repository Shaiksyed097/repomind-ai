from backend.vectorstore.qdrant_store import QdrantVectorStore


store = QdrantVectorStore()


points, next_page = store.client.scroll(
    collection_name=store.collection_name,
    limit=2000,
    with_payload=True
)


function_count = 0
class_count = 0
other_count = 0


class_names = []


for point in points:

    payload = point.payload

    item_type = payload.get("type")

    if item_type == "function":

        function_count += 1

    elif item_type == "class":

        class_count += 1

        class_names.append(
            payload.get("name")
        )

    else:

        other_count += 1


print("\n" + "=" * 60)
print("QDRANT CONTENT CHECK")
print("=" * 60)

print(
    f"\nTotal points: {len(points)}"
)

print(
    f"Function chunks: {function_count}"
)

print(
    f"Class chunks: {class_count}"
)

print(
    f"Other chunks: {other_count}"
)


print("\nClasses found:")

for name in class_names:

    print(
        f"  - {name}"
    )


store.close()