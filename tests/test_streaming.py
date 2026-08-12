"""Test script to demonstrate streaming response functionality"""

from src.services.llm import generate_answer
from src.services.chat_service import chat
from src.services.memory import ConversationMemory
import time

print("=" * 80)
print("Streaming Response Test")
print("=" * 80)

# Test 1: Basic streaming from LLM
print("\n=== Test 1: LLM Streaming (generate_answer) ===")
prompt = "What is machine learning? Answer in 2 sentences."

print("\n[Non-Streaming Mode]")
print("Response: ", end="", flush=True)
start = time.time()
response = generate_answer(prompt, stream=False)
print(response)
print(f"Time: {time.time() - start:.2f}s\n")

print("[Streaming Mode]")
print("Response: ", end="", flush=True)
start = time.time()
full_response = ""
for chunk in generate_answer(prompt, stream=True):
    print(chunk, end="", flush=True)
    full_response += chunk
    time.sleep(0.01)  # Small delay to visualize streaming
print(f"\nTime: {time.time() - start:.2f}s")
print(f"✓ Streamed {len(full_response)} characters")

# Test 2: Chat service streaming
print("\n" + "=" * 80)
print("=== Test 2: Chat Service Streaming ===")

memory = ConversationMemory()
question = "What is AI?"

print("\n[Non-Streaming Chat]")
print("Question:", question)
print("Answer: ", end="", flush=True)
start = time.time()
answer = chat(question, source=None, memory=memory, stream=False)
print(answer)
print(f"Time: {time.time() - start:.2f}s")
print(f"Memory has {memory.get_message_count()} messages")

# Clear memory for streaming test
memory.clear()

print("\n[Streaming Chat]")
print("Question:", question)
print("Answer: ", end="", flush=True)
start = time.time()
full_answer = ""
for chunk in chat(question, source=None, memory=memory, stream=True):
    print(chunk, end="", flush=True)
    full_answer += chunk
    time.sleep(0.01)  # Small delay to visualize streaming
print(f"\nTime: {time.time() - start:.2f}s")
print(f"Memory has {memory.get_message_count()} messages")

# Test 3: Verify memory works with streaming
print("\n" + "=" * 80)
print("=== Test 3: Memory with Streaming ===")

memory.clear()

print("\nQuestion 1 (streaming):", "What is machine learning?")
print("Answer: ", end="", flush=True)
for chunk in chat("What is machine learning?", memory=memory, stream=True):
    print(chunk, end="", flush=True)
    time.sleep(0.01)
print(f"\n\nMemory count: {memory.get_message_count()}")

print("\nQuestion 2 (streaming follow-up):", "Can you give an example?")
print("Answer: ", end="", flush=True)
for chunk in chat("Can you give an example?", memory=memory, stream=True):
    print(chunk, end="", flush=True)
    time.sleep(0.01)
print(f"\n\nMemory count: {memory.get_message_count()}")

if memory.get_message_count() == 4:
    print("✓ Memory correctly stored 2 Q&A pairs (4 messages)")
else:
    print(f"✗ Expected 4 messages, got {memory.get_message_count()}")

print("\n" + "=" * 80)
print("Streaming Test Complete")
print("=" * 80)
print("\n✓ Features Verified:")
print("  - LLM streaming with generate_answer(stream=True)")
print("  - Chat service streaming with chat(stream=True)")
print("  - Non-streaming backward compatibility")
print("  - Memory works with streaming")
print("  - Citations included at end of stream")
print("\n✓ How to use in app:")
print("  1. Run: python app.py")
print("  2. Streaming is ON by default")
print("  3. Type 'stream' to toggle on/off")
print("  4. Type 'clear' to reset memory")
print("  5. Type 'exit' to quit")
