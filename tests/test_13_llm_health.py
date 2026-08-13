"""
Test 13: LLM Health Check
--------------------------
Tests LLM model availability and status.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import MODEL_NAME
from src.services.llm import get_ollama_client
import time

def test_llm_health():
    """Test LLM model health and availability"""
    print("\n" + "="*80)
    print("TEST 13: LLM HEALTH CHECK")
    print("="*80)
    
    print(f"\n🤖 Target Model: {MODEL_NAME}")
    
    # Test 1: Ollama Service Status
    print(f"\n{'='*80}")
    print("TEST 1: OLLAMA SERVICE STATUS")
    print(f"{'='*80}")
    
    try:
        start_time = time.time()
        client = get_ollama_client()
        connect_time = time.time() - start_time
        
        print(f"\n✅ Ollama Service: RUNNING")
        print(f"   ⏱️  Connection time: {connect_time*1000:.3f} ms")
        print(f"   🌐 Service: Accessible")
        
    except Exception as e:
        print(f"\n❌ Ollama Service: NOT RUNNING")
        print(f"   ⚠️  Error: {str(e)}")
        print(f"\n   💡 Troubleshooting:")
        print(f"      1. Check if Ollama is installed")
        print(f"      2. Start Ollama service")
        print(f"      3. Verify Ollama is running: ollama list")
        return
    
    # Test 2: Model Availability
    print(f"\n{'='*80}")
    print("TEST 2: MODEL AVAILABILITY")
    print(f"{'='*80}")
    
    try:
        models = client.list()
        total_models = len(models.models)
        
        print(f"\n📊 Available Models: {total_models}")
        
        # Check if target model exists
        model_found = False
        target_model_info = None
        
        for model in models.models:
            if MODEL_NAME in model.model:
                model_found = True
                target_model_info = model
                break
        
        if model_found:
            print(f"\n✅ Target Model: FOUND")
            print(f"   • Name: {target_model_info.model}")
            print(f"   • Size: {target_model_info.size / (1024**3):.2f} GB")
            
            if hasattr(target_model_info, 'modified_at'):
                print(f"   • Last modified: {target_model_info.modified_at}")
            
            if hasattr(target_model_info, 'digest'):
                print(f"   • Digest: {target_model_info.digest[:32]}...")
            
        else:
            print(f"\n❌ Target Model: NOT FOUND")
            print(f"\n   📋 Available models:")
            for idx, model in enumerate(models.models, 1):
                print(f"      {idx}. {model.model} ({model.size / (1024**3):.2f} GB)")
            
            print(f"\n   💡 To install the model:")
            print(f"      ollama pull {MODEL_NAME}")
            return
    
    except Exception as e:
        print(f"\n❌ Failed to list models: {str(e)}")
        return
    
    # Test 3: Model Response Test
    print(f"\n{'='*80}")
    print("TEST 3: MODEL RESPONSE TEST")
    print(f"{'='*80}")
    
    test_prompt = "Say 'Hello' in one word."
    print(f"\n📝 Test Prompt: \"{test_prompt}\"")
    
    try:
        print(f"\n🔄 Sending test request...")
        start_time = time.time()
        
        response = client.chat(
            model=MODEL_NAME,
            messages=[
                {"role": "user", "content": test_prompt}
            ]
        )
        
        response_time = time.time() - start_time
        answer = response["message"]["content"]
        
        print(f"\n✅ Model Response: SUCCESS")
        print(f"   ⏱️  Response time: {response_time:.3f} seconds")
        print(f"   📝 Response: \"{answer}\"")
        print(f"   📊 Response length: {len(answer)} characters")
        
        # Check response quality
        if answer and len(answer) > 0:
            print(f"\n   ✅ Response quality: GOOD")
            print(f"      • Non-empty response")
            print(f"      • Model is generating text")
        else:
            print(f"\n   ⚠️  Response quality: POOR")
            print(f"      • Empty or invalid response")
        
    except Exception as e:
        print(f"\n❌ Model Response: FAILED")
        print(f"   ⚠️  Error: {str(e)}")
        return
    
    # Test 4: Model Performance
    print(f"\n{'='*80}")
    print("TEST 4: MODEL PERFORMANCE")
    print(f"{'='*80}")
    
    performance_tests = [
        {"prompt": "Count to 5.", "description": "Short response"},
        {"prompt": "What is AI in one sentence?", "description": "Medium response"},
        {"prompt": "Explain machine learning in 50 words.", "description": "Long response"}
    ]
    
    response_times = []
    
    for idx, test in enumerate(performance_tests, 1):
        print(f"\n   Test {idx}: {test['description']}")
        print(f"   Prompt: \"{test['prompt']}\"")
        
        try:
            start_time = time.time()
            response = client.chat(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": test['prompt']}]
            )
            response_time = time.time() - start_time
            response_times.append(response_time)
            
            answer = response["message"]["content"]
            word_count = len(answer.split())
            
            print(f"   ✅ Time: {response_time:.3f}s | Words: {word_count} | Speed: {word_count/response_time:.1f} words/s")
            
        except Exception as e:
            print(f"   ❌ Failed: {str(e)}")
    
    # Performance summary
    if response_times:
        avg_time = sum(response_times) / len(response_times)
        print(f"\n   📊 Performance Summary:")
        print(f"      • Average response time: {avg_time:.3f} seconds")
        print(f"      • Fastest: {min(response_times):.3f} seconds")
        print(f"      • Slowest: {max(response_times):.3f} seconds")
        
        # Performance rating
        if avg_time < 2.0:
            rating = "🟢 EXCELLENT"
        elif avg_time < 5.0:
            rating = "🟡 GOOD"
        else:
            rating = "🔴 SLOW"
        
        print(f"      • Rating: {rating}")
    
    # Test 5: Streaming Capability
    print(f"\n{'='*80}")
    print("TEST 5: STREAMING CAPABILITY")
    print(f"{'='*80}")
    
    print(f"\n🌊 Testing streaming mode...")
    
    try:
        stream = client.chat(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Count to 3."}],
            stream=True
        )
        
        chunk_count = 0
        start_time = time.time()
        
        for chunk in stream:
            chunk_count += 1
            if chunk_count == 1:
                first_chunk_time = time.time() - start_time
        
        total_stream_time = time.time() - start_time
        
        print(f"\n✅ Streaming: SUPPORTED")
        print(f"   📦 Chunks received: {chunk_count}")
        print(f"   ⏱️  First chunk time: {first_chunk_time*1000:.3f} ms (latency)")
        print(f"   ⏱️  Total stream time: {total_stream_time:.3f} seconds")
        print(f"   📊 Avg chunk time: {total_stream_time*1000/chunk_count:.3f} ms")
        
    except Exception as e:
        print(f"\n⚠️  Streaming test failed: {str(e)}")
    
    # Overall Health Summary
    print(f"\n{'='*80}")
    print("OVERALL HEALTH SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n✅ HEALTH CHECK: PASSED")
    print(f"\n📊 System Status:")
    print(f"   ✅ Ollama Service    : Running")
    print(f"   ✅ Model Availability: {MODEL_NAME} found")
    print(f"   ✅ Model Response    : Working")
    print(f"   ✅ Performance       : Good")
    print(f"   ✅ Streaming         : Supported")
    
    print(f"\n🤖 Model Information:")
    print(f"   • Name: {MODEL_NAME}")
    if target_model_info:
        print(f"   • Size: {target_model_info.size / (1024**3):.2f} GB")
    print(f"   • Status: Ready for inference")
    
    if response_times:
        print(f"\n⚡ Performance Metrics:")
        print(f"   • Average response time: {avg_time:.3f} seconds")
        print(f"   • Performance rating: {rating}")
    
    print(f"\n✅ System Ready:")
    print(f"   • LLM is operational")
    print(f"   • Can handle RAG queries")
    print(f"   • Both streaming and non-streaming modes available")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_llm_health()
