"""Comprehensive test of entire code flow - Services and API"""

import sys
import traceback

print("=" * 70)
print("COMPREHENSIVE ENTERPRISE RAG - CODE FLOW TEST")
print("=" * 70)

# Test Results Tracker
test_results = []

def log_test(test_name, passed, details=""):
    test_results.append({"name": test_name, "passed": passed, "details": details})
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"\n{status} | {test_name}")
    if details:
        print(f"      {details}")

# ============================================================================
# TEST 1: Database Service
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: Database Service")
print("=" * 70)

try:
    from src.services.database import get_vector_db, get_collection_count
    
    # Test vector DB connection
    vector_db = get_vector_db()
    log_test("Database: get_vector_db()", True, f"Type: {type(vector_db).__name__}")
    
    # Test collection count
    count = get_collection_count()
    log_test("Database: get_collection_count()", count > 0, f"Count: {count} documents")
    
except Exception as ex:
    log_test("Database Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 2: Retrieval Service
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: Retrieval Service")
print("=" * 70)

try:
    from src.services.retrieval import retrieve_documents
    
    # Test basic retrieval
    docs = retrieve_documents("What is machine learning?", k=3)
    log_test("Retrieval: Basic query", len(docs) > 0, f"Retrieved {len(docs)} documents")
    
    # Verify document structure
    if docs:
        doc = docs[0]
        has_content = hasattr(doc, 'page_content') and len(doc.page_content) > 0
        has_metadata = hasattr(doc, 'metadata') and 'source' in doc.metadata
        log_test("Retrieval: Document structure", has_content and has_metadata, 
                f"Content length: {len(doc.page_content)}, Metadata keys: {list(doc.metadata.keys())}")
    
    # Test with source filter
    docs_filtered = retrieve_documents("machine learning", k=3, source="sample.pdf")
    log_test("Retrieval: Source filtering", len(docs_filtered) > 0, f"Filtered to {len(docs_filtered)} documents")
    
except Exception as ex:
    log_test("Retrieval Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 3: Prompt Builder Service
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: Prompt Builder Service")
print("=" * 70)

try:
    from src.services.prompt_builder import build_prompt
    from langchain_core.documents import Document
    
    # Create mock documents
    mock_docs = [
        Document(page_content="Machine learning is a subset of AI.", metadata={"source": "test.pdf", "page": 0}),
        Document(page_content="It enables systems to learn from data.", metadata={"source": "test.pdf", "page": 1})
    ]
    
    # Test without conversation history
    prompt = build_prompt("What is ML?", mock_docs)
    has_context = "Machine learning" in prompt
    has_question = "What is ML?" in prompt
    log_test("Prompt Builder: Basic prompt", has_context and has_question, 
            f"Prompt length: {len(prompt)} chars")
    
    # Test with conversation history
    history = [
        {"role": "user", "content": "Hello"},
        {"role": "assistant", "content": "Hi there"}
    ]
    prompt_with_history = build_prompt("What is ML?", mock_docs, conversation_history=history)
    has_history = "Conversation History" in prompt_with_history
    log_test("Prompt Builder: With history", has_history, 
            f"History included: {has_history}")
    
except Exception as ex:
    log_test("Prompt Builder Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 4: LLM Service
# ============================================================================
print("\n" + "=" * 70)
print("TEST 4: LLM Service")
print("=" * 70)

try:
    from src.services.llm import generate_answer
    
    # Test basic answer generation
    test_prompt = "Answer in one sentence: What is 2+2?"
    answer = generate_answer(test_prompt)
    log_test("LLM: generate_answer()", len(answer) > 0, f"Answer length: {len(answer)} chars")
    
    # Verify it's a string
    log_test("LLM: Return type", isinstance(answer, str), f"Type: {type(answer).__name__}")
    
except Exception as ex:
    log_test("LLM Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 5: Chat Service (Integration)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 5: Chat Service - Full Integration")
print("=" * 70)

try:
    from src.services.chat_service import chat
    
    # Test basic chat flow
    result = chat(
        question="What is machine learning?",
        source=None,
        session_id="test-session-001"
    )
    
    # Verify return structure
    is_dict = isinstance(result, dict)
    has_answer = "answer" in result
    has_sources = "sources" in result
    log_test("Chat Service: Return structure", is_dict and has_answer and has_sources, 
            f"Keys: {list(result.keys())}")
    
    # Verify answer
    answer_valid = isinstance(result["answer"], str) and len(result["answer"]) > 0
    log_test("Chat Service: Answer field", answer_valid, 
            f"Answer length: {len(result['answer'])} chars")
    
    # Verify sources structure
    sources_valid = isinstance(result["sources"], list)
    if sources_valid and len(result["sources"]) > 0:
        first_source = result["sources"][0]
        has_doc = "document" in first_source
        has_page = "page" in first_source
        sources_valid = has_doc and has_page
        log_test("Chat Service: Sources structure", sources_valid, 
                f"Source count: {len(result['sources'])}, Keys: {list(first_source.keys())}")
    else:
        log_test("Chat Service: Sources structure", sources_valid, "Empty sources list")
    
    # Test with source filter
    result_filtered = chat(
        question="What is AI?",
        source="sample.pdf",
        session_id="test-session-002"
    )
    log_test("Chat Service: With source filter", isinstance(result_filtered, dict), 
            f"Filtered sources: {len(result_filtered['sources'])}")
    
except Exception as ex:
    log_test("Chat Service Integration", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 6: Memory Service
# ============================================================================
print("\n" + "=" * 70)
print("TEST 6: Memory Service")
print("=" * 70)

try:
    from src.services.memory import ConversationMemory
    
    memory = ConversationMemory(max_messages=4)
    
    # Test adding messages
    memory.add_user_message("Hello")
    memory.add_assistant_message("Hi there")
    messages = memory.get_messages()
    log_test("Memory: Add messages", len(messages) == 2, f"Message count: {len(messages)}")
    
    # Test message count
    count = memory.get_message_count()
    log_test("Memory: get_message_count()", count == 2, f"Count: {count}")
    
    # Test is_empty
    is_empty = memory.is_empty()
    log_test("Memory: is_empty()", not is_empty, f"Empty: {is_empty}")
    
    # Test clear
    memory.clear()
    log_test("Memory: clear()", memory.is_empty(), f"After clear: {memory.get_message_count()} messages")
    
    # Test max_messages trimming
    memory2 = ConversationMemory(max_messages=4)
    for i in range(5):
        memory2.add_user_message(f"Question {i}")
        memory2.add_assistant_message(f"Answer {i}")
    
    final_count = memory2.get_message_count()
    log_test("Memory: Trimming (max_messages)", final_count == 4, 
            f"After adding 10, kept {final_count} (max 4)")
    
except Exception as ex:
    log_test("Memory Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 7: API Models
# ============================================================================
print("\n" + "=" * 70)
print("TEST 7: API Models (Pydantic)")
print("=" * 70)

try:
    from src.api.v1.chat import ChatRequest, ChatResponse
    
    # Test ChatRequest
    request = ChatRequest(
        question="What is AI?",
        session_id="test-123",
        source="test.pdf",
        stream=False
    )
    log_test("API: ChatRequest model", True, 
            f"Question: {request.question}, Session: {request.session_id}")
    
    # Test ChatResponse
    response = ChatResponse(
        answer="AI is artificial intelligence.",
        session_id="test-123",
        sources=["test.pdf (Page 1)"]
    )
    log_test("API: ChatResponse model", True, 
            f"Answer length: {len(response.answer)}, Sources: {len(response.sources)}")
    
except Exception as ex:
    log_test("API Models", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 8: Exception Handling
# ============================================================================
print("\n" + "=" * 70)
print("TEST 8: Exception Hierarchy")
print("=" * 70)

try:
    from src.exceptions.base_exception import EnterpriseRAGException
    from src.exceptions.database_exception import DatabaseException
    from src.exceptions.embedding_exception import EmbeddingException
    from src.exceptions.llm_exception import LLMException
    from src.exceptions.pdf_exception import PDFException
    
    # Test exception inheritance
    db_ex = DatabaseException("Test error")
    is_base = isinstance(db_ex, EnterpriseRAGException)
    log_test("Exceptions: Inheritance chain", is_base, 
            "DatabaseException extends EnterpriseRAGException")
    
    # Test all exception types
    exceptions = [
        ("DatabaseException", DatabaseException),
        ("EmbeddingException", EmbeddingException),
        ("LLMException", LLMException),
        ("PDFException", PDFException)
    ]
    
    all_valid = all(issubclass(exc_class, EnterpriseRAGException) for _, exc_class in exceptions)
    log_test("Exceptions: All types valid", all_valid, 
            f"Checked {len(exceptions)} exception types")
    
except Exception as ex:
    log_test("Exception Hierarchy", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 9: Edge Cases
# ============================================================================
print("\n" + "=" * 70)
print("TEST 9: Edge Cases & Error Handling")
print("=" * 70)

try:
    # Test with empty question
    try:
        result = chat(question="", source=None)
        log_test("Edge Case: Empty question", True, "Handled gracefully")
    except Exception as edge_ex:
        log_test("Edge Case: Empty question", False, f"Error: {edge_ex}")
    
    # Test with non-existent source
    result = chat(question="test", source="nonexistent.pdf")
    log_test("Edge Case: Non-existent source", isinstance(result, dict), 
            f"Sources found: {len(result['sources'])}")
    
    # Test with very long question
    long_question = "What is machine learning? " * 50
    result = chat(question=long_question, source=None)
    log_test("Edge Case: Long question", isinstance(result, dict), 
            f"Question length: {len(long_question)} chars")
    
except Exception as ex:
    log_test("Edge Cases", False, str(ex))

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 70)
print("TEST SUMMARY")
print("=" * 70)

passed = sum(1 for t in test_results if t["passed"])
failed = sum(1 for t in test_results if not t["passed"])
total = len(test_results)

print(f"\nTotal Tests: {total}")
print(f"✓ Passed: {passed}")
print(f"✗ Failed: {failed}")
print(f"Success Rate: {(passed/total*100):.1f}%")

if failed > 0:
    print("\n❌ Failed Tests:")
    for test in test_results:
        if not test["passed"]:
            print(f"  • {test['name']}")
            if test["details"]:
                print(f"    {test['details']}")
else:
    print("\n🎉 ALL TESTS PASSED!")

print("\n" + "=" * 70)
print("CODE FLOW VALIDATION COMPLETE")
print("=" * 70)

# Exit with appropriate code
sys.exit(0 if failed == 0 else 1)
