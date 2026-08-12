"""Test FastAPI endpoints - requires server to be running"""

import requests
import json
import sys
import time

BASE_URL = "http://localhost:8001"
API_URL = f"{BASE_URL}/api/v1"

print("=" * 70)
print("FASTAPI ENDPOINT TEST")
print("=" * 70)
print(f"\nBase URL: {BASE_URL}")
print(f"API URL: {API_URL}")

test_results = []

def log_test(test_name, passed, details=""):
    test_results.append({"name": test_name, "passed": passed, "details": details})
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"\n{status} | {test_name}")
    if details:
        print(f"      {details}")

# Check if server is running
print("\n" + "=" * 70)
print("Checking Server Status...")
print("=" * 70)

try:
    response = requests.get(BASE_URL, timeout=2)
    print("✓ Server is running!")
except requests.exceptions.ConnectionError:
    print("\n❌ ERROR: FastAPI server is not running!")
    print("\nPlease start the server first:")
    print("  uvicorn main:app --reload")
    print("\nThen run this test again.")
    sys.exit(1)

# ============================================================================
# TEST 1: Root Endpoint
# ============================================================================
print("\n" + "=" * 70)
print("TEST 1: Root Endpoint")
print("=" * 70)

try:
    response = requests.get(BASE_URL)
    is_200 = response.status_code == 200
    log_test("GET /", is_200, f"Status: {response.status_code}")
    
    if is_200:
        data = response.json()
        has_message = "message" in data
        log_test("Root: Response structure", has_message, f"Message: {data.get('message', '')}")
except Exception as ex:
    log_test("Root Endpoint", False, str(ex))

# ============================================================================
# TEST 2: Chat Endpoint (POST /api/v1/chat/)
# ============================================================================
print("\n" + "=" * 70)
print("TEST 2: Chat Endpoint")
print("=" * 70)

try:
    # Test basic chat request
    payload = {
        "question": "What is machine learning?",
        "session_id": "api-test-001",
        "source": None,
        "stream": False
    }
    
    response = requests.post(f"{API_URL}/chat/", json=payload)
    is_200 = response.status_code == 200
    log_test("POST /api/v1/chat/", is_200, f"Status: {response.status_code}")
    
    if is_200:
        data = response.json()
        
        # Check response structure
        has_answer = "answer" in data
        has_session = "session_id" in data
        has_sources = "sources" in data
        log_test("Chat: Response structure", has_answer and has_session and has_sources, 
                f"Keys: {list(data.keys())}")
        
        # Check answer
        answer_valid = isinstance(data["answer"], str) and len(data["answer"]) > 0
        log_test("Chat: Answer field", answer_valid, 
                f"Length: {len(data['answer'])} chars")
        
        # Check session_id
        session_matches = data["session_id"] == "api-test-001"
        log_test("Chat: Session ID", session_matches, 
                f"Session: {data['session_id']}")
        
        # Check sources
        sources_valid = isinstance(data["sources"], list)
        log_test("Chat: Sources field", sources_valid, 
                f"Count: {len(data['sources'])}")
        
    # Test with source filter
    payload_filtered = {
        "question": "What is AI?",
        "session_id": "api-test-002",
        "source": "sample.pdf",
        "stream": False
    }
    
    response = requests.post(f"{API_URL}/chat/", json=payload_filtered)
    log_test("Chat: With source filter", response.status_code == 200, 
            f"Status: {response.status_code}")
    
    # Test without session_id (should default)
    payload_no_session = {
        "question": "Hello",
        "source": None,
        "stream": False
    }
    
    response = requests.post(f"{API_URL}/chat/", json=payload_no_session)
    if response.status_code == 200:
        data = response.json()
        has_default = data.get("session_id") == "default"
        log_test("Chat: Default session", has_default, 
                f"Session: {data.get('session_id')}")
    
except Exception as ex:
    log_test("Chat Endpoint", False, str(ex))

# ============================================================================
# TEST 3: Session Management
# ============================================================================
print("\n" + "=" * 70)
print("TEST 3: Session Management")
print("=" * 70)

try:
    # Create a session with multiple messages
    session_id = "api-test-session-management"
    
    # First message
    response1 = requests.post(f"{API_URL}/chat/", json={
        "question": "What is machine learning?",
        "session_id": session_id
    })
    log_test("Session: First message", response1.status_code == 200, 
            f"Status: {response1.status_code}")
    
    # Second message (should use memory)
    response2 = requests.post(f"{API_URL}/chat/", json={
        "question": "Tell me more about it",
        "session_id": session_id
    })
    log_test("Session: Follow-up message", response2.status_code == 200, 
            f"Status: {response2.status_code}")
    
    # List sessions
    response = requests.get(f"{API_URL}/chat/sessions")
    is_200 = response.status_code == 200
    log_test("GET /api/v1/chat/sessions", is_200, f"Status: {response.status_code}")
    
    if is_200:
        data = response.json()
        has_sessions = "sessions" in data
        log_test("Sessions: Response structure", has_sessions, 
                f"Keys: {list(data.keys())}")
        
        if has_sessions:
            sessions = data["sessions"]
            session_count = len(sessions)
            log_test("Sessions: List content", session_count > 0, 
                    f"Active sessions: {session_count}")
            
            # Check if our test session exists
            if session_id in sessions:
                session_data = sessions[session_id]
                log_test("Sessions: Test session exists", True, 
                        f"Messages: {session_data.get('message_count', 0)}")
    
except Exception as ex:
    log_test("Session Management", False, str(ex))

# ============================================================================
# TEST 4: Clear Session
# ============================================================================
print("\n" + "=" * 70)
print("TEST 4: Clear Session")
print("=" * 70)

try:
    # Create a session
    test_session = "api-test-clear"
    requests.post(f"{API_URL}/chat/", json={
        "question": "Test message",
        "session_id": test_session
    })
    
    # Clear the session
    response = requests.delete(f"{API_URL}/chat/session/{test_session}")
    is_200 = response.status_code == 200
    log_test("DELETE /api/v1/chat/session/{id}", is_200, f"Status: {response.status_code}")
    
    if is_200:
        data = response.json()
        has_message = "message" in data
        log_test("Clear: Response structure", has_message, 
                f"Message: {data.get('message', '')}")
    
    # Try to clear non-existent session
    response = requests.delete(f"{API_URL}/chat/session/nonexistent-session")
    is_404 = response.status_code == 404
    log_test("Clear: Non-existent session", is_404, 
            f"Status: {response.status_code} (expected 404)")
    
except Exception as ex:
    log_test("Clear Session", False, str(ex))

# ============================================================================
# TEST 5: Error Handling
# ============================================================================
print("\n" + "=" * 70)
print("TEST 5: Error Handling")
print("=" * 70)

try:
    # Test with missing required field
    response = requests.post(f"{API_URL}/chat/", json={
        "session_id": "test"
        # Missing "question"
    })
    is_error = response.status_code in [400, 422]
    log_test("Error: Missing required field", is_error, 
            f"Status: {response.status_code} (expected 400/422)")
    
    # Test with invalid data type
    response = requests.post(f"{API_URL}/chat/", json={
        "question": 123,  # Should be string
        "session_id": "test"
    })
    is_error = response.status_code in [400, 422]
    log_test("Error: Invalid data type", is_error, 
            f"Status: {response.status_code} (expected 400/422)")
    
except Exception as ex:
    log_test("Error Handling", False, str(ex))

# ============================================================================
# TEST 6: Performance
# ============================================================================
print("\n" + "=" * 70)
print("TEST 6: Performance")
print("=" * 70)

try:
    # Measure response time
    start_time = time.time()
    response = requests.post(f"{API_URL}/chat/", json={
        "question": "What is AI?",
        "session_id": "perf-test"
    })
    elapsed = time.time() - start_time
    
    is_fast = elapsed < 60  # Should respond within 60 seconds
    log_test("Performance: Response time", is_fast, 
            f"Time: {elapsed:.2f}s (threshold: 60s)")
    
except Exception as ex:
    log_test("Performance", False, str(ex))

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
    print("\n🎉 ALL API TESTS PASSED!")

print("\n" + "=" * 70)
print("API ENDPOINT VALIDATION COMPLETE")
print("=" * 70)

sys.exit(0 if failed == 0 else 1)
