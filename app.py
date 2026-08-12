from src.services.chat_service import chat
from src.exceptions.base_exception import EnterpriseRAGException
from src.utils.logger import logger
import sys

print("=" * 60)
print("Enterprise RAG Chat")
print("=" * 60)
print("\nCommands:")
print("  - Type 'exit' or 'quit' to end the session")
print("=" * 60)

while True:
    question = input("\nYou: ").strip()

    if question.lower() in ["exit", "quit"]:
        print("\nGoodbye!")
        break

    if not question:
        continue

    try:
        print("\nAI: ", end="", flush=True)
        
        # Get chat response
        result = chat(question, source=None)
        
        # Print answer
        print(result["answer"])
        
        # Print sources
        if result["sources"]:
            print("\n📚 Sources:")
            for source in result["sources"]:
                print(f"  📄 {source['document']} (Page {source['page']})")
    
    except EnterpriseRAGException as ex:
        print(f"\nError: An error occurred while processing your question. Please try again.")
        logger.error(f"Chat error: {ex}")
    except Exception as ex:
        print(f"\nError: An unexpected error occurred. Please try again.")
        logger.exception(f"Unexpected error in main loop: {ex}")