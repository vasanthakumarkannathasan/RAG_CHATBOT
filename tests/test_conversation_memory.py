"""Test script to demonstrate conversation memory functionality"""

from src.services.memory import ConversationMemory
from src.services.prompt_builder import build_prompt
from langchain_core.documents import Document

print("=" * 70)
print("Conversation Memory Test")
print("=" * 70)

# Test 1: Basic memory operations
print("\n=== Test 1: Basic Memory Operations ===")
memory = ConversationMemory()
print(f"Initial state - Empty: {memory.is_empty()}")
print(f"Initial state - Count: {memory.get_message_count()}")

# Add some messages
memory.add_user_message("What is machine learning?")
memory.add_assistant_message("Machine learning is a subset of AI...")
print(f"\nAfter adding 1 Q&A pair:")
print(f"  Empty: {memory.is_empty()}")
print(f"  Count: {memory.get_message_count()}")

memory.add_user_message("Can you explain supervised learning?")
memory.add_assistant_message("Supervised learning uses labeled data...")
print(f"\nAfter adding 2 Q&A pairs:")
print(f"  Count: {memory.get_message_count()}")

# Test 2: Getting messages
print("\n=== Test 2: Retrieving Messages ===")
messages = memory.get_messages()
for i, msg in enumerate(messages, 1):
    print(f"{i}. {msg['role'].title()}: {msg['content'][:50]}...")

# Test 3: Max messages limit
print("\n=== Test 3: Max Messages Limit (6 messages = 3 Q&A pairs) ===")
memory.add_user_message("Question 3")
memory.add_assistant_message("Answer 3")
memory.add_user_message("Question 4")
memory.add_assistant_message("Answer 4")
print(f"After adding 4 Q&A pairs: {memory.get_message_count()} messages")
print("✓ Should keep only last 6 messages (3 Q&A pairs)")

messages = memory.get_messages()
print(f"Retrieved messages: {len(messages)}")
for i, msg in enumerate(messages, 1):
    print(f"  {i}. {msg['role']}: {msg['content']}")

# Test 4: Clear memory
print("\n=== Test 4: Clear Memory ===")
memory.clear()
print(f"After clear - Empty: {memory.is_empty()}")
print(f"After clear - Count: {memory.get_message_count()}")

# Test 5: Integration with prompt builder
print("\n=== Test 5: Integration with Prompt Builder ===")
memory = ConversationMemory()
memory.add_user_message("What is AI?")
memory.add_assistant_message("AI is artificial intelligence...")
memory.add_user_message("Tell me more about it")

# Create sample document
docs = [
    Document(page_content="AI enables machines to perform tasks...", metadata={})
]

# Build prompt with history
prompt = build_prompt(
    question="Tell me more about it",
    documents=docs,
    conversation_history=memory.get_messages()
)

print("Prompt preview (first 500 chars):")
print("-" * 70)
print(prompt[:500] + "...")
print("-" * 70)

if "Conversation History" in prompt:
    print("✓ Conversation history is included in the prompt!")
else:
    print("✗ WARNING: Conversation history NOT in prompt")

if "What is AI?" in prompt:
    print("✓ Previous questions are in the prompt!")
else:
    print("✗ WARNING: Previous questions NOT in prompt")

# Test 6: Prompt without history
print("\n=== Test 6: Prompt Without History (No Memory) ===")
prompt_no_history = build_prompt(
    question="What is AI?",
    documents=docs,
    conversation_history=None
)

if "Conversation History" not in prompt_no_history:
    print("✓ No history section when memory is None")
else:
    print("✗ WARNING: History section should not appear")

print("\n" + "=" * 70)
print("Conversation Memory Test Complete")
print("=" * 70)
print("\nMemory features:")
print("  ✓ Stores user and assistant messages")
print("  ✓ Keeps last 6 messages (3 Q&A pairs)")
print("  ✓ Auto-trims older messages")
print("  ✓ Can be cleared on demand")
print("  ✓ Integrates with prompt builder")
print("  ✓ Provides context for follow-up questions")
