"""
Test 7: User Query to Embedding
--------------------------------
Tests query conversion: tokenization, embedding transformation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import EMBEDDING_MODEL
from src.services.embedding import get_embedding_model
from transformers import AutoTokenizer
import numpy as np
import time

def test_query_to_embedding():
    """Test user query conversion to embedding"""
    print("\n" + "="*80)
    print("TEST 7: USER QUERY TO EMBEDDING (RETRIEVAL)")
    print("="*80)
    
    # Sample user queries
    user_queries = [
        "What is Docker?",
        "How does microservices architecture work?",
        "Explain containerization and its benefits"
    ]
    
    print(f"\n🤖 Embedding Model: {EMBEDDING_MODEL}")
    
    # Load embedding model and tokenizer
    print(f"\n{'─'*80}")
    print("Loading Model and Tokenizer...")
    print(f"{'─'*80}")
    
    try:
        start_time = time.time()
        embedding_model = get_embedding_model()
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        load_time = time.time() - start_time
        
        print(f"   ✅ Loaded successfully")
        print(f"   ⏱️  Load time: {load_time:.3f} seconds")
    except Exception as e:
        print(f"   ❌ Failed to load: {str(e)}")
        return
    
    # Process each query
    for query_idx, user_query in enumerate(user_queries, 1):
        print(f"\n{'='*80}")
        print(f"QUERY #{query_idx}")
        print(f"{'='*80}")
        
        print(f"\n📝 User Query:")
        print(f"   \"{user_query}\"")
        print(f"   Length: {len(user_query)} characters")
        print(f"   Word count: {len(user_query.split())} words")
        
        # Step 1: Tokenization
        print(f"\n{'─'*80}")
        print("STEP 1: TOKENIZATION")
        print(f"{'─'*80}")
        
        start_time = time.time()
        tokens = tokenizer.tokenize(user_query)
        token_ids = tokenizer.encode(user_query, add_special_tokens=True)
        tokenize_time = time.time() - start_time
        
        print(f"\n⏱️  Tokenization time: {tokenize_time*1000:.3f} milliseconds")
        print(f"🔤 Tokenizer method: {type(tokenizer).__name__}")
        print(f"📊 Token count: {len(tokens)} tokens")
        print(f"🆔 Token IDs count: {len(token_ids)} (with special tokens)")
        
        print(f"\n🔤 Tokens:")
        print(f"   {tokens}")
        
        print(f"\n🆔 Token IDs:")
        print(f"   {token_ids}")
        
        # Token to ID mapping
        print(f"\n🔗 Token → ID Mapping:")
        for i, (token, tid) in enumerate(zip(tokens, token_ids[1:-1])):  # Skip CLS and SEP
            print(f"   {i+1}. '{token}' → ID: {tid}")
        
        # Step 2: Embedding conversion
        print(f"\n{'─'*80}")
        print("STEP 2: EMBEDDING CONVERSION")
        print(f"{'─'*80}")
        
        print(f"\n🔄 Conversion Process:")
        print(f"   1️⃣  Tokenization     : Text → Tokens → Token IDs")
        print(f"   2️⃣  Model Forward    : Token IDs → Hidden States")
        print(f"   3️⃣  Pooling          : Hidden States → Single Vector")
        print(f"   4️⃣  Normalization    : Scale vector (optional)")
        
        start_time = time.time()
        query_embedding = embedding_model.embed_query(user_query)
        embed_time = time.time() - start_time
        
        print(f"\n⏱️  Embedding time: {embed_time*1000:.3f} milliseconds")
        print(f"✅ Query successfully converted to embedding")
        
        # Embedding details
        print(f"\n{'─'*80}")
        print("STEP 3: QUERY EMBEDDING DETAILS")
        print(f"{'─'*80}")
        
        query_embedding_array = np.array(query_embedding)
        
        print(f"\n📊 Embedding Properties:")
        print(f"   🔢 Dimensions        : {len(query_embedding)}")
        print(f"   📏 Vector shape      : {query_embedding_array.shape}")
        print(f"   📈 Data type         : {query_embedding_array.dtype}")
        print(f"   📉 Min value         : {query_embedding_array.min():.6f}")
        print(f"   📊 Max value         : {query_embedding_array.max():.6f}")
        print(f"   🎯 Mean value        : {query_embedding_array.mean():.6f}")
        print(f"   📐 Std deviation     : {query_embedding_array.std():.6f}")
        print(f"   🔗 L2 Norm           : {np.linalg.norm(query_embedding_array):.6f}")
        
        print(f"\n🔢 Embedding Values (first 15):")
        first_15 = ', '.join(f"{val:.4f}" for val in query_embedding[:15])
        print(f"   [{first_15}, ...]")
        
        print(f"\n🔢 Embedding Values (last 15):")
        last_15 = ', '.join(f"{val:.4f}" for val in query_embedding[-15:])
        print(f"   [..., {last_15}]")
        
        # Total time
        total_time = tokenize_time + embed_time
        print(f"\n⏱️  Total Conversion Time:")
        print(f"   • Tokenization : {tokenize_time*1000:.3f} ms ({tokenize_time/total_time*100:.1f}%)")
        print(f"   • Embedding    : {embed_time*1000:.3f} ms ({embed_time/total_time*100:.1f}%)")
        print(f"   ━━━━━━━━━━━━━━━━━━")
        print(f"   • Total        : {total_time*1000:.3f} ms")
    
    # Compare query embeddings
    print(f"\n{'='*80}")
    print("QUERY SIMILARITY COMPARISON")
    print(f"{'='*80}")
    
    # Get all embeddings
    all_embeddings = [embedding_model.embed_query(q) for q in user_queries]
    
    from sklearn.metrics.pairwise import cosine_similarity
    embeddings_matrix = np.array(all_embeddings)
    similarity_matrix = cosine_similarity(embeddings_matrix)
    
    print(f"\n🔗 Cosine Similarity Between Queries:")
    print(f"\n   {'Query':8s} | ", end='')
    for i in range(len(user_queries)):
        print(f"Query {i+1:2d} |", end='')
    print()
    print(f"   {'-'*8} | {'-'*10}|{'-'*10}|{'-'*10}|")
    
    for i in range(len(user_queries)):
        print(f"   Query {i+1:2d} | ", end='')
        for j in range(len(user_queries)):
            sim = similarity_matrix[i][j]
            print(f" {sim:7.4f} |", end='')
        print()
    
    print(f"\n📊 Interpretation:")
    print(f"   • 1.0000 = Identical queries")
    print(f"   • >0.80  = Very similar queries")
    print(f"   • 0.50-0.80 = Moderately similar")
    print(f"   • <0.50  = Different queries")
    
    # Summary
    print(f"\n{'='*80}")
    print("QUERY TO EMBEDDING SUMMARY")
    print(f"{'='*80}")
    
    avg_tokens = sum(len(tokenizer.tokenize(q)) for q in user_queries) / len(user_queries)
    avg_embed_time = sum(embed_time for q in user_queries) / len(user_queries)
    
    print(f"🤖 Embedding Model           : {EMBEDDING_MODEL}")
    print(f"📊 Queries Processed         : {len(user_queries)}")
    print(f"🔤 Average Tokens per Query  : {avg_tokens:.1f}")
    print(f"🔢 Embedding Dimensions      : {len(all_embeddings[0])}")
    print(f"⏱️  Average Embedding Time   : {avg_embed_time*1000:.3f} ms")
    print(f"🎯 Purpose                   : Convert user query to vector for similarity search")
    print(f"🔍 Next Step                 : Search vector database for similar embeddings")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_query_to_embedding()
