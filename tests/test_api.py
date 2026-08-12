"""Test script to verify the FastAPI application is working"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 70)
print("FastAPI Enterprise RAG - API Test")
print("=" * 70)

# Test 1: Root endpoint
print("\n=== Test 1: Root Endpoint ===")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✓ Root endpoint working!")
except Exception as ex:
    print(f"✗ Error: {ex}")
    print("Make sure the API is running: uvicorn main:app --reload")

# Test 2: Chat endpoint
print("\n=== Test 2: Chat Endpoint ===")
try:
    payload = {
        "question": "What is machine learning?",
        "session_id": "test-session",
        "source": None,
        "stream": False
    }
    
    response = requests.post(f"{BASE_URL}/api/v1/chat/", json=payload)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"\nAnswer: {data['answer'][:200]}...")
        print(f"\nSession ID: {data['session_id']}")
        print(f"Sources: {data['sources']}")
        print("\n✓ Chat endpoint working!")
    else:
        print(f"✗ Error: {response.text}")
        
except Exception as ex:
    print(f"✗ Error: {ex}")

# Test 3: List sessions
print("\n=== Test 3: List Sessions ===")
try:
    response = requests.get(f"{BASE_URL}/api/v1/chat/sessions")
    print(f"Status: {response.status_code}")
    print(f"Sessions: {json.dumps(response.json(), indent=2)}")
    print("✓ Sessions endpoint working!")
except Exception as ex:
    print(f"✗ Error: {ex}")

# Test 4: Clear session
print("\n=== Test 4: Clear Session ===")
try:
    response = requests.delete(f"{BASE_URL}/api/v1/chat/session/test-session")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✓ Clear session endpoint working!")
except Exception as ex:
    print(f"✗ Error: {ex}")

print("\n" + "=" * 70)
print("API Test Complete")
print("=" * 70)
