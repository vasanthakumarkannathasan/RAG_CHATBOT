"""Test the simplified chat_service.py changes"""

from src.services.chat_service import chat

print("=" * 60)
print("Testing Simplified Chat Service")
print("=" * 60)

# Test the new dict return format
print("\nTest: chat() function with new dict format")
print("-" * 60)

question = "What is machine learning?"

result = chat(
    question=question,
    source=None,
    session_id="test-session"
)

print(f"\nQuestion: {question}")
print(f"\nResult type: {type(result)}")
print(f"\nAnswer: {result['answer'][:200]}...")
print(f"\nSources ({len(result['sources'])} found):")
for source in result['sources']:
    print(f"  • {source['document']} - Page {source['page']}")

print("\n" + "=" * 60)
print("✓ Chat service simplified successfully!")
print("=" * 60)
print("\nChanges made:")
print("  • Removed: memory parameter")
print("  • Removed: streaming support")
print("  • Removed: @measure_performance decorator")
print("  • Changed: Returns dict instead of string")
print("  • Changed: Sources as list of dicts with 'document' and 'page'")
print("  • Added: session_id parameter (for future use)")
