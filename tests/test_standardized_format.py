"""
Test script to verify standardized API response format
All endpoints should return: {"success": bool, "message": str, "data": dict}
"""

import requests
import json

BASE_URL = "http://localhost:8000"

print("=" * 80)
print("TESTING STANDARDIZED API RESPONSE FORMAT")
print("=" * 80)

def test_endpoint(method, url, json_data=None, expected_keys=["success", "message", "data"]):
    """Test an endpoint and verify response structure"""
    print(f"\n{'='*80}")
    print(f"{method} {url}")
    print(f"{'='*80}")
    
    try:
        if method == "GET":
            response = requests.get(url)
        elif method == "POST":
            response = requests.post(url, json=json_data)
        elif method == "DELETE":
            response = requests.delete(url)
        else:
            print(f"❌ Unsupported method: {method}")
            return False
        
        print(f"Status Code: {response.status_code}")
        
        if response.status_code in [200, 201]:
            data = response.json()
            print(f"\nResponse:")
            print(json.dumps(data, indent=2))
            
            # Check if all expected keys are present
            missing_keys = [key for key in expected_keys if key not in data]
            if missing_keys:
                print(f"\n❌ FAIL - Missing keys: {missing_keys}")
                return False
            
            # Verify success is boolean
            if not isinstance(data.get("success"), bool):
                print(f"\n❌ FAIL - 'success' is not boolean: {type(data.get('success'))}")
                return False
            
            # Verify message is string
            if not isinstance(data.get("message"), str):
                print(f"\n❌ FAIL - 'message' is not string: {type(data.get('message'))}")
                return False
            
            # Verify data is dict
            if not isinstance(data.get("data"), dict):
                print(f"\n❌ FAIL - 'data' is not dict: {type(data.get('data'))}")
                return False
            
            print(f"\n✅ PASS - Standard format verified")
            return True
        else:
            print(f"\n❌ FAIL - Error: {response.text}")
            return False
    
    except requests.exceptions.ConnectionError:
        print("\n❌ Server not running!")
        print("Please start the server: python -m uvicorn main:app --reload")
        return False
    except Exception as ex:
        print(f"\n❌ Error: {ex}")
        return False

# Track results
results = []

print("\n" + "="*80)
print("Starting tests... (Make sure server is running)")
print("="*80)

# Test 1: Root endpoint
results.append(("Root", test_endpoint("GET", f"{BASE_URL}/")))

# Test 2: Health endpoint
results.append(("Health", test_endpoint("GET", f"{BASE_URL}/api/v1/health")))

# Test 3: Database info endpoint
results.append(("Database Info", test_endpoint("GET", f"{BASE_URL}/api/v1/database")))

# Test 4: Chat endpoint
chat_payload = {
    "question": "What is machine learning?",
    "session_id": "test-standardized-format"
}
results.append(("Chat", test_endpoint("POST", f"{BASE_URL}/api/v1/chat/", chat_payload)))

# Test 5: List sessions endpoint
results.append(("List Sessions", test_endpoint("GET", f"{BASE_URL}/api/v1/chat/sessions")))

# Test 6: Clear session endpoint
results.append(("Clear Session", test_endpoint("DELETE", f"{BASE_URL}/api/v1/chat/session/test-standardized-format")))

# Test 7: Index endpoint (optional - only if you want to actually index)
# Uncomment to test indexing
# results.append(("Index Documents", test_endpoint("POST", f"{BASE_URL}/api/v1/index")))

# Summary
print("\n" + "="*80)
print("TEST SUMMARY")
print("="*80)

passed = sum(1 for _, result in results if result)
failed = sum(1 for _, result in results if not result)
total = len(results)

print(f"\nTotal Tests: {total}")
print(f"✅ Passed: {passed}")
print(f"❌ Failed: {failed}")
print(f"Success Rate: {(passed/total*100):.1f}%")

if failed > 0:
    print("\n❌ Failed Tests:")
    for name, result in results:
        if not result:
            print(f"  • {name}")
else:
    print("\n🎉 ALL TESTS PASSED!")
    print("\n✅ All API endpoints follow the standard format:")
    print("   {")
    print('     "success": true,')
    print('     "message": "...",')
    print('     "data": {...}')
    print("   }")

print("\n" + "="*80)
