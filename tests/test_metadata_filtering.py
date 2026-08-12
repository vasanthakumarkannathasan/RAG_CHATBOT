"""Test script to verify metadata filtering functionality"""

from src.services.retrieval import retrieve_documents
from src.utils.logger import logger

print("=" * 70)
print("Metadata Filtering Test")
print("=" * 70)

test_question = "What is machine learning?"

# Test 1: Retrieve without filter (all documents)
print("\n=== Test 1: No Filter (Search All Documents) ===")
try:
    docs_all = retrieve_documents(test_question, k=3, source=None)
    print(f"✓ Retrieved {len(docs_all)} documents")
    for i, doc in enumerate(docs_all, 1):
        print(f"\n  Document {i}:")
        print(f"    Source: {doc.metadata.get('source', 'N/A')}")
        print(f"    Page: {doc.metadata.get('page', 'N/A')}")
        print(f"    Content preview: {doc.page_content[:100]}...")
except Exception as ex:
    print(f"✗ Error: {ex}")

# Test 2: Retrieve with filter (specific source)
print("\n=== Test 2: With Filter (source='sample.pdf') ===")
try:
    docs_filtered = retrieve_documents(test_question, k=3, source="sample.pdf")
    print(f"✓ Retrieved {len(docs_filtered)} documents")
    for i, doc in enumerate(docs_filtered, 1):
        print(f"\n  Document {i}:")
        print(f"    Source: {doc.metadata.get('source', 'N/A')}")
        print(f"    Page: {doc.metadata.get('page', 'N/A')}")
        print(f"    Content preview: {doc.page_content[:100]}...")
        
    # Verify all documents are from the correct source
    all_from_sample = all(doc.metadata.get('source') == 'sample.pdf' for doc in docs_filtered)
    if all_from_sample:
        print("\n  ✓ All documents are from 'sample.pdf' - Filter working correctly!")
    else:
        print("\n  ✗ WARNING: Some documents are not from 'sample.pdf'")
except Exception as ex:
    print(f"✗ Error: {ex}")

# Test 3: Test with non-existent source
print("\n=== Test 3: Non-Existent Source (source='nonexistent.pdf') ===")
try:
    docs_none = retrieve_documents(test_question, k=3, source="nonexistent.pdf")
    print(f"✓ Retrieved {len(docs_none)} documents")
    if len(docs_none) == 0:
        print("  ✓ Correctly returned 0 documents - Filter working!")
    else:
        print(f"  ✗ WARNING: Retrieved {len(docs_none)} documents (expected 0)")
except Exception as ex:
    print(f"✗ Error: {ex}")

print("\n" + "=" * 70)
print("Metadata Filtering Test Complete")
print("=" * 70)
