"""
Master Test Runner
------------------
Runs all comprehensive tests in sequence.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import time
from datetime import datetime

# Test modules
test_modules = [
    ("Test 1: Document Loading", "test_1_document_loading"),
    ("Test 2: Document Chunking", "test_2_chunking"),
    ("Test 3: Embedding Tokenization", "test_3_embedding_tokenization"),
    ("Test 4: Embedding Transformation", "test_4_embedding_transformation"),
    ("Test 5: Embedding Pooling", "test_5_embedding_pooling"),
    ("Test 6: Vector Storage", "test_6_vector_storage"),
    ("Test 7: Query Embedding", "test_7_query_embedding"),
    ("Test 8: Metadata Filtering", "test_8_metadata_filtering"),
    ("Test 9: Search Operation", "test_9_search"),
    ("Test 10: Prompt Builder", "test_10_prompt_builder"),
    ("Test 11: LLM Generation", "test_11_llm_generation"),
    ("Test 12: Duplicate Check", "test_12_duplicate_check"),
    ("Test 13: LLM Health", "test_13_llm_health"),
    ("Test 14: Indexing Flow", "test_14_indexing_flow"),
    ("Test 15: Retrieval Flow", "test_15_retrieval_flow"),
]

def run_all_tests():
    """Run all tests in sequence"""
    print("\n" + "="*80)
    print("ENTERPRISE RAG - COMPREHENSIVE TEST SUITE")
    print("="*80)
    print(f"\n📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"📊 Total Tests: {len(test_modules)}")
    
    print("\n" + "="*80)
    print("TEST CATEGORIES")
    print("="*80)
    print("\n📦 INDEXING TESTS (1-6):")
    print("   Tests document loading, chunking, embedding, and storage")
    print("\n🔍 RETRIEVAL TESTS (7-11):")
    print("   Tests query processing, search, and answer generation")
    print("\n🛠️  SYSTEM TESTS (12-15):")
    print("   Tests health, duplicates, and end-to-end flows")
    
    overall_start = time.time()
    results = []
    
    for test_name, module_name in test_modules:
        print("\n" + "="*80)
        print(f"Running: {test_name}")
        print("="*80)
        
        test_start = time.time()
        
        try:
            # Import and run test
            module = __import__(module_name)
            
            # Get the main test function
            if hasattr(module, 'test_document_loading'):
                module.test_document_loading()
            elif hasattr(module, 'test_chunking'):
                module.test_chunking()
            elif hasattr(module, 'test_tokenization'):
                module.test_tokenization()
            elif hasattr(module, 'test_embedding_transformation'):
                module.test_embedding_transformation()
            elif hasattr(module, 'test_embedding_pooling'):
                module.test_embedding_pooling()
            elif hasattr(module, 'test_vector_storage'):
                module.test_vector_storage()
            elif hasattr(module, 'test_query_to_embedding'):
                module.test_query_to_embedding()
            elif hasattr(module, 'test_metadata_filtering'):
                module.test_metadata_filtering()
            elif hasattr(module, 'test_search_operation'):
                module.test_search_operation()
            elif hasattr(module, 'test_prompt_builder'):
                module.test_prompt_builder()
            elif hasattr(module, 'test_llm_generation'):
                module.test_llm_generation()
            elif hasattr(module, 'test_duplicate_detection'):
                module.test_duplicate_detection()
            elif hasattr(module, 'test_llm_health'):
                module.test_llm_health()
            elif hasattr(module, 'test_indexing_flow'):
                module.test_indexing_flow()
            elif hasattr(module, 'test_retrieval_flow'):
                module.test_retrieval_flow()
            
            test_time = time.time() - test_start
            results.append({
                'name': test_name,
                'status': '✅ PASS',
                'time': test_time
            })
            
        except Exception as e:
            test_time = time.time() - test_start
            results.append({
                'name': test_name,
                'status': '❌ FAIL',
                'time': test_time,
                'error': str(e)
            })
            print(f"\n❌ Test failed: {str(e)}")
    
    # Summary
    overall_time = time.time() - overall_start
    
    print("\n" + "="*80)
    print("TEST SUITE SUMMARY")
    print("="*80)
    
    passed = sum(1 for r in results if 'PASS' in r['status'])
    failed = sum(1 for r in results if 'FAIL' in r['status'])
    
    print(f"\n📊 Results:")
    print(f"   • Total tests: {len(results)}")
    print(f"   • Passed: {passed} ✅")
    print(f"   • Failed: {failed} ❌")
    print(f"   • Success rate: {(passed/len(results)*100):.1f}%")
    
    print(f"\n⏱️  Timing:")
    print(f"   • Total time: {overall_time:.2f} seconds")
    print(f"   • Average per test: {overall_time/len(results):.2f} seconds")
    
    print(f"\n📋 Detailed Results:")
    print(f"   {'Test':<50} {'Status':<12} {'Time (s)':<10}")
    print(f"   {'-'*50} {'-'*12} {'-'*10}")
    
    for result in results:
        print(f"   {result['name']:<50} {result['status']:<12} {result['time']:>8.2f}")
    
    if failed > 0:
        print(f"\n⚠️  Failed Tests:")
        for result in results:
            if 'FAIL' in result['status']:
                print(f"\n   ❌ {result['name']}")
                if 'error' in result:
                    print(f"      Error: {result['error']}")
    
    print(f"\n{'='*80}")
    if failed == 0:
        print("✅ ALL TESTS PASSED! System is fully operational.")
    else:
        print(f"⚠️  {failed} TEST(S) FAILED. Please review errors above.")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    run_all_tests()
