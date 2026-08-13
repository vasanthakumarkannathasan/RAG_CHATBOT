"""
Test 3: Embedding Model - Tokenization
---------------------------------------
Tests tokenization: model used, token count, and token IDs.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import EMBEDDING_MODEL
from src.services.embedding import get_embedding_model
from transformers import AutoTokenizer
import time

def test_tokenization():
    """Test tokenization process with detailed information"""
    print("\n" + "="*80)
    print("TEST 3: EMBEDDING MODEL - TOKENIZATION")
    print("="*80)
    
    # Sample texts for testing
    test_texts = [
        "What is machine learning?",
        "Docker is a platform for developing, shipping, and running applications in containers.",
        "Microservices architecture enables independent deployment of services."
    ]
    
    print(f"\n🤖 Embedding Model: {EMBEDDING_MODEL}")
    
    # Load tokenizer
    print(f"\n{'─'*80}")
    print("Loading Tokenizer...")
    print(f"{'─'*80}")
    
    try:
        start_time = time.time()
        tokenizer = AutoTokenizer.from_pretrained(EMBEDDING_MODEL)
        load_time = time.time() - start_time
        
        print(f"   ✅ Tokenizer loaded successfully")
        print(f"   ⏱️  Load time: {load_time:.3f} seconds")
        print(f"   🔤 Vocabulary size: {tokenizer.vocab_size:,} tokens")
        print(f"   📏 Max length: {tokenizer.model_max_length} tokens")
        
        # Tokenizer properties
        print(f"\n   🔧 Tokenizer Properties:")
        print(f"      - Model: {EMBEDDING_MODEL}")
        print(f"      - Type: {type(tokenizer).__name__}")
        print(f"      - Special tokens: {len(tokenizer.all_special_tokens)}")
        
        # Show special tokens
        print(f"\n   🏷️  Special Tokens:")
        for token in tokenizer.all_special_tokens[:10]:
            token_id = tokenizer.convert_tokens_to_ids(token)
            print(f"      - '{token}' → ID: {token_id}")
        
    except Exception as e:
        print(f"   ❌ Failed to load tokenizer: {str(e)}")
        return
    
    # Tokenize sample texts
    print(f"\n{'='*80}")
    print("TOKENIZATION ANALYSIS")
    print(f"{'='*80}")
    
    for idx, text in enumerate(test_texts, 1):
        print(f"\n┌{'─'*78}┐")
        print(f"│ SAMPLE TEXT #{idx}" + " "*64 + "│")
        print(f"└{'─'*78}┘")
        
        print(f"\n📝 Original Text:")
        print(f"   \"{text}\"")
        print(f"   Length: {len(text)} characters")
        
        # Tokenize
        start_time = time.time()
        tokens = tokenizer.tokenize(text)
        token_ids = tokenizer.encode(text, add_special_tokens=True)
        tokenize_time = time.time() - start_time
        
        print(f"\n⏱️  Tokenization Time: {tokenize_time*1000:.3f} milliseconds")
        print(f"📊 Token Count: {len(tokens)} tokens")
        print(f"🆔 Token IDs Count: {len(token_ids)} (including special tokens)")
        
        # Show tokens
        print(f"\n🔤 Tokens:")
        token_display = []
        for i, token in enumerate(tokens[:20]):
            token_display.append(f"'{token}'")
        print(f"   {', '.join(token_display)}")
        if len(tokens) > 20:
            print(f"   ... and {len(tokens) - 20} more tokens")
        
        # Show token IDs
        print(f"\n🆔 Token IDs:")
        ids_display = ', '.join(str(tid) for tid in token_ids[:20])
        print(f"   [{ids_display}]")
        if len(token_ids) > 20:
            print(f"   ... and {len(token_ids) - 20} more IDs")
        
        # Token to ID mapping (first 5)
        print(f"\n🔗 Token → ID Mapping (first 5):")
        for i, (token, tid) in enumerate(zip(tokens[:5], token_ids[1:6])):  # Skip CLS token
            print(f"   {i+1}. '{token}' → {tid}")
        
        # Decode back
        decoded = tokenizer.decode(token_ids)
        print(f"\n🔄 Decoded Text:")
        print(f"   \"{decoded}\"")
        print(f"   Match: {'✅ Perfect match' if decoded.strip().lower() == text.strip().lower() else '⚠️ Minor differences'}")
    
    # Summary
    print(f"\n{'='*80}")
    print("TOKENIZATION SUMMARY")
    print(f"{'='*80}")
    
    total_tokens = sum(len(tokenizer.tokenize(text)) for text in test_texts)
    avg_tokens = total_tokens / len(test_texts)
    
    print(f"🤖 Tokenizer Model          : {EMBEDDING_MODEL}")
    print(f"📊 Total Texts Processed    : {len(test_texts)}")
    print(f"🔤 Total Tokens Generated   : {total_tokens}")
    print(f"📏 Average Tokens per Text  : {avg_tokens:.1f}")
    print(f"📖 Vocabulary Size          : {tokenizer.vocab_size:,}")
    print(f"⚡ Tokenization Method      : WordPiece/SentencePiece (model-dependent)")
    print(f"🎯 Purpose                  : Convert text to numerical tokens for embedding")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_tokenization()
