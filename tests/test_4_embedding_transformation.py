"""
Test 4: Embedding Model - Transformation
-----------------------------------------
Tests transformation: model, dimensions, embeddings, chunk info.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import EMBEDDING_MODEL, PDF_DIRECTORY
from src.services.embedding import get_embedding_model
from src.services.loader import load_document
from src.services.chunking import split_documents
import numpy as np
import time

def test_embedding_transformation():
    """Test embedding transformation with detailed information"""
    print("\n" + "="*80)
    print("TEST 4: EMBEDDING MODEL - TRANSFORMATION")
    print("="*80)
    
    # Get embedding model
    print(f"\n🤖 Loading Embedding Model...")
    print(f"   Model: {EMBEDDING_MODEL}")
    
    try:
        start_time = time.time()
        embedding_model = get_embedding_model()
        load_time = time.time() - start_time
        
        print(f"   ✅ Model loaded successfully")
        print(f"   ⏱️  Load time: {load_time:.3f} seconds")
    except Exception as e:
        print(f"   ❌ Failed to load model: {str(e)}")
        return
    
    # Test samples
    test_chunks = [
        {
            "chunk_id": "CHUNK-001",
            "original_text": "Machine learning is a subset of artificial intelligence.",
            "metadata": {"source": "sample.pdf", "page": 1}
        },
        {
            "chunk_id": "CHUNK-002",
            "original_text": "Docker containers provide isolated environments for applications.",
            "metadata": {"source": "docker.pdf", "page": 3}
        },
        {
            "chunk_id": "CHUNK-003",
            "original_text": "Vector databases store and retrieve high-dimensional embeddings.",
            "metadata": {"source": "vectors.pdf", "page": 5}
        }
    ]
    
    print(f"\n{'='*80}")
    print("EMBEDDING TRANSFORMATION ANALYSIS")
    print(f"{'='*80}")
    
    all_embeddings = []
    transformation_times = []
    
    for idx, chunk_info in enumerate(test_chunks, 1):
        print(f"\n┌{'─'*78}┐")
        print(f"│ CHUNK #{idx}: {chunk_info['chunk_id']}" + " "*(65-len(chunk_info['chunk_id'])) + "│")
        print(f"└{'─'*78}┘")
        
        # Original text
        original_text = chunk_info['original_text']
        print(f"\n📝 Original Chunk Text:")
        print(f"   \"{original_text}\"")
        print(f"   Length: {len(original_text)} characters")
        
        # Metadata
        print(f"\n🏷️  Chunk Metadata:")
        for key, value in chunk_info['metadata'].items():
            print(f"   - {key}: {value}")
        
        # Transform to embedding
        print(f"\n🔄 Transformation Process:")
        print(f"   1️⃣  Input: Raw text string")
        print(f"   2️⃣  Tokenization: Text → Token IDs")
        print(f"   3️⃣  Model forward pass: Tokens → Hidden states")
        print(f"   4️⃣  Pooling: Hidden states → Single vector")
        
        start_time = time.time()
        embedding = embedding_model.embed_query(original_text)
        transform_time = time.time() - start_time
        transformation_times.append(transform_time)
        
        all_embeddings.append(embedding)
        
        print(f"\n✅ Transformation completed in {transform_time*1000:.3f} milliseconds")
        
        # Embedding details
        embedding_array = np.array(embedding)
        print(f"\n📊 Embedding Details:")
        print(f"   🔢 Dimension         : {len(embedding)} dimensions")
        print(f"   📏 Vector shape      : {embedding_array.shape}")
        print(f"   📈 Data type         : {embedding_array.dtype}")
        print(f"   📉 Min value         : {embedding_array.min():.6f}")
        print(f"   📊 Max value         : {embedding_array.max():.6f}")
        print(f"   🎯 Mean value        : {embedding_array.mean():.6f}")
        print(f"   📐 Standard dev      : {embedding_array.std():.6f}")
        print(f"   🔗 L2 Norm           : {np.linalg.norm(embedding_array):.6f}")
        
        # Show first 10 and last 10 values
        print(f"\n🔢 Embedding Values (first 10):")
        first_10 = ', '.join(f"{val:.4f}" for val in embedding[:10])
        print(f"   [{first_10}, ...]")
        
        print(f"\n🔢 Embedding Values (last 10):")
        last_10 = ', '.join(f"{val:.4f}" for val in embedding[-10:])
        print(f"   [..., {last_10}]")
        
        # Show embedding text representation
        print(f"\n📝 Embedding Text (truncated):")
        embedding_str = str(embedding[:5])[:-1] + ", ..., " + str(embedding[-5:])[1:]
        print(f"   {embedding_str}")
    
    # Similarity analysis between embeddings
    print(f"\n{'='*80}")
    print("EMBEDDING SIMILARITY ANALYSIS")
    print(f"{'='*80}")
    
    from sklearn.metrics.pairwise import cosine_similarity
    
    embeddings_matrix = np.array(all_embeddings)
    similarity_matrix = cosine_similarity(embeddings_matrix)
    
    print(f"\n🔗 Cosine Similarity Matrix:")
    print(f"   {' '*12}", end='')
    for i in range(len(test_chunks)):
        print(f"CHUNK-{i+1:03d}  ", end='')
    print()
    
    for i, chunk in enumerate(test_chunks):
        print(f"   {chunk['chunk_id']:12s}", end='')
        for j in range(len(test_chunks)):
            sim = similarity_matrix[i][j]
            color = '🟢' if sim > 0.8 else '🟡' if sim > 0.5 else '🔴'
            print(f"{sim:8.4f} {color} ", end='')
        print()
    
    # Summary
    print(f"\n{'='*80}")
    print("TRANSFORMATION SUMMARY")
    print(f"{'='*80}")
    
    avg_time = sum(transformation_times) / len(transformation_times)
    
    print(f"🤖 Embedding Model           : {EMBEDDING_MODEL}")
    print(f"🔢 Embedding Dimensions      : {len(all_embeddings[0])}")
    print(f"📊 Total Chunks Processed    : {len(test_chunks)}")
    print(f"⏱️  Average Transform Time   : {avg_time*1000:.3f} milliseconds")
    print(f"⚡ Fastest Transform         : {min(transformation_times)*1000:.3f} ms")
    print(f"🐌 Slowest Transform         : {max(transformation_times)*1000:.3f} ms")
    print(f"🎯 Transformation Method     : Neural Network (Transformer-based)")
    print(f"📐 Vector Space              : {len(all_embeddings[0])}-dimensional space")
    print(f"🔧 Purpose                   : Convert text to dense numerical vectors")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_embedding_transformation()
