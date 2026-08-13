"""
Test 5: Embedding Model - Pooling
----------------------------------
Tests pooling: before/after comparison, single vector creation.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import EMBEDDING_MODEL
from src.services.embedding import get_embedding_model
from transformers import AutoModel, AutoTokenizer
import torch
import numpy as np
import time

def test_embedding_pooling():
    """Test embedding pooling process with before/after comparison"""
    print("\n" + "="*80)
    print("TEST 5: EMBEDDING MODEL - POOLING")
    print("="*80)
    
    print(f"\n🤖 Model: {EMBEDDING_MODEL}")
    
    # Load model and tokenizer
    print(f"\n{'─'*80}")
    print("Loading Model and Tokenizer...")
    print(f"{'─'*80}")
    
    try:
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        model = AutoModel.from_pretrained(EMBEDDING_MODEL)
        print(f"   ✅ Model and tokenizer loaded successfully")
    except Exception as e:
        print(f"   ❌ Failed to load: {str(e)}")
        return
    
    # Test text
    test_text = "Machine learning models process data to make predictions and decisions."
    
    print(f"\n📝 Test Text:")
    print(f"   \"{test_text}\"")
    print(f"   Length: {len(test_text)} characters")
    
    # Tokenize
    print(f"\n{'='*80}")
    print("STEP 1: TOKENIZATION")
    print(f"{'='*80}")
    
    inputs = tokenizer(test_text, return_tensors="pt", padding=True, truncation=True)
    token_ids = inputs['input_ids'][0].tolist()
    tokens = tokenizer.convert_ids_to_tokens(token_ids)
    
    print(f"\n📊 Tokenization Results:")
    print(f"   🔢 Token count: {len(tokens)}")
    print(f"   🔤 Tokens: {tokens}")
    print(f"   🆔 Token IDs: {token_ids}")
    
    # Model forward pass (before pooling)
    print(f"\n{'='*80}")
    print("STEP 2: MODEL FORWARD PASS (Before Pooling)")
    print(f"{'='*80}")
    
    with torch.no_grad():
        start_time = time.time()
        outputs = model(**inputs)
        forward_time = time.time() - start_time
    
    # Get hidden states (before pooling)
    hidden_states = outputs.last_hidden_state
    
    print(f"\n⏱️  Forward pass time: {forward_time*1000:.3f} milliseconds")
    print(f"\n📊 Hidden States (Before Pooling):")
    print(f"   🔢 Shape: {hidden_states.shape}")
    print(f"   📝 Interpretation: (batch_size, sequence_length, hidden_size)")
    print(f"   📦 Batch size: {hidden_states.shape[0]}")
    print(f"   📏 Sequence length: {hidden_states.shape[1]} tokens")
    print(f"   🔢 Hidden size: {hidden_states.shape[2]} dimensions")
    print(f"   📈 Total values: {hidden_states.numel():,}")
    
    # Show embeddings for each token (before pooling)
    print(f"\n📋 Token-wise Embeddings (Before Pooling):")
    print(f"   Each token has its own {hidden_states.shape[2]}-dimensional embedding")
    
    for i, token in enumerate(tokens[:5]):
        token_embedding = hidden_states[0][i].numpy()
        print(f"\n   Token {i+1}: '{token}'")
        print(f"      Vector shape: {token_embedding.shape}")
        print(f"      First 5 values: {token_embedding[:5]}")
        print(f"      Mean: {token_embedding.mean():.6f}, Std: {token_embedding.std():.6f}")
    
    if len(tokens) > 5:
        print(f"\n   ... and {len(tokens)-5} more tokens")
    
    # Pooling operation
    print(f"\n{'='*80}")
    print("STEP 3: POOLING OPERATION")
    print(f"{'='*80}")
    
    print(f"\n🎯 Pooling Strategy: Mean Pooling")
    print(f"   Description: Average all token embeddings into single vector")
    print(f"   Formula: pooled_vector = mean(token_embeddings, axis=sequence_length)")
    
    start_time = time.time()
    
    # Mean pooling
    attention_mask = inputs['attention_mask']
    input_mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
    sum_embeddings = torch.sum(hidden_states * input_mask_expanded, dim=1)
    sum_mask = torch.clamp(input_mask_expanded.sum(dim=1), min=1e-9)
    pooled_embedding = (sum_embeddings / sum_mask)[0].numpy()
    
    pooling_time = time.time() - start_time
    
    print(f"\n⏱️  Pooling time: {pooling_time*1000:.3f} milliseconds")
    
    # After pooling
    print(f"\n{'='*80}")
    print("STEP 4: POOLED EMBEDDING (After Pooling)")
    print(f"{'='*80}")
    
    print(f"\n📊 Pooled Embedding Details:")
    print(f"   🔢 Shape: {pooled_embedding.shape}")
    print(f"   📏 Dimensions: {len(pooled_embedding)}")
    print(f"   📉 Min value: {pooled_embedding.min():.6f}")
    print(f"   📈 Max value: {pooled_embedding.max():.6f}")
    print(f"   🎯 Mean value: {pooled_embedding.mean():.6f}")
    print(f"   📐 Standard deviation: {pooled_embedding.std():.6f}")
    print(f"   🔗 L2 Norm: {np.linalg.norm(pooled_embedding):.6f}")
    
    print(f"\n🔢 Pooled Vector (first 10 values):")
    print(f"   {pooled_embedding[:10]}")
    
    print(f"\n🔢 Pooled Vector (last 10 values):")
    print(f"   {pooled_embedding[-10:]}")
    
    # Before vs After comparison
    print(f"\n{'='*80}")
    print("BEFORE vs AFTER POOLING COMPARISON")
    print(f"{'='*80}")
    
    print(f"\n📊 BEFORE Pooling:")
    print(f"   • Multiple vectors: {hidden_states.shape[1]} vectors (one per token)")
    print(f"   • Each vector: {hidden_states.shape[2]} dimensions")
    print(f"   • Total size: {hidden_states.numel():,} values")
    print(f"   • Memory: ~{hidden_states.numel() * 4 / 1024:.2f} KB (float32)")
    print(f"   • Representation: Token-level embeddings")
    
    print(f"\n📊 AFTER Pooling:")
    print(f"   • Single vector: 1 vector (represents entire text)")
    print(f"   • Vector dimensions: {len(pooled_embedding)} dimensions")
    print(f"   • Total size: {len(pooled_embedding):,} values")
    print(f"   • Memory: ~{len(pooled_embedding) * 4 / 1024:.2f} KB (float32)")
    print(f"   • Representation: Sentence-level embedding")
    
    compression_ratio = hidden_states.numel() / len(pooled_embedding)
    print(f"\n🎯 Compression Ratio: {compression_ratio:.1f}x")
    print(f"   Original text had {len(tokens)} token embeddings")
    print(f"   After pooling: 1 single embedding representing entire text")
    
    # Demonstrate with HuggingFaceEmbeddings
    print(f"\n{'='*80}")
    print("VALIDATION: Using HuggingFaceEmbeddings")
    print(f"{'='*80}")
    
    embedding_model = get_embedding_model()
    final_embedding = embedding_model.embed_query(test_text)
    
    print(f"\n✅ Final embedding dimensions: {len(final_embedding)}")
    print(f"✅ This is the single pooled vector used for:")
    print(f"   • Vector database storage")
    print(f"   • Similarity search")
    print(f"   • Semantic retrieval")
    
    # Summary
    print(f"\n{'='*80}")
    print("POOLING SUMMARY")
    print(f"{'='*80}")
    
    print(f"🤖 Model                     : {EMBEDDING_MODEL}")
    print(f"📝 Input Text                : \"{test_text[:50]}...\"")
    print(f"🔢 Tokens (before pooling)   : {len(tokens)} tokens")
    print(f"📊 Each token embedding      : {hidden_states.shape[2]} dimensions")
    print(f"📦 Total embeddings (before) : {hidden_states.shape[1] * hidden_states.shape[2]:,} values")
    print(f"⬇️  Pooling method            : Mean Pooling")
    print(f"📊 Pooled embedding          : {len(pooled_embedding)} dimensions")
    print(f"🎯 Result                    : Single vector representing entire text")
    print(f"⚡ Purpose                   : Reduce multiple token vectors to single semantic vector")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_embedding_pooling()
