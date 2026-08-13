"""
CONVERSATION MEMORY BEHAVIOR - COMPLETE GUIDE
================================================

┌─────────────────────────────────────────────────────────────────┐
│                    SESSION LIFECYCLE                             │
└─────────────────────────────────────────────────────────────────┘

[User runs app.py] → Memory Created (Empty) → [User exits] → Memory Destroyed


┌─────────────────────────────────────────────────────────────────┐
│              QUESTION-BY-QUESTION FLOW                           │
└─────────────────────────────────────────────────────────────────┘

Question 1: "What is machine learning?"
├─ Memory Before: []
├─ History in Prompt: ❌ NO
├─ Prompt Builder receives: question + docs + None
├─ LLM sees: System prompt + Context + Question
└─ Memory After: [Q1, A1]

Question 2: "Can you give an example?"
├─ Memory Before: [Q1, A1]
├─ History in Prompt: ✅ YES
├─ Prompt Builder receives: question + docs + [Q1, A1]
├─ LLM sees: System prompt + History [Q1, A1] + Context + Question
└─ Memory After: [Q1, A1, Q2, A2]

Question 3: "Tell me more"
├─ Memory Before: [Q1, A1, Q2, A2]
├─ History in Prompt: ✅ YES
├─ Prompt Builder receives: question + docs + [Q1, A1, Q2, A2]
├─ LLM sees: System prompt + History [Q1→A1, Q2→A2] + Context + Question
└─ Memory After: [Q1, A1, Q2, A2, Q3, A3]

Question 4: "More details?"
├─ Memory Before: [Q1, A1, Q2, A2, Q3, A3] (6 messages - LIMIT REACHED)
├─ History in Prompt: ✅ YES
├─ Prompt Builder receives: question + docs + [Q1, A1, Q2, A2, Q3, A3]
├─ LLM sees: All 3 previous Q&A pairs + Current question
└─ Memory After: [Q1, A1, Q2, A2, Q3, A3, Q4, A4] → AUTO-TRIMS to [Q2, A2, Q3, A3, Q4, A4]

Question 5: "Another question"
├─ Memory Before: [Q2, A2, Q3, A3, Q4, A4] (oldest Q1, A1 dropped)
├─ History in Prompt: ✅ YES
├─ Prompt Builder receives: question + docs + [Q2, A2, Q3, A3, Q4, A4]
├─ LLM sees: Last 3 Q&A pairs (not the first one anymore)
└─ Memory After: [Q3, A3, Q4, A4, Q5, A5]


┌─────────────────────────────────────────────────────────────────┐
│                   WHEN HISTORY STOPS                             │
└─────────────────────────────────────────────────────────────────┘

Scenario 1: User types 'clear'
  Before: [Q1, A1, Q2, A2, Q3, A3]
  Action: memory.clear()
  After: []
  Next Question: NO history (starts fresh)

Scenario 2: User types 'exit' or 'quit'
  Action: App closes
  Memory: Destroyed (goes out of scope)
  Next Run: New memory instance (empty)


┌─────────────────────────────────────────────────────────────────┐
│                    IMPLEMENTATION                                │
└─────────────────────────────────────────────────────────────────┘

In app.py:
  ┌─────────────────────────────────────┐
  │ memory = ConversationMemory()      │  ← Created once per session
  │                                     │
  │ while True:                         │
  │   question = input()                │
  │   answer = chat(                    │
  │       question,                     │
  │       memory=memory  ← Same memory │  ← Passed to every chat() call
  │   )                                 │
  └─────────────────────────────────────┘

In chat_service.py:
  ┌───────────────────────────────────────────────┐
  │ def chat(question, memory):                  │
  │   # Get history from memory                  │
  │   history = memory.get_messages()  ← Retrieve│
  │                                              │
  │   # Build prompt with history                │
  │   prompt = build_prompt(                     │
  │       question, docs, history    ← Include  │
  │   )                                          │
  │                                              │
  │   # Get answer from LLM                      │
  │   answer = generate_answer(prompt)           │
  │                                              │
  │   # Update memory                            │
  │   memory.add_user_message(question)  ← Save │
  │   memory.add_assistant_message(answer) ← Save│
  │                                              │
  │   return answer                              │
  └───────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                    KEY POINTS                                    │
└─────────────────────────────────────────────────────────────────┘

✓ From Question 2 onwards: History is ALWAYS included
✓ Memory persists: Throughout entire chat session
✓ Auto-trimming: Keeps last 6 messages (3 Q&A pairs)
✓ Manual reset: Type 'clear' command
✓ Session end: Exit app = memory destroyed
✓ Fresh start: Each time you run app.py = new empty memory


┌─────────────────────────────────────────────────────────────────┐
│                 EXAMPLE SESSION                                  │
└─────────────────────────────────────────────────────────────────┘

$ python app.py                          ← Start session

You: What is ML?                         ← Q1: No history
AI: Machine learning is...

You: Give example?                       ← Q2: Has [Q1, A1]
AI: For example, in healthcare...

You: More details?                       ← Q3: Has [Q1, A1, Q2, A2]
AI: Sure, let me elaborate...

You: clear                               ← Reset memory
✓ Conversation memory cleared!

You: What is AI?                         ← Q4: No history (fresh)
AI: Artificial intelligence is...

You: exit                                ← End session
Goodbye!

$ python app.py                          ← New session = fresh memory

You: Hello                               ← Q1: No history (new session)
"""

print(__doc__)
