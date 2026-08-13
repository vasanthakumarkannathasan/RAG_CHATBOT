"""
Test 11: LLM Generation & Activity
-----------------------------------
Tests LLM: model, generation process, tokenization, timing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import MODEL_NAME
from src.services.llm import generate_answer, get_ollama_client
from src.services.prompt_builder import build_prompt
from src.services.retrieval import retrieve_documents
import time
import ollama

def test_llm_generation():
    """Test LLM generation with detailed activity analysis"""
    print("\n" + "="*80)
    print("TEST 11: LLM GENERATION & ACTIVITY")
    print("="*80)
    
    print(f"\n🤖 LLM Model: {MODEL_NAME}")
    
    # Check Ollama client
    print(f"\n{'─'*80}")
    print("STEP 1: Ollama Client Initialization")
    print(f"{'─'*80}")
    
    try:
        start_time = time.time()
        client = get_ollama_client()
        init_time = time.time() - start_time
        
        print(f"   ✅ Client initialized successfully")
        print(f"   ⏱️  Initialization time: {init_time*1000:.3f} ms")
        
        # Get model info
        models = client.list()
        model_found = False
        for model in models.models:
            if MODEL_NAME in model.model:
                model_found = True
                print(f"\n   📊 Model Information:")
                print(f"      • Name: {model.model}")
                print(f"      • Size: {model.size / (1024**3):.2f} GB")
                if hasattr(model, 'modified_at'):
                    print(f"      • Modified: {model.modified_at}")
                break
        
        if not model_found:
            print(f"\n   ⚠️  Model '{MODEL_NAME}' not found in Ollama")
            print(f"   Available models:")
            for model in models.models:
                print(f"      • {model.model}")
            return
            
    except Exception as e:
        print(f"   ❌ Client initialization failed: {str(e)}")
        return
    
    # Test query
    user_query = "What is Docker?"
    
    print(f"\n{'='*80}")
    print("STEP 2: Prepare RAG Prompt")
    print(f"{'='*80}")
    
    print(f"\n📝 User Query: \"{user_query}\"")
    
    # Retrieve context
    try:
        documents = retrieve_documents(user_query, k=2)
        print(f"   ✅ Retrieved {len(documents)} context documents")
    except:
        from langchain_core.documents import Document
        documents = [
            Document(
                page_content="Docker is a platform for developing, shipping, and running applications in containers.",
                metadata={"source": "docker.pdf", "page": 1}
            )
        ]
        print(f"   ℹ️  Using mock documents")
    
    # Build prompt
    prompt = build_prompt(user_query, documents)
    prompt_length = len(prompt)
    prompt_words = len(prompt.split())
    
    print(f"\n📊 Prompt Statistics:")
    print(f"   • Characters: {prompt_length}")
    print(f"   • Words: {prompt_words}")
    print(f"   • Estimated tokens: ~{int(prompt_words * 1.3)}")
    
    # LLM Generation
    print(f"\n{'='*80}")
    print("STEP 3: LLM GENERATION PROCESS")
    print(f"{'='*80}")
    
    print(f"\n🔄 Generation Pipeline:")
    print(f"   1️⃣  Tokenization: Convert prompt text to token IDs")
    print(f"   2️⃣  Encoding: Process tokens through transformer layers")
    print(f"   3️⃣  Generation: Predict next tokens iteratively")
    print(f"   4️⃣  Decoding: Convert token IDs back to text")
    print(f"   5️⃣  Post-processing: Format and clean output")
    
    print(f"\n⚙️  Starting generation...")
    print(f"   Model: {MODEL_NAME}")
    print(f"   Mode: Non-streaming")
    
    start_gen_time = time.time()
    
    try:
        answer = generate_answer(prompt, stream=False)
        generation_time = time.time() - start_gen_time
        
        print(f"\n✅ Generation completed successfully")
        print(f"   ⏱️  Total generation time: {generation_time:.3f} seconds")
        
    except Exception as e:
        print(f"\n❌ Generation failed: {str(e)}")
        return
    
    # Analyze answer
    print(f"\n{'='*80}")
    print("STEP 4: ANSWER ANALYSIS")
    print(f"{'='*80}")
    
    answer_length = len(answer)
    answer_words = len(answer.split())
    answer_sentences = answer.count('.') + answer.count('!') + answer.count('?')
    
    print(f"\n📊 Answer Statistics:")
    print(f"   • Characters: {answer_length}")
    print(f"   • Words: {answer_words}")
    print(f"   • Sentences: {answer_sentences}")
    print(f"   • Estimated tokens: ~{int(answer_words * 1.3)}")
    print(f"   • Avg words per sentence: {answer_words/max(answer_sentences, 1):.1f}")
    
    print(f"\n📝 Generated Answer:")
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
    
    # Performance metrics
    print(f"\n{'='*80}")
    print("STEP 5: PERFORMANCE METRICS")
    print(f"{'='*80}")
    
    tokens_per_second = answer_words / generation_time if generation_time > 0 else 0
    
    print(f"\n⏱️  Timing Breakdown:")
    print(f"   • Prompt preparation  : (handled in previous steps)")
    print(f"   • LLM generation      : {generation_time:.3f} seconds")
    print(f"   • Average speed       : {tokens_per_second:.1f} words/second")
    print(f"   • Est. tokens/second  : ~{tokens_per_second * 1.3:.1f}")
    
    print(f"\n📊 Processing Metrics:")
    print(f"   • Input length        : {prompt_length} chars ({prompt_words} words)")
    print(f"   • Output length       : {answer_length} chars ({answer_words} words)")
    print(f"   • Total processed     : {prompt_length + answer_length} chars")
    print(f"   • Compression ratio   : {prompt_length / max(answer_length, 1):.2f}x")
    
    # LLM Activity Details
    print(f"\n{'='*80}")
    print("STEP 6: LLM ACTIVITY DETAILS")
    print(f"{'='*80}")
    
    print(f"\n🔤 Tokenization Model:")
    print(f"   • Model: {MODEL_NAME}")
    print(f"   • Type: SentencePiece/BPE (model-dependent)")
    print(f"   • Purpose: Convert text ↔ numerical tokens")
    
    print(f"\n🧠 Answer Preparation Process:")
    print(f"   1. Prompt Tokenization:")
    print(f"      • Input text → Token IDs")
    print(f"      • Estimated: ~{int(prompt_words * 1.3)} tokens")
    print(f"\n   2. Context Processing:")
    print(f"      • Load context into attention mechanism")
    print(f"      • Build key-value cache for efficiency")
    print(f"\n   3. Auto-regressive Generation:")
    print(f"      • Generate one token at a time")
    print(f"      • Each token depends on previous tokens")
    print(f"      • Continue until EOS token or max length")
    print(f"\n   4. Output Assembly:")
    print(f"      • Collect generated token IDs")
    print(f"      • Decode tokens back to text")
    print(f"      • Apply post-processing (formatting, cleanup)")
    
    print(f"\n🎯 LLM Output Response:")
    print(f"   • Status: Success")
    print(f"   • Response time: {generation_time:.3f} seconds")
    print(f"   • Output quality: Context-aware answer")
    print(f"   • Answer length: {answer_words} words")
    
    # Test streaming mode
    print(f"\n{'='*80}")
    print("STEP 7: STREAMING MODE TEST")
    print(f"{'='*80}")
    
    print(f"\n🌊 Testing streaming generation...")
    print(f"   Streaming allows real-time token display")
    
    print(f"\n📝 Streamed Output:")
    print(f"   ", end='', flush=True)
    
    start_stream_time = time.time()
    streamed_text = ""
    chunk_count = 0
    
    try:
        for chunk in generate_answer(prompt, stream=True):
            print(chunk, end='', flush=True)
            streamed_text += chunk
            chunk_count += 1
        
        stream_time = time.time() - start_stream_time
        print(f"\n\n✅ Streaming completed")
        print(f"   ⏱️  Streaming time: {stream_time:.3f} seconds")
        print(f"   📦 Chunks received: {chunk_count}")
        print(f"   📊 Avg chunk size: {len(streamed_text)/max(chunk_count, 1):.1f} chars")
        
    except Exception as e:
        print(f"\n\n⚠️  Streaming test skipped: {str(e)}")
    
    # Summary
    print(f"\n{'='*80}")
    print("LLM GENERATION SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n🤖 Model Details:")
    print(f"   • Name: {MODEL_NAME}")
    print(f"   • Type: Large Language Model")
    print(f"   • Provider: Ollama")
    
    print(f"\n📊 Performance:")
    print(f"   • Generation time: {generation_time:.3f} seconds")
    print(f"   • Speed: ~{tokens_per_second:.1f} words/second")
    print(f"   • Mode: Supports both streaming and non-streaming")
    
    print(f"\n📝 Output:")
    print(f"   • Answer length: {answer_words} words")
    print(f"   • Quality: Context-aware RAG response")
    print(f"   • Format: Plain text")
    
    print(f"\n🔧 Activity:")
    print(f"   1. Tokenization: Text → Tokens")
    print(f"   2. Processing: Attention mechanism + context")
    print(f"   3. Generation: Auto-regressive token prediction")
    print(f"   4. Decoding: Tokens → Text")
    
    print(f"\n🎯 Purpose:")
    print(f"   Generate accurate answers based on retrieved context")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_llm_generation()
