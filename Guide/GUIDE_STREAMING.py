"""
STREAMING RESPONSE - IMPLEMENTATION GUIDE
==========================================

┌─────────────────────────────────────────────────────────────────┐
│                    HOW STREAMING WORKS                           │
└─────────────────────────────────────────────────────────────────┘

Traditional (Non-Streaming):
  User asks question
       ↓
  Wait for complete response (10-30 seconds)
       ↓
  Display entire answer at once
  

Streaming:
  User asks question
       ↓
  Display answer word-by-word as it's generated (real-time)
       ↓
  Better user experience (no long wait)


┌─────────────────────────────────────────────────────────────────┐
│                 IMPLEMENTATION LAYERS                            │
└─────────────────────────────────────────────────────────────────┘

Layer 1: LLM (llm.py)
┌───────────────────────────────────────────────────────────┐
│ generate_answer(prompt, stream=False)                    │
│                                                           │
│ If stream=False:                                         │
│   → Returns complete string                              │
│   → "Machine learning is..."                             │
│                                                           │
│ If stream=True:                                          │
│   → Returns generator                                    │
│   → Yields: "Machine", " learning", " is", "..."       │
└───────────────────────────────────────────────────────────┘

Layer 2: Chat Service (chat_service.py)
┌───────────────────────────────────────────────────────────┐
│ chat(question, memory, stream=False)                     │
│                                                           │
│ If stream=False:                                         │
│   → Returns: answer + citations (complete string)        │
│                                                           │
│ If stream=True:                                          │
│   → Returns generator                                    │
│   → Yields answer chunks, then citations                 │
│   → Updates memory after streaming completes             │
└───────────────────────────────────────────────────────────┘

Layer 3: Application (app.py)
┌───────────────────────────────────────────────────────────┐
│ if streaming_enabled:                                     │
│     for chunk in chat(..., stream=True):                 │
│         print(chunk, end="", flush=True)  ← Real-time   │
│ else:                                                     │
│     answer = chat(..., stream=False)                     │
│     print(answer)  ← All at once                         │
└───────────────────────────────────────────────────────────┘


┌─────────────────────────────────────────────────────────────────┐
│                     CODE FLOW                                    │
└─────────────────────────────────────────────────────────────────┘

Streaming Mode (stream=True):
─────────────────────────────
1. User: "What is ML?"
   
2. app.py receives question
   ↓
3. Calls: chat(question, stream=True)
   ↓
4. chat_service.py:
   - Retrieves documents
   - Builds prompt with history
   - Calls generate_answer(prompt, stream=True)
   ↓
5. llm.py:
   - Creates Ollama stream
   - Returns generator
   ↓
6. Chunks flow back:
   "Machine" → print("Machine")
   " learning" → print(" learning")
   " is" → print(" is")
   " a" → print(" a")
   ...
   "data." → print("data.")
   
7. After streaming completes:
   - Memory updated with full answer
   - Citations yielded
   - Citations printed


Non-Streaming Mode (stream=False):
──────────────────────────────────
1. User: "What is ML?"
   
2. app.py receives question
   ↓
3. Calls: chat(question, stream=False)
   ↓
4. chat_service.py:
   - Retrieves documents
   - Builds prompt
   - Calls generate_answer(prompt, stream=False)
   ↓
5. llm.py:
   - Waits for complete response
   - Returns full string
   ↓
6. Complete answer returned:
   "Machine learning is a subset of AI..."
   
7. Memory updated
8. Citations added
9. Full response printed at once


┌─────────────────────────────────────────────────────────────────┐
│                   KEY FEATURES                                   │
└─────────────────────────────────────────────────────────────────┘

✓ Real-time streaming: See response as it's generated
✓ Backward compatible: Non-streaming still works
✓ Memory integration: Works with conversation history
✓ Source citations: Included at end of stream
✓ Toggle command: Type 'stream' to switch modes
✓ Error handling: Graceful fallback on failures


┌─────────────────────────────────────────────────────────────────┐
│                  USAGE IN APP                                    │
└─────────────────────────────────────────────────────────────────┘

Commands:
  clear  → Reset conversation memory
  stream → Toggle streaming ON/OFF
  exit   → Quit application

Example Session:
────────────────
$ python app.py

✓ Streaming mode: ON

You: What is machine learning?
Filter by source: [Enter]

AI: Machine learning is a subset of artificial intelligence...
    [text appears word by word in real-time]

Sources
📄 sample.pdf (Page 1)

You: stream
✓ Streaming mode: OFF

You: Give an example
Filter by source: [Enter]

AI: [Complete answer appears all at once after waiting]

Sources
📄 sample.pdf (Page 4)


┌─────────────────────────────────────────────────────────────────┐
│              TECHNICAL DETAILS                                   │
└─────────────────────────────────────────────────────────────────┘

Generator Functions:
────────────────────
def generate_answer(prompt, stream=False):
    if stream:
        return _stream_response(...)  ← Returns generator
    else:
        return complete_string  ← Returns string

def _stream_response(client, messages):
    for chunk in client.chat(..., stream=True):
        yield chunk["message"]["content"]  ← Yields chunks

Memory Management:
──────────────────
- Streaming: Collects full answer during streaming
- Updates memory AFTER streaming completes
- Ensures conversation history is accurate

Output Flushing:
────────────────
print(chunk, end="", flush=True)
      ↑      ↑       ↑
      │      │       └─ Immediate output (no buffering)
      │      └─ No newline after each chunk
      └─ Print the chunk

Performance:
────────────
- Streaming: User sees output immediately (better UX)
- Non-streaming: Slightly faster (no chunk overhead)
- Same total time to complete


┌─────────────────────────────────────────────────────────────────┐
│                  BENEFITS                                        │
└─────────────────────────────────────────────────────────────────┘

1. Better User Experience
   - No long waits
   - Immediate feedback
   - ChatGPT-like feel

2. Flexibility
   - Can toggle streaming on/off
   - Works with all existing features

3. Professional
   - Modern chat interface
   - Industry-standard pattern

4. Maintainable
   - Clean implementation
   - Well-documented
   - Backward compatible
"""

print(__doc__)
