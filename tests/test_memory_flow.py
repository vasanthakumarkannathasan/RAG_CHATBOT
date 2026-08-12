"""Demonstration of conversation memory behavior across multiple questions"""

from src.services.memory import ConversationMemory
from src.services.prompt_builder import build_prompt
from langchain_core.documents import Document

print("=" * 80)
print("Conversation Memory Flow Demonstration")
print("=" * 80)

# Simulate a chat session
memory = ConversationMemory()
sample_docs = [Document(page_content="Sample context about AI and ML", metadata={})]

def show_prompt_state(question_num, question, memory):
    """Show what's in the prompt at each stage"""
    history = memory.get_messages()
    prompt = build_prompt(question, sample_docs, conversation_history=history if not memory.is_empty() else None)
    
    print(f"\n{'=' * 80}")
    print(f"QUESTION {question_num}: {question}")
    print(f"{'=' * 80}")
    print(f"Memory state:")
    print(f"  - Total messages in memory: {memory.get_message_count()}")
    print(f"  - Is empty: {memory.is_empty()}")
    
    if not memory.is_empty():
        print(f"\n  Conversation history in memory:")
        for i, msg in enumerate(history, 1):
            print(f"    {i}. {msg['role']}: {msg['content'][:60]}...")
    else:
        print(f"  No history yet (first question)")
    
    print(f"\n  Prompt contains history: {'YES' if 'Conversation History' in prompt else 'NO'}")
    
    if 'Conversation History' in prompt:
        # Extract and show the history section
        start = prompt.find('Conversation History')
        end = prompt.find('================================================', start + 20)
        history_section = prompt[start:end]
        print(f"\n  History section in prompt:")
        for line in history_section.split('\n')[:8]:  # Show first 8 lines
            if line.strip():
                print(f"    {line}")

# Simulate conversation flow
print("\n" + "▶" * 40)
print("SIMULATION: Chat Session Starts")
print("▶" * 40)

# Question 1
show_prompt_state(1, "What is machine learning?", memory)
# Simulate adding response to memory
memory.add_user_message("What is machine learning?")
memory.add_assistant_message("Machine learning is a subset of AI that enables systems to learn from data...")

# Question 2 (Follow-up)
show_prompt_state(2, "Can you give me an example?", memory)
# Simulate adding response to memory
memory.add_user_message("Can you give me an example?")
memory.add_assistant_message("Sure! In healthcare, ML algorithms analyze medical imaging to detect anomalies...")

# Question 3 (Another follow-up)
show_prompt_state(3, "How does it compare to traditional programming?", memory)
# Simulate adding response to memory
memory.add_user_message("How does it compare to traditional programming?")
memory.add_assistant_message("Traditional programming requires explicit rules, while ML learns patterns from data...")

# Question 4 (Testing memory limit)
show_prompt_state(4, "What are some real-world applications?", memory)
memory.add_user_message("What are some real-world applications?")
memory.add_assistant_message("Real-world applications include recommendation systems, fraud detection, and autonomous vehicles...")

# Question 5 (Should start dropping oldest messages)
show_prompt_state(5, "Tell me about deep learning", memory)

print("\n" + "■" * 40)
print("ACTION: User types 'clear' command")
print("■" * 40)
memory.clear()
print(f"\nMemory cleared!")
print(f"  - Total messages: {memory.get_message_count()}")
print(f"  - Is empty: {memory.is_empty()}")

# Question after clear
show_prompt_state(6, "What is deep learning?", memory)

print("\n" + "×" * 40)
print("ACTION: User types 'exit' or closes application")
print("×" * 40)
print("\nSession ends - Memory is destroyed")
print("Next time user starts the app, memory will be fresh/empty\n")

print("=" * 80)
print("KEY BEHAVIORS:")
print("=" * 80)
print("✓ Question 1: NO history (memory is empty)")
print("✓ Question 2+: YES history (previous Q&A pairs included)")
print("✓ History persists: Across all questions in the same session")
print("✓ Memory limit: Keeps last 6 messages (3 Q&A pairs) automatically")
print("✓ 'clear' command: Resets memory immediately")
print("✓ Exit/Quit: Session ends, memory destroyed (fresh start next time)")
print("=" * 80)

print("\n" + "📋 SUMMARY")
print("=" * 80)
print("""
When user starts the app:
  Session 1:
    Q1: "What is ML?"              → No history
    Q2: "Give example?"            → History: [Q1, A1]
    Q3: "More details?"            → History: [Q1, A1, Q2, A2]
    Q4: "Applications?"            → History: [Q1, A1, Q2, A2, Q3, A3]
    Q5: "Deep learning?"           → History: [Q2, A2, Q3, A3, Q4, A4]  ← Oldest dropped
    
    User types: clear
    
    Q6: "What is AI?"              → No history (cleared)
    Q7: "Explain more"             → History: [Q6, A6]
    
    User types: exit
    
  Session 2 (Next time user runs app):
    Q1: "Hello"                    → No history (fresh start)
""")
print("=" * 80)
