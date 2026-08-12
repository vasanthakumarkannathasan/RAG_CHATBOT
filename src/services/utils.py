from src.services.retrieval import retrieve_documents

documents = retrieve_documents("What is Python?")

print(len(documents))

for doc in documents:
    print("-" * 50)
    print(doc.page_content)