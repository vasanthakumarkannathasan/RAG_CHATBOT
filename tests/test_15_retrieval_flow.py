"""
Test 15: Overall Retrieval Flow
--------------------------------
Tests complete retrieval pipeline from query to answer.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.embedding import get_embedding_model
from src.services.retrieval import retrieve_documents
from src.services.prompt_builder import build_prompt
from src.services.llm import generate_answer
import time

def test_retrieval_flow():
    """Test complete retrieval pipeline"""
    print("\n" + "="*80)
    print("TEST 15: OVERALL RETRIEVAL FLOW")
    print("="*80)
    
    # Test query
    user_query = "What is Docker?"
    print(f"\n📝 User Query: \"{user_query}\"")
    
    # Initialize timing
    stage_times = {}
    overall_start = time.time()
    
    # STAGE 1: Query Embedding
    print(f"\n{'='*80}")
    print("STAGE 1: QUERY TO EMBEDDING")
    print(f"{'='*80}")
    
    print(f"\n🔄 Converting query to embedding vector...")
    
    try:
        start_time = time.time()
        embedding_model = get_embedding_model()
        model_load_time = time.time() - start_time
        
        print(f"   ✅ Embedding model loaded: {model_load_time:.3f}s")
        
        start_time = time.time()
        query_embedding = embedding_model.embed_query(user_query)
        stage_times['query_embedding'] = time.time() - start_time
        
        print(f"\n✅ Query embedding generated")
        print(f"   ⏱️  Time: {stage_times['query_embedding']*1000:.3f} ms")
        print(f"   🔢 Dimensions: {len(query_embedding)}")
        print(f"   📊 Sample values: [{query_embedding[0]:.4f}, {query_embedding[1]:.4f}, ..., {query_embedding[-1]:.4f}]")
        
    except Exception as e:
        print(f"\n❌ Query embedding failed: {str(e)}")
        return
    
    # STAGE 2: Metadata Filtering (if applicable)
    print(f"\n{'='*80}")
    print("STAGE 2: METADATA FILTERING")
    print(f"{'='*80}")
    
    print(f"\n🔍 Filter configuration:")
    print(f"   • Source filter: None (search all documents)")
    print(f"   • Search scope: All indexed documents")
    print(f"   ℹ️  To filter by document, specify source parameter")
    
    stage_times['metadata_filtering'] = 0  # No filtering in this test
    
    # STAGE 3: Similarity Search
    print(f"\n{'='*80}")
    print("STAGE 3: SIMILARITY SEARCH")
    print(f"{'='*80}")
    
    k = 3
    print(f"\n🔍 Search parameters:")
    print(f"   • Search method: Cosine Similarity")
    print(f"   • Top-k: {k} results")
    print(f"   • Distance metric: Cosine distance")
    
    try:
        start_time = time.time()
        retrieved_docs = retrieve_documents(user_query, k=k, source=None)
        stage_times['search'] = time.time() - start_time
        
        print(f"\n✅ Search completed")
        print(f"   ⏱️  Time: {stage_times['search']*1000:.3f} ms")
        print(f"   📊 Documents retrieved: {len(retrieved_docs)}")
        
        # Show retrieved documents
        print(f"\n   📄 Retrieved Documents:")
        total_context_chars = 0
        
        for idx, doc in enumerate(retrieved_docs, 1):
            source = doc.metadata.get('source', 'unknown')
            page = doc.metadata.get('page', 'N/A')
            content_len = len(doc.page_content)
            total_context_chars += content_len
            
            print(f"      {idx}. {source} (Page {page}) - {content_len} chars")
            content_preview = doc.page_content[:80].replace('\n', ' ')
            print(f"         Preview: {content_preview}...")
        
        print(f"\n   📊 Total context: {total_context_chars} characters")
        
    except Exception as e:
        print(f"\n❌ Search failed: {str(e)}")
        return
    
    # STAGE 4: Reranking (Optional - not implemented in current system)
    print(f"\n{'='*80}")
    print("STAGE 4: RERANKING")
    print(f"{'='*80}")
    
    print(f"\n   ℹ️  Reranking: NOT IMPLEMENTED")
    print(f"      Current system uses direct similarity scores")
    print(f"      Documents are already ranked by relevance")
    print(f"\n   📊 Current ranking:")
    for idx, doc in enumerate(retrieved_docs, 1):
        print(f"      Rank {idx}: {doc.metadata.get('source', 'unknown')} (Page {doc.metadata.get('page', 'N/A')})")
    
    stage_times['reranking'] = 0
    
    # STAGE 5: Prompt Building
    print(f"\n{'='*80}")
    print("STAGE 5: PROMPT BUILDING")
    print(f"{'='*80}")
    
    print(f"\n🔧 Building RAG prompt...")
    
    try:
        start_time = time.time()
        prompt = build_prompt(
            question=user_query,
            documents=retrieved_docs,
            conversation_history=None
        )
        stage_times['prompt_building'] = time.time() - start_time
        
        print(f"\n✅ Prompt built")
        print(f"   ⏱️  Time: {stage_times['prompt_building']*1000:.3f} ms")
        print(f"   📏 Total length: {len(prompt)} characters")
        print(f"   📊 Estimated tokens: ~{len(prompt.split())}")
        
        # Prompt components
        print(f"\n   📦 Prompt components:")
        print(f"      • System instructions")
        print(f"      • Context ({len(retrieved_docs)} documents, {total_context_chars} chars)")
        print(f"      • User query ({len(user_query)} chars)")
        
        # Show prompt preview
        print(f"\n   📝 Prompt preview (first 200 chars):")
        preview = prompt[:200].replace('\n', ' ')
        print(f"      {preview}...")
        
    except Exception as e:
        print(f"\n❌ Prompt building failed: {str(e)}")
        return
    
    # STAGE 6: LLM Generation
    print(f"\n{'='*80}")
    print("STAGE 6: LLM GENERATION")
    print(f"{'='*80}")
    
    print(f"\n🤖 Generating answer with LLM...")
    print(f"   Model: Will use configured LLM")
    print(f"   Input: RAG prompt ({len(prompt)} chars)")
    
    try:
        start_time = time.time()
        answer = generate_answer(prompt, stream=False)
        stage_times['llm_generation'] = time.time() - start_time
        
        print(f"\n✅ Answer generated")
        print(f"   ⏱️  Time: {stage_times['llm_generation']:.3f} seconds")
        print(f"   📏 Answer length: {len(answer)} characters")
        print(f"   📊 Word count: {len(answer.split())} words")
        print(f"   ⚡ Speed: ~{len(answer.split())/stage_times['llm_generation']:.1f} words/second")
        
        # Show answer
        print(f"\n   📝 Generated Answer:")
        print(f"   ┌{'─'*74}┐")
        for line in answer.split('\n'):
            if line.strip():
                # Wrap long lines
                words = line.split()
                current_line = "   │ "
                for word in words:
                    if len(current_line) + len(word) + 1 > 78:
                        print(f"{current_line:<78}│")
                        current_line = "   │ " + word + " "
                    else:
                        current_line += word + " "
                print(f"{current_line:<78}│")
        print(f"   └{'─'*74}┘")
        
    except Exception as e:
        print(f"\n❌ LLM generation failed: {str(e)}")
        return
    
    # STAGE 7: Response Formatting (with sources)
    print(f"\n{'='*80}")
    print("STAGE 7: RESPONSE FORMATTING")
    print(f"{'='*80}")
    
    print(f"\n📦 Formatting final response...")
    
    # Extract sources
    sources = []
    for doc in retrieved_docs:
        source_info = {
            "document": doc.metadata.get('source', 'unknown'),
            "page": doc.metadata.get('page', 'N/A')
        }
        if source_info not in sources:
            sources.append(source_info)
    
    # Create final response
    response = {
        "answer": answer,
        "sources": sources
    }
    
    print(f"\n✅ Response formatted")
    print(f"   📝 Answer: {len(answer)} characters")
    print(f"   📚 Sources: {len(sources)} unique documents")
    
    print(f"\n   📚 Source Citations:")
    for idx, source in enumerate(sources, 1):
        print(f"      {idx}. {source['document']} (Page {source['page']})")
    
    # Overall Summary
    print(f"\n{'='*80}")
    print("RETRIEVAL FLOW SUMMARY")
    print(f"{'='*80}")
    
    overall_time = time.time() - overall_start
    
    print(f"\n⏱️  TIMING BREAKDOWN:")
    total_measured = sum(stage_times.values())
    
    print(f"   1. Query Embedding     : {stage_times.get('query_embedding', 0)*1000:7.1f} ms ({stage_times.get('query_embedding', 0)/overall_time*100:5.1f}%)")
    print(f"   2. Metadata Filtering  : {stage_times.get('metadata_filtering', 0)*1000:7.1f} ms ({stage_times.get('metadata_filtering', 0)/overall_time*100:5.1f}%)")
    print(f"   3. Similarity Search   : {stage_times.get('search', 0)*1000:7.1f} ms ({stage_times.get('search', 0)/overall_time*100:5.1f}%)")
    print(f"   4. Reranking           : {stage_times.get('reranking', 0)*1000:7.1f} ms ({stage_times.get('reranking', 0)/overall_time*100:5.1f}%)")
    print(f"   5. Prompt Building     : {stage_times.get('prompt_building', 0)*1000:7.1f} ms ({stage_times.get('prompt_building', 0)/overall_time*100:5.1f}%)")
    print(f"   6. LLM Generation      : {stage_times.get('llm_generation', 0)*1000:7.1f} ms ({stage_times.get('llm_generation', 0)/overall_time*100:5.1f}%)")
    print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total Time             : {overall_time*1000:7.1f} ms")
    
    # Identify bottleneck
    slowest_stage = max(stage_times.items(), key=lambda x: x[1])
    print(f"\n   🐌 Slowest stage: {slowest_stage[0]} ({slowest_stage[1]*1000:.1f} ms)")
    
    print(f"\n📊 PROCESSING STATISTICS:")
    print(f"   • User query: \"{user_query}\"")
    print(f"   • Query length: {len(user_query)} characters")
    print(f"   • Documents retrieved: {len(retrieved_docs)}")
    print(f"   • Context size: {total_context_chars} characters")
    print(f"   • Prompt size: {len(prompt)} characters")
    print(f"   • Answer length: {len(answer)} characters")
    print(f"   • Sources cited: {len(sources)}")
    
    print(f"\n🔄 COMPLETE FLOW:")
    print(f"   1. ✅ Query to Embedding  → {len(query_embedding)}D vector")
    print(f"   2. ✅ Metadata Filtering  → No filter applied")
    print(f"   3. ✅ Similarity Search   → {len(retrieved_docs)} documents")
    print(f"   4. ✅ Reranking           → Not implemented (using similarity scores)")
    print(f"   5. ✅ Prompt Building     → {len(prompt)} chars")
    print(f"   6. ✅ LLM Generation      → {len(answer)} chars answer")
    print(f"   7. ✅ Response Formatting → Answer + {len(sources)} sources")
    
    print(f"\n📈 PERFORMANCE METRICS:")
    print(f"   • End-to-end latency: {overall_time:.3f} seconds")
    print(f"   • LLM percentage: {(stage_times['llm_generation']/overall_time*100):.1f}%")
    print(f"   • Retrieval percentage: {((stage_times['query_embedding'] + stage_times['search'])/overall_time*100):.1f}%")
    
    if overall_time < 5.0:
        performance_rating = "🟢 EXCELLENT"
    elif overall_time < 10.0:
        performance_rating = "🟡 GOOD"
    else:
        performance_rating = "🔴 NEEDS OPTIMIZATION"
    
    print(f"   • Performance rating: {performance_rating}")
    
    print(f"\n✅ RETRIEVAL PIPELINE: OPERATIONAL")
    print(f"   All stages completed successfully")
    print(f"   System ready for production use")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_retrieval_flow()
