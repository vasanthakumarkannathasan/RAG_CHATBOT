"""
Test 10: Prompt Builder
------------------------
Tests prompt construction: context, query, answer, metadata.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.retrieval import retrieve_documents
from src.services.prompt_builder import build_prompt, SYSTEM_PROMPT
from langchain_core.documents import Document

def test_prompt_builder():
    """Test prompt builder with detailed information"""
    print("\n" + "="*80)
    print("TEST 10: PROMPT BUILDER")
    print("="*80)
    
    # Test query
    user_query = "What is Docker?"
    
    print(f"\n📝 User Query: \"{user_query}\"")
    
    # Retrieve documents
    print(f"\n{'─'*80}")
    print("STEP 1: Retrieving Context Documents")
    print(f"{'─'*80}")
    
    try:
        documents = retrieve_documents(user_query, k=2)
        print(f"   ✅ Retrieved {len(documents)} documents")
    except Exception as e:
        print(f"   ❌ Retrieval failed: {str(e)}")
        print(f"   Using mock documents for demonstration...")
        
        # Create mock documents
        documents = [
            Document(
                page_content="Docker is a platform for developing, shipping, and running applications in containers. It provides isolation and portability.",
                metadata={"source": "docker.pdf", "page": 1}
            ),
            Document(
                page_content="Containers are lightweight, standalone packages that include everything needed to run an application: code, runtime, libraries, and system tools.",
                metadata={"source": "containers.pdf", "page": 3}
            )
        ]
    
    # Display retrieved documents
    print(f"\n📄 Retrieved Documents:")
    total_context_chars = 0
    
    for idx, doc in enumerate(documents, 1):
        print(f"\n   Document {idx}:")
        print(f"      Source: {doc.metadata.get('source', 'unknown')}")
        print(f"      Page: {doc.metadata.get('page', 'N/A')}")
        print(f"      Length: {len(doc.page_content)} characters")
        content_preview = doc.page_content[:150].replace('\n', ' ')
        print(f"      Preview: {content_preview}...")
        total_context_chars += len(doc.page_content)
    
    print(f"\n   Total context: {total_context_chars} characters")
    
    # Test Case 1: Without conversation history
    print(f"\n{'='*80}")
    print("TEST CASE 1: Prompt Without Conversation History")
    print(f"{'='*80}")
    
    print(f"\n🔧 Building prompt...")
    prompt_no_history = build_prompt(
        question=user_query,
        documents=documents,
        conversation_history=None
    )
    
    print(f"\n✅ Prompt built successfully")
    print(f"   Total length: {len(prompt_no_history)} characters")
    print(f"   Estimated tokens: ~{len(prompt_no_history.split())} words")
    
    # Display prompt structure
    print(f"\n{'─'*80}")
    print("PROMPT STRUCTURE")
    print(f"{'─'*80}")
    
    print(f"\n┌{'─'*78}┐")
    print(f"│ 1. SYSTEM PROMPT" + " "*61 + "│")
    print(f"└{'─'*78}┘")
    print(f"\n{SYSTEM_PROMPT}")
    
    print(f"\n┌{'─'*78}┐")
    print(f"│ 2. CONTEXT" + " "*67 + "│")
    print(f"└{'─'*78}┘")
    
    for idx, doc in enumerate(documents, 1):
        print(f"\n   Context {idx}:")
        print(f"   {doc.page_content}")
    
    print(f"\n┌{'─'*78}┐")
    print(f"│ 3. CURRENT QUESTION" + " "*58 + "│")
    print(f"└{'─'*78}┘")
    print(f"\n   {user_query}")
    
    # Metadata analysis
    print(f"\n{'─'*80}")
    print("METADATA INFORMATION")
    print(f"{'─'*80}")
    
    print(f"\n📊 Context Metadata:")
    for idx, doc in enumerate(documents, 1):
        print(f"\n   Document {idx} Metadata:")
        for key, value in doc.metadata.items():
            print(f"      • {key}: {value}")
    
    print(f"\n🔗 Metadata Purpose:")
    print(f"   • Source tracking: Identify which document provided the answer")
    print(f"   • Page reference: Enable precise citation")
    print(f"   • Context filtering: Filter by specific documents if needed")
    
    # Test Case 2: With conversation history
    print(f"\n{'='*80}")
    print("TEST CASE 2: Prompt With Conversation History")
    print(f"{'='*80}")
    
    conversation_history = [
        {"role": "user", "content": "What is containerization?"},
        {"role": "assistant", "content": "Containerization is a lightweight form of virtualization..."},
        {"role": "user", "content": "How does it differ from VMs?"}
    ]
    
    print(f"\n📜 Conversation History ({len(conversation_history)} messages):")
    for idx, msg in enumerate(conversation_history, 1):
        role = "User" if msg["role"] == "user" else "Assistant"
        content_preview = msg["content"][:80]
        print(f"   {idx}. {role}: {content_preview}...")
    
    print(f"\n🔧 Building prompt with history...")
    prompt_with_history = build_prompt(
        question=user_query,
        documents=documents,
        conversation_history=conversation_history
    )
    
    print(f"\n✅ Prompt built successfully")
    print(f"   Total length: {len(prompt_with_history)} characters")
    print(f"   Estimated tokens: ~{len(prompt_with_history.split())} words")
    
    # Display history section
    print(f"\n┌{'─'*78}┐")
    print(f"│ CONVERSATION HISTORY SECTION" + " "*49 + "│")
    print(f"└{'─'*78}┘")
    
    print("\n================================================")
    print("Conversation History")
    for msg in conversation_history:
        role = "User" if msg["role"] == "user" else "Assistant"
        print(f"{role}: {msg['content']}")
    print("================================================")
    
    # Prompt comparison
    print(f"\n{'─'*80}")
    print("PROMPT COMPARISON")
    print(f"{'─'*80}")
    
    print(f"\n📊 Size Comparison:")
    print(f"   Without history: {len(prompt_no_history)} characters")
    print(f"   With history   : {len(prompt_with_history)} characters")
    print(f"   Difference     : {len(prompt_with_history) - len(prompt_no_history)} characters")
    print(f"   Increase       : {((len(prompt_with_history) / len(prompt_no_history) - 1) * 100):.1f}%")
    
    # Prompt components breakdown
    print(f"\n{'='*80}")
    print("PROMPT COMPONENTS BREAKDOWN")
    print(f"{'='*80}")
    
    system_prompt_len = len(SYSTEM_PROMPT)
    context_len = sum(len(doc.page_content) for doc in documents)
    query_len = len(user_query)
    history_len = len(prompt_with_history) - len(prompt_no_history)
    formatting_len = len(prompt_no_history) - system_prompt_len - context_len - query_len
    
    total_len = len(prompt_with_history)
    
    print(f"\n📊 Component Sizes:")
    print(f"   1. System Prompt      : {system_prompt_len:5d} chars ({system_prompt_len/total_len*100:5.1f}%)")
    print(f"   2. Context Documents  : {context_len:5d} chars ({context_len/total_len*100:5.1f}%)")
    print(f"   3. User Query         : {query_len:5d} chars ({query_len/total_len*100:5.1f}%)")
    print(f"   4. Conversation Hist  : {history_len:5d} chars ({history_len/total_len*100:5.1f}%)")
    print(f"   5. Formatting/Dividers: {formatting_len:5d} chars ({formatting_len/total_len*100:5.1f}%)")
    print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total                 : {total_len:5d} chars")
    
    # Token estimation
    print(f"\n📏 Token Estimation (approximate):")
    words = len(prompt_with_history.split())
    estimated_tokens = int(words * 1.3)  # Rough estimate: 1 word ≈ 1.3 tokens
    print(f"   • Words: {words}")
    print(f"   • Estimated tokens: ~{estimated_tokens}")
    print(f"   • Note: Actual tokens may vary by tokenizer")
    
    # Summary
    print(f"\n{'='*80}")
    print("PROMPT BUILDER SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n🎯 Purpose:")
    print(f"   • Combine system instructions, context, and query")
    print(f"   • Provide LLM with all necessary information")
    print(f"   • Include conversation history for context")
    print(f"   • Structure data for optimal LLM understanding")
    
    print(f"\n🔧 Components:")
    print(f"   1. System Prompt: Instructions for LLM behavior")
    print(f"   2. Conversation History: Previous exchanges (optional)")
    print(f"   3. Context: Retrieved documents from vector DB")
    print(f"   4. Current Question: User's current query")
    
    print(f"\n📊 Data Passed to LLM:")
    print(f"   • User query: \"{user_query}\"")
    print(f"   • Context documents: {len(documents)}")
    print(f"   • Total context chars: {context_len}")
    print(f"   • Conversation history: {len(conversation_history) if conversation_history else 0} messages")
    print(f"   • Metadata: Source and page information")
    
    print(f"\n⚡ Next Step:")
    print(f"   • Prompt is sent to LLM for answer generation")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_prompt_builder()
