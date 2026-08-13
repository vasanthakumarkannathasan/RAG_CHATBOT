from langchain_core.documents import Document
from src.utils.logger import logger

SYSTEM_PROMPT = """
You are an Enterprise AI Assistant.
Answer ONLY using the provided context.
If the answer is not available in the context,
reply:
'I couldn't find the answer in the indexed documents.'
Always answer clearly and professionally.

If there is conversation history, use it to understand context and follow-up questions,
but always answer based on the provided context documents.
"""

def build_prompt(
    question: str,
    documents: list[Document],
    conversation_history: list[dict] | None = None
) -> str:
    """
    Build a comprehensive prompt for the LLM including system instructions,
    conversation history, retrieved context, and the current question.
    """
    try:
        logger.info(f"Building prompt for question: '{question[:50]}...'")
        logger.info(f"Documents provided: {len(documents)}")
        
        context = "\n\n".join(
            document.page_content
            for document in documents
        )
        
        context_length = len(context)
        logger.info(f"Context size: {context_length} characters")

        # Build conversation history section
        history_section = ""
        if conversation_history and len(conversation_history) > 0:
            history_section = "\n================================================\nConversation History\n"
            for msg in conversation_history:
                role = "User" if msg["role"] == "user" else "Assistant"
                history_section += f"{role}: {msg['content']}\n"
            history_section += "================================================\n"
            logger.info(f"Included conversation history: {len(conversation_history)} messages")
        else:
            logger.info("No conversation history included")

        prompt = f"""
{SYSTEM_PROMPT}{history_section}
================================================
Context
{context}
================================================
Current Question
{question}
"""
        prompt_length = len(prompt)
        logger.info(f"Prompt built successfully - Total length: {prompt_length} characters")
        
        return prompt
        
    except Exception as ex:
        logger.exception(f"Failed to build prompt: {ex}")
        raise