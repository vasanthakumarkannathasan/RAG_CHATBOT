"""Test script to verify source citation functionality"""

from src.services.chat_service import chat
from src.utils.logger import logger

print("=" * 70)
print("Source Citation Test")
print("=" * 70)

test_question = "What is machine learning?"

# Test 1: Get answer with citations
print(f"\nQuestion: {test_question}")
print("-" * 70)

try:
    answer = chat(test_question, source=None)
    print(f"\n{answer}")
    print("-" * 70)
    
    # Check if citations are included
    if "Sources" in answer:
        print("\n✓ Citations are included in the response!")
        
        # Check if it has the emoji and page info
        if "📄" in answer and "Page" in answer:
            print("✓ Citation format is correct (includes emoji and page numbers)")
        else:
            print("✗ WARNING: Citation format might be incorrect")
    else:
        print("\n✗ WARNING: Citations are NOT included in the response!")
        
except Exception as ex:
    print(f"\n✗ Error occurred: {ex}")
    logger.exception("Test failed")

print("\n" + "=" * 70)
print("Source Citation Test Complete")
print("=" * 70)
