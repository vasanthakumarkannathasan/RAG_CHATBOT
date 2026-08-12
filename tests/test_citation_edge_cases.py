"""Comprehensive test for source citation edge cases"""

from src.services.chat_service import build_sources
from langchain_core.documents import Document

print("=" * 70)
print("Source Citation Edge Cases Test")
print("=" * 70)

# Test Case 1: Multiple documents from same source and page
print("\n=== Test 1: Duplicate Source/Page (Should Deduplicate) ===")
docs1 = [
    Document(page_content="Content 1", metadata={"source": "doc1.pdf", "page": 0}),
    Document(page_content="Content 2", metadata={"source": "doc1.pdf", "page": 0}),
    Document(page_content="Content 3", metadata={"source": "doc1.pdf", "page": 0}),
]
citations1 = build_sources(docs1)
print(citations1)
if citations1.count("doc1.pdf") == 1:
    print("✓ Correctly deduplicated - shows doc1.pdf only once")
else:
    print("✗ WARNING: Not deduplicating properly")

# Test Case 2: Multiple sources and pages
print("\n=== Test 2: Multiple Sources and Pages ===")
docs2 = [
    Document(page_content="Content 1", metadata={"source": "doc1.pdf", "page": 0}),
    Document(page_content="Content 2", metadata={"source": "doc1.pdf", "page": 2}),
    Document(page_content="Content 3", metadata={"source": "doc2.pdf", "page": 1}),
    Document(page_content="Content 4", metadata={"source": "doc3.pdf", "page": 0}),
]
citations2 = build_sources(docs2)
print(citations2)
if "doc1.pdf (Page 1)" in citations2 and "doc1.pdf (Page 3)" in citations2:
    print("✓ Shows multiple pages from same document correctly")
else:
    print("✗ WARNING: Multiple pages not showing correctly")

if citations2.count("📄") == 4:
    print("✓ Shows all 4 unique source/page combinations")
else:
    print("✗ WARNING: Not showing all sources")

# Test Case 3: Missing metadata
print("\n=== Test 3: Missing Metadata (Should Handle Gracefully) ===")
docs3 = [
    Document(page_content="Content 1", metadata={}),  # No metadata
    Document(page_content="Content 2", metadata={"source": "doc1.pdf"}),  # No page
]
citations3 = build_sources(docs3)
print(citations3)
if "Unknown" in citations3:
    print("✓ Handles missing source gracefully with 'Unknown'")
else:
    print("✗ WARNING: Not handling missing source")

# Test Case 4: Sorting
print("\n=== Test 4: Alphabetical Sorting ===")
docs4 = [
    Document(page_content="Content 1", metadata={"source": "zebra.pdf", "page": 0}),
    Document(page_content="Content 2", metadata={"source": "apple.pdf", "page": 0}),
    Document(page_content="Content 3", metadata={"source": "banana.pdf", "page": 0}),
]
citations4 = build_sources(docs4)
print(citations4)
lines = [line for line in citations4.split("\n") if "📄" in line]
if lines == sorted(lines):
    print("✓ Citations are sorted alphabetically")
else:
    print("✗ WARNING: Citations are not sorted")

# Test Case 5: Page number conversion (0-indexed to 1-indexed)
print("\n=== Test 5: Page Number Indexing ===")
docs5 = [
    Document(page_content="Content", metadata={"source": "test.pdf", "page": 0}),
]
citations5 = build_sources(docs5)
print(citations5)
if "Page 1" in citations5:
    print("✓ Correctly converts page 0 to Page 1 (user-friendly)")
else:
    print("✗ WARNING: Page indexing might be incorrect")

print("\n" + "=" * 70)
print("All Edge Case Tests Complete")
print("=" * 70)
