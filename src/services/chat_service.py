from src.services.retrieval import retrieve_documents
from src.services.prompt_builder import build_prompt
from src.services.llm import generate_answer


def chat(
    question: str,
    source: str | None = None,
    session_id: str | None = None,
):

    documents = retrieve_documents(
        question=question,
        source=source
    )

    prompt = build_prompt(
        question=question,
        documents=documents
    )

    answer = generate_answer(prompt)

    unique_sources = set()

    for doc in documents:

        unique_sources.add(
            (
                doc.metadata["source"],
                doc.metadata["page"] + 1
            )
        )

    sources = [
        {
            "document": source,
            "page": page
        }
        for source, page in sorted(unique_sources)
    ]

    return {
        "answer": answer,
        "sources": sources
    }