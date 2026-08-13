from src.services.retrieval import retrieve_documents
from src.services.prompt_builder import build_prompt
from src.services.llm import generate_answer
from src.utils.logger import logger
from src.utils.performance import measure_performance


@measure_performance("Chat Service")
def chat(
    question: str,
    source: str | None = None,
    session_id: str | None = None,
):
    try:
        logger.info(f"Chat request - Question: '{question[:50]}...', Source: {source}, Session: {session_id}")
        
        documents = retrieve_documents(
            question=question,
            source=source
        )
        
        logger.info(f"Retrieved {len(documents)} documents for query")

        prompt = build_prompt(
            question=question,
            documents=documents
        )
        
        logger.info(f"Built prompt with {len(prompt)} characters")

        answer = generate_answer(prompt)
        
        logger.info(f"Generated answer with {len(answer)} characters")

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
        
        logger.info(f"Chat completed - {len(sources)} unique sources cited")
        
        return {
            "answer": answer,
            "sources": sources
        }
        
    except Exception as ex:
        logger.exception(f"Chat service failed for question: '{question[:50]}...'")
        raise