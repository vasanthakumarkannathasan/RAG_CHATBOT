from langchain_core.documents import Document

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

    context = "\n\n".join(
        document.page_content
        for document in documents
    )

    # Build conversation history section
    history_section = ""
    if conversation_history and len(conversation_history) > 0:
        history_section = "\n================================================\nConversation History\n"
        for msg in conversation_history:
            role = "User" if msg["role"] == "user" else "Assistant"
            history_section += f"{role}: {msg['content']}\n"
        history_section += "================================================\n"

    prompt = f"""
{SYSTEM_PROMPT}{history_section}
================================================
Context
{context}
================================================
Current Question
{question}
"""
    return prompt