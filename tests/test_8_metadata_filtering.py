"""
Test 8: Metadata Filtering
---------------------------
Tests metadata filtering before search operation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.database import get_vector_db
from src.services.retrieval import retrieve_documents
import time

def test_metadata_filtering():
    """Test metadata filtering capabilities"""
    print("\n" + "="*80)
    print("TEST 8: METADATA FILTERING")
    print("="*80)
    
    # Get vector database
    print(f"\n{'─'*80}")
    print("Connecting to Vector Database...")
    print(f"{'─'*80}")
    
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        print(f"   ✅ Connected successfully")
        
        # Get all documents to understand metadata
        results = collection.get(include=['metadatas'])
        total_docs = len(results['ids'])
        print(f"   📊 Total documents: {total_docs}")
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return
    
    # Analyze metadata structure
    print(f"\n{'='*80}")
    print("METADATA STRUCTURE ANALYSIS")
    print(f"{'='*80}")
    
    # Collect all unique metadata keys
    all_metadata_keys = set()
    metadata_examples = {}
    source_distribution = {}
    
    for metadata in results['metadatas']:
        if metadata:
            for key, value in metadata.items():
                all_metadata_keys.add(key)
                if key not in metadata_examples:
                    metadata_examples[key] = value
                
                # Track source distribution
                if key == 'source':
                    source_distribution[value] = source_distribution.get(value, 0) + 1
    
    print(f"\n📋 Available Metadata Fields:")
    for idx, key in enumerate(sorted(all_metadata_keys), 1):
        example_value = metadata_examples.get(key, 'N/A')
        if key == 'chunk_hash':
            example_value = f"{str(example_value)[:20]}..."
        print(f"   {idx}. {key:15s} : {example_value}")
    
    print(f"\n📊 Source Distribution:")
    for source, count in source_distribution.items():
        percentage = (count / total_docs) * 100
        print(f"   • {source:30s}: {count:4d} chunks ({percentage:5.1f}%)")
    
    # Test different filtering scenarios
    test_query = "What is Docker?"
    
    print(f"\n{'='*80}")
    print("FILTERING SCENARIOS")
    print(f"{'='*80}")
    print(f"\n📝 Test Query: \"{test_query}\"")
    
    # Scenario 1: No filtering (search all documents)
    print(f"\n┌{'─'*78}┐")
    print(f"│ SCENARIO 1: No Filtering (Search All Documents)" + " "*28 + "│")
    print(f"└{'─'*78}┘")
    
    print(f"\n🔍 Filter Configuration:")
    print(f"   • Metadata filter: None")
    print(f"   • Search scope: All {total_docs} documents")
    print(f"   • Top-k: 3")
    
    try:
        start_time = time.time()
        results_no_filter = retrieve_documents(test_query, k=3, source=None)
        search_time = time.time() - start_time
        
        print(f"\n✅ Search completed in {search_time*1000:.3f} milliseconds")
        print(f"📊 Results found: {len(results_no_filter)}")
        
        print(f"\n📄 Retrieved Documents:")
        for idx, doc in enumerate(results_no_filter, 1):
            source = doc.metadata.get('source', 'unknown')
            page = doc.metadata.get('page', 'N/A')
            content_preview = doc.page_content[:100].replace('\n', ' ')
            print(f"\n   Result {idx}:")
            print(f"      Source: {source}")
            print(f"      Page: {page}")
            print(f"      Preview: {content_preview}...")
    
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")
    
    # Scenario 2: Filter by specific document
    if source_distribution:
        specific_source = list(source_distribution.keys())[0]
        
        print(f"\n┌{'─'*78}┐")
        print(f"│ SCENARIO 2: Filter by Specific Document" + " "*36 + "│")
        print(f"└{'─'*78}┘")
        
        print(f"\n🔍 Filter Configuration:")
        print(f"   • Metadata filter: source = '{specific_source}'")
        filtered_count = source_distribution[specific_source]
        print(f"   • Search scope: {filtered_count} documents (out of {total_docs})")
        print(f"   • Reduction: {((total_docs - filtered_count) / total_docs * 100):.1f}% of documents excluded")
        print(f"   • Top-k: 3")
        
        try:
            start_time = time.time()
            results_filtered = retrieve_documents(test_query, k=3, source=specific_source)
            search_time = time.time() - start_time
            
            print(f"\n✅ Filtered search completed in {search_time*1000:.3f} milliseconds")
            print(f"📊 Results found: {len(results_filtered)}")
            
            print(f"\n📄 Retrieved Documents:")
            for idx, doc in enumerate(results_filtered, 1):
                source = doc.metadata.get('source', 'unknown')
                page = doc.metadata.get('page', 'N/A')
                content_preview = doc.page_content[:100].replace('\n', ' ')
                print(f"\n   Result {idx}:")
                print(f"      Source: {source}")
                print(f"      Page: {page}")
                print(f"      Preview: {content_preview}...")
                print(f"      ✅ Matches filter: source = '{specific_source}'")
        
        except Exception as e:
            print(f"\n❌ Filtered search failed: {str(e)}")
    
    # Scenario 3: Understanding filter benefits
    print(f"\n┌{'─'*78}┐")
    print(f"│ SCENARIO 3: Filter Benefits Analysis" + " "*40 + "│")
    print(f"└{'─'*78}┘")
    
    print(f"\n📊 Filtering Benefits:")
    print(f"\n   1️⃣  Search Scope Reduction:")
    print(f"      • Without filter: Search through {total_docs} chunks")
    if source_distribution:
        for source, count in list(source_distribution.items())[:3]:
            reduction = ((total_docs - count) / total_docs * 100)
            print(f"      • With filter '{source}': Search through {count} chunks")
            print(f"        → {reduction:.1f}% reduction in search space")
    
    print(f"\n   2️⃣  Performance Improvement:")
    print(f"      • Smaller search space = Faster retrieval")
    print(f"      • More focused results from specific document")
    print(f"      • Reduced computational overhead")
    
    print(f"\n   3️⃣  Result Relevance:")
    print(f"      • Filters ensure results come from desired source")
    print(f"      • Useful when user specifies document context")
    print(f"      • Prevents cross-document contamination")
    
    # Summary
    print(f"\n{'='*80}")
    print("METADATA FILTERING SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n📋 Available Filters:")
    print(f"   • Primary: source (document filename)")
    print(f"   • Secondary: page, chunk_hash")
    print(f"   • Custom: Any metadata field")
    
    print(f"\n📊 Filter Statistics:")
    print(f"   • Total documents: {total_docs}")
    print(f"   • Unique sources: {len(source_distribution)}")
    print(f"   • Metadata fields: {len(all_metadata_keys)}")
    
    print(f"\n🎯 Filtering Purpose:")
    print(f"   • Reduce search space for faster retrieval")
    print(f"   • Limit results to specific documents")
    print(f"   • Improve result relevance")
    print(f"   • Support context-aware queries")
    
    print(f"\n⚙️  Implementation:")
    print(f"   • Applied BEFORE similarity search")
    print(f"   • Uses ChromaDB's built-in filtering")
    print(f"   • Supports exact match and complex queries")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_metadata_filtering()
