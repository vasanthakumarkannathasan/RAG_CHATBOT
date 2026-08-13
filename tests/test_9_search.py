"""
Test 9: Search Operation
-------------------------
Tests search: type, timing, top-k retrieval.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.database import get_vector_db
from src.services.retrieval import retrieve_documents
from src.services.embedding import get_embedding_model
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import time

def test_search_operation():
    """Test search operation with detailed analysis"""
    print("\n" + "="*80)
    print("TEST 9: SEARCH OPERATION")
    print("="*80)
    
    # Test queries
    test_queries = [
        {
            "query": "What is Docker?",
            "k": 3,
            "description": "Simple factual question"
        },
        {
            "query": "Explain microservices architecture",
            "k": 5,
            "description": "Detailed explanation request"
        }
    ]
    
    # Get embedding model
    print(f"\n{'─'*80}")
    print("Initializing Search Components...")
    print(f"{'─'*80}")
    
    try:
        vector_db = get_vector_db()
        embedding_model = get_embedding_model()
        print(f"   ✅ Vector database ready")
        print(f"   ✅ Embedding model ready")
    except Exception as e:
        print(f"   ❌ Initialization failed: {str(e)}")
        return
    
    # Process each query
    for query_idx, test_case in enumerate(test_queries, 1):
        query = test_case["query"]
        k = test_case["k"]
        description = test_case["description"]
        
        print(f"\n{'='*80}")
        print(f"SEARCH TEST #{query_idx}")
        print(f"{'='*80}")
        
        print(f"\n📝 Query Information:")
        print(f"   Query: \"{query}\"")
        print(f"   Type: {description}")
        print(f"   Top-k: {k} results")
        
        # Step 1: Convert query to embedding
        print(f"\n{'─'*80}")
        print("STEP 1: Query Embedding")
        print(f"{'─'*80}")
        
        start_embed = time.time()
        query_embedding = embedding_model.embed_query(query)
        embed_time = time.time() - start_embed
        
        print(f"   ⏱️  Embedding time: {embed_time*1000:.3f} ms")
        print(f"   🔢 Query vector dimensions: {len(query_embedding)}")
        
        # Step 2: Perform similarity search
        print(f"\n{'─'*80}")
        print("STEP 2: Similarity Search")
        print(f"{'─'*80}")
        
        print(f"\n🔍 Search Configuration:")
        print(f"   • Search type: Cosine Similarity")
        print(f"   • Algorithm: Approximate Nearest Neighbors (ANN)")
        print(f"   • Top-k: {k} results")
        print(f"   • Distance metric: Cosine distance")
        
        start_search = time.time()
        try:
            results = retrieve_documents(query, k=k, source=None)
            search_time = time.time() - start_search
            
            print(f"\n✅ Search completed successfully")
            print(f"   ⏱️  Search time: {search_time*1000:.3f} ms")
            print(f"   📊 Results found: {len(results)}")
            
        except Exception as e:
            print(f"\n❌ Search failed: {str(e)}")
            continue
        
        # Step 3: Analyze results
        print(f"\n{'─'*80}")
        print("STEP 3: Search Results Analysis")
        print(f"{'─'*80}")
        
        # Calculate similarities manually for analysis
        result_embeddings = []
        for doc in results:
            doc_embedding = embedding_model.embed_query(doc.page_content)
            result_embeddings.append(doc_embedding)
        
        query_array = np.array(query_embedding).reshape(1, -1)
        
        print(f"\n📊 Retrieved Documents:")
        for idx, doc in enumerate(results, 1):
            print(f"\n   ┌{'─'*74}┐")
            print(f"   │ RESULT #{idx}" + " "*63 + "│")
            print(f"   └{'─'*74}┘")
            
            # Calculate similarity
            doc_array = np.array(result_embeddings[idx-1]).reshape(1, -1)
            similarity = cosine_similarity(query_array, doc_array)[0][0]
            
            # Document info
            source = doc.metadata.get('source', 'unknown')
            page = doc.metadata.get('page', 'N/A')
            
            print(f"\n   📄 Document: {source}")
            print(f"   📖 Page: {page}")
            print(f"   🎯 Similarity Score: {similarity:.6f} ({similarity*100:.2f}%)")
            
            # Similarity interpretation
            if similarity > 0.80:
                relevance = "🟢 Highly Relevant"
            elif similarity > 0.60:
                relevance = "🟡 Moderately Relevant"
            else:
                relevance = "🔴 Low Relevance"
            print(f"   📊 Relevance: {relevance}")
            
            # Content preview
            content_preview = doc.page_content[:200].replace('\n', ' ')
            print(f"\n   📝 Content Preview:")
            print(f"      {content_preview}...")
            print(f"      (Total length: {len(doc.page_content)} characters)")
            
            # Metadata
            print(f"\n   🏷️  Metadata:")
            for key, value in doc.metadata.items():
                if key == 'chunk_hash':
                    print(f"      • {key}: {str(value)[:32]}...")
                else:
                    print(f"      • {key}: {value}")
        
        # Performance metrics
        print(f"\n{'─'*80}")
        print("STEP 4: Performance Metrics")
        print(f"{'─'*80}")
        
        total_time = embed_time + search_time
        
        print(f"\n⏱️  Timing Breakdown:")
        print(f"   • Query Embedding  : {embed_time*1000:7.3f} ms ({embed_time/total_time*100:5.1f}%)")
        print(f"   • Similarity Search: {search_time*1000:7.3f} ms ({search_time/total_time*100:5.1f}%)")
        print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"   • Total Time       : {total_time*1000:7.3f} ms")
        
        print(f"\n📊 Search Statistics:")
        print(f"   • Query length: {len(query)} characters")
        print(f"   • Results requested (k): {k}")
        print(f"   • Results retrieved: {len(results)}")
        print(f"   • Search efficiency: {len(results)/search_time:.0f} docs/second")
        
        if result_embeddings:
            similarities = [cosine_similarity(query_array, np.array(emb).reshape(1, -1))[0][0] 
                          for emb in result_embeddings]
            print(f"\n📈 Similarity Distribution:")
            print(f"   • Highest: {max(similarities):.6f}")
            print(f"   • Lowest: {min(similarities):.6f}")
            print(f"   • Average: {np.mean(similarities):.6f}")
            print(f"   • Range: {max(similarities) - min(similarities):.6f}")
    
    # Search type explanation
    print(f"\n{'='*80}")
    print("SEARCH TYPE: COSINE SIMILARITY")
    print(f"{'='*80}")
    
    print(f"\n🔍 How It Works:")
    print(f"   1. Convert query to embedding vector")
    print(f"   2. Calculate cosine similarity with all document vectors")
    print(f"   3. Rank documents by similarity score")
    print(f"   4. Return top-k most similar documents")
    
    print(f"\n📐 Cosine Similarity Formula:")
    print(f"   similarity = (A · B) / (||A|| × ||B||)")
    print(f"   where A = query vector, B = document vector")
    
    print(f"\n📊 Similarity Scores:")
    print(f"   • 1.0  : Identical vectors (same direction)")
    print(f"   • >0.8 : Very similar (highly relevant)")
    print(f"   • 0.6-0.8 : Moderately similar")
    print(f"   • <0.6 : Low similarity")
    print(f"   • 0.0  : Orthogonal (no similarity)")
    
    print(f"\n⚡ Advantages:")
    print(f"   • Fast: O(n) with optimizations")
    print(f"   • Scale invariant: Focuses on direction, not magnitude")
    print(f"   • Intuitive: Higher score = more similar")
    print(f"   • Proven: Industry standard for semantic search")
    
    # Summary
    print(f"\n{'='*80}")
    print("SEARCH OPERATION SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n🔍 Search Method: Cosine Similarity (Semantic Search)")
    print(f"📊 Queries Tested: {len(test_queries)}")
    print(f"🎯 Search Purpose: Find semantically similar chunks")
    print(f"⚡ Performance: Sub-second retrieval for typical queries")
    print(f"🔧 Implementation: ChromaDB with HNSW indexing")
    print(f"📏 Distance Metric: Cosine distance (1 - cosine similarity)")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_search_operation()
