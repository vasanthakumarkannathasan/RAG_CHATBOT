from src.services.database import get_vector_db


vector_db = get_vector_db()
collection = vector_db._collection
data = collection.get()

print("=" * 70)
print("Enterprise RAG Database Inspection")
print("=" * 70)

print(f"Collection Name : {collection.name}")
print(f"Total Chunks    : {collection.count()}")
print()

for index in range(len(data["documents"])):
    print("=" * 70)
    print(f"Chunk : {index + 1}")
    print("-" * 70)
    print("Document")
    print(data["documents"][index])
    print()
    print("Metadata")
    print(data["metadatas"][index])
    print()
    print("ID")
    print(data["ids"][index])
    print()

    if index == 4:
        print("Showing first 5 chunks only...")
        break