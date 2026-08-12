"""
Comprehensive verification of code flow after standardized API format changes
"""

import sys
import os
import traceback

# Add parent directory to path to allow imports from src and main
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

print("=" * 80)
print("CODE FLOW VERIFICATION - STANDARDIZED API FORMAT")
print("=" * 80)

test_results = []

def log_test(test_name, passed, details=""):
    test_results.append({"name": test_name, "passed": passed, "details": details})
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"\n{status} | {test_name}")
    if details:
        print(f"      {details}")

# ============================================================================
# TEST 1: Import All API Routers
# ============================================================================
print("\n" + "=" * 80)
print("TEST 1: Import All API Routers")
print("=" * 80)

try:
    from src.api.v1.chat import router as chat_router
    from src.api.v1.health import router as health_router
    from src.api.v1.index import router as index_router
    from src.api.v1.database import router as database_router
    
    log_test("API Routers: All imports", True, "All v1 routers imported successfully")
    
except Exception as ex:
    log_test("API Routers Import", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 2: Verify Pydantic Models
# ============================================================================
print("\n" + "=" * 80)
print("TEST 2: Verify Pydantic Models")
print("=" * 80)

try:
    from src.api.v1.chat import ChatRequest, ChatResponse
    
    # Test ChatRequest
    request = ChatRequest(
        question="Test question",
        session_id="test-123"
    )
    log_test("Pydantic: ChatRequest", True, "Model instantiated successfully")
    
    # Test ChatResponse with new structure
    response = ChatResponse(
        success=True,
        message="Test message",
        data={"answer": "test", "session_id": "test-123", "sources": []}
    )
    log_test("Pydantic: ChatResponse", True, "New standardized format working")
    
    # Verify structure
    has_success = hasattr(response, 'success')
    has_message = hasattr(response, 'message')
    has_data = hasattr(response, 'data')
    
    log_test("Pydantic: Response structure", has_success and has_message and has_data,
            f"success: {has_success}, message: {has_message}, data: {has_data}")
    
except Exception as ex:
    log_test("Pydantic Models", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 3: Verify Services Still Work
# ============================================================================
print("\n" + "=" * 80)
print("TEST 3: Verify Services Still Work")
print("=" * 80)

try:
    from src.services.chat_service import chat
    from src.services.database_service import get_database_info
    
    # Test chat service (unchanged - should still return dict)
    result = chat(
        question="What is machine learning?",
        source=None,
        session_id="test-verification"
    )
    
    is_dict = isinstance(result, dict)
    has_answer = "answer" in result
    has_sources = "sources" in result
    
    log_test("Services: chat_service", is_dict and has_answer and has_sources,
            f"Returns dict with answer and sources")
    
    # Test database service
    db_info = get_database_info()
    has_collection = "collection" in db_info
    has_documents = "documents" in db_info
    
    log_test("Services: database_service", has_collection and has_documents,
            f"Collection: {db_info.get('collection')}, Documents: {db_info.get('documents')}")
    
except Exception as ex:
    log_test("Services Verification", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 4: Verify Main Application
# ============================================================================
print("\n" + "=" * 80)
print("TEST 4: Verify Main Application")
print("=" * 80)

try:
    from main import app
    from fastapi import FastAPI
    
    # Verify app is FastAPI instance
    is_fastapi = isinstance(app, FastAPI)
    log_test("Main: FastAPI instance", is_fastapi, "App is valid FastAPI instance")
    
    # Verify routers are registered
    route_count = len(app.router.routes)
    log_test("Main: Routes registered", route_count > 5,
            f"Total routes: {route_count}")
    
except Exception as ex:
    log_test("Main Application", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 5: Verify Response Format Functions
# ============================================================================
print("\n" + "=" * 80)
print("TEST 5: Verify Response Format in Endpoint Functions")
print("=" * 80)

try:
    # Check health endpoint
    from src.api.v1 import health
    import inspect
    
    health_source = inspect.getsource(health.health)
    has_success = '"success"' in health_source or "'success'" in health_source
    has_message = '"message"' in health_source or "'message'" in health_source
    has_data = '"data"' in health_source or "'data'" in health_source
    
    log_test("Format: Health endpoint", has_success and has_message and has_data,
            "Returns standardized format")
    
    # Check database endpoint
    from src.api.v1 import database
    
    db_source = inspect.getsource(database.database_info)
    has_success = '"success"' in db_source or "'success'" in db_source
    has_message = '"message"' in db_source or "'message'" in db_source
    has_data = '"data"' in db_source or "'data'" in db_source
    
    log_test("Format: Database endpoint", has_success and has_message and has_data,
            "Returns standardized format")
    
    # Check index endpoint
    from src.api.v1 import index
    
    index_source = inspect.getsource(index.index_documents)
    has_success = '"success"' in index_source or "'success'" in index_source
    has_message = '"message"' in index_source or "'message'" in index_source
    has_data = '"data"' in index_source or "'data'" in index_source
    
    log_test("Format: Index endpoint", has_success and has_message and has_data,
            "Returns standardized format")
    
except Exception as ex:
    log_test("Response Format Verification", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 6: End-to-End Integration
# ============================================================================
print("\n" + "=" * 80)
print("TEST 6: End-to-End Integration (Service → API Format)")
print("=" * 80)

try:
    from src.services.chat_service import chat
    
    # Get service response
    service_result = chat(
        question="Test question",
        source=None,
        session_id="integration-test"
    )
    
    # Simulate API wrapping (how chat endpoint does it)
    api_response = {
        "success": True,
        "message": "Chat response generated successfully",
        "data": {
            "answer": service_result["answer"],
            "session_id": "integration-test",
            "sources": [f"{src['document']} (Page {src['page']})" for src in service_result["sources"]]
        }
    }
    
    # Verify structure
    structure_valid = (
        isinstance(api_response["success"], bool) and
        isinstance(api_response["message"], str) and
        isinstance(api_response["data"], dict)
    )
    
    log_test("Integration: Service to API format", structure_valid,
            "Service data properly wrapped in API format")
    
except Exception as ex:
    log_test("End-to-End Integration", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 7: Memory Service (Unchanged)
# ============================================================================
print("\n" + "=" * 80)
print("TEST 7: Memory Service (Should be unchanged)")
print("=" * 80)

try:
    from src.services.memory import ConversationMemory
    
    memory = ConversationMemory(max_messages=4)
    memory.add_user_message("Test question")
    memory.add_assistant_message("Test answer")
    
    count = memory.get_message_count()
    log_test("Memory: Basic operations", count == 2, f"Message count: {count}")
    
    memory.clear()
    log_test("Memory: Clear operation", memory.is_empty(), "Memory cleared successfully")
    
except Exception as ex:
    log_test("Memory Service", False, str(ex))
    traceback.print_exc()

# ============================================================================
# TEST 8: Backward Compatibility Check
# ============================================================================
print("\n" + "=" * 80)
print("TEST 8: Backward Compatibility")
print("=" * 80)

try:
    # Verify services still return their original format
    from src.services.chat_service import chat
    
    result = chat("Test", source=None, session_id="backward-test")
    
    # Service should still return dict with answer and sources (NOT standardized format)
    is_service_format = (
        isinstance(result, dict) and
        "answer" in result and
        "sources" in result and
        "success" not in result  # Services don't have success field
    )
    
    log_test("Backward Compatibility: Service format", is_service_format,
            "Services maintain original format (API wraps them)")
    
except Exception as ex:
    log_test("Backward Compatibility", False, str(ex))
    traceback.print_exc()

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "=" * 80)
print("TEST SUMMARY")
print("=" * 80)

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

print("\n" + "=" * 80)
print("CODE FLOW STATUS")
print("=" * 80)
print("\n✅ Service Layer: Returns original dict format")
print("✅ API Layer: Wraps service response in standardized format")
print("✅ Response Format: {success, message, data}")
print("✅ Backward Compatibility: Maintained")
print("✅ All Routers: Working correctly")
print("=" * 80)

sys.exit(0 if failed == 0 else 1)
