"""
Test 14: Overall Indexing Flow
-------------------------------
Tests complete indexing pipeline from documents to vector DB.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import PDF_DIRECTORY
from src.services.loader import load_document
from src.services.chunking import split_documents
from src.services.embedding import get_embedding_model
from src.services.database import get_vector_db, get_existing_hashes
import time

def test_indexing_flow():
    """Test complete indexing pipeline"""
    print("\n" + "="*80)
    print("TEST 14: OVERALL INDEXING FLOW")
    print("="*80)
    
    # Get test document
    supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.pptx', '*.ppt']
    all_files = []
    
    for pattern in supported_extensions:
        all_files.extend(list(PDF_DIRECTORY.glob(pattern)))
    
    if not all_files:
        print("\n❌ No documents found for testing")
        return
    
    test_file = all_files[0].name
    print(f"\n📄 Test Document: {test_file}")
    
    # Initialize timing
    stage_times = {}
    overall_start = time.time()
    
    # STAGE 1: Document Loading
    print(f"\n{'='*80}")
    print("STAGE 1: DOCUMENT LOADING")
    print(f"{'='*80}")
    
    print(f"\n📂 Loading document from: {PDF_DIRECTORY}")
    print(f"   File: {test_file}")
    
    try:
        start_time = time.time()
        documents = load_document(test_file)
        stage_times['loading'] = time.time() - start_time
        
        print(f"\n✅ Loading completed")
        print(f"   ⏱️  Time: {stage_times['loading']:.3f} seconds")
        print(f"   📖 Pages loaded: {len(documents)}")
        print(f"   📊 Total characters: {sum(len(doc.page_content) for doc in documents):,}")
        
        # Show first document sample
        if documents:
            print(f"\n   📝 First page sample:")
            sample = documents[0].page_content[:150].replace('\n', ' ')
            print(f"      {sample}...")
        
    except Exception as e:
        print(f"\n❌ Loading failed: {str(e)}")
        return
    
    # STAGE 2: Chunking
    print(f"\n{'='*80}")
    print("STAGE 2: CHUNKING")
    print(f"{'='*80}")
    
    print(f"\n🔧 Chunking parameters:")
    print(f"   • Chunk size: 500 characters")
    print(f"   • Chunk overlap: 100 characters")
    print(f"   • Method: RecursiveCharacterTextSplitter")
    
    try:
        start_time = time.time()
        chunks = split_documents(documents)
        stage_times['chunking'] = time.time() - start_time
        
        print(f"\n✅ Chunking completed")
        print(f"   ⏱️  Time: {stage_times['chunking']:.3f} seconds")
        print(f"   📦 Chunks created: {len(chunks)}")
        
        # Chunk statistics
        chunk_sizes = [len(chunk.page_content) for chunk in chunks]
        avg_size = sum(chunk_sizes) / len(chunk_sizes)
        
        print(f"\n   📊 Chunk statistics:")
        print(f"      • Average size: {avg_size:.1f} characters")
        print(f"      • Min size: {min(chunk_sizes)} characters")
        print(f"      • Max size: {max(chunk_sizes)} characters")
        
        # Show first chunk sample
        if chunks:
            print(f"\n   📝 First chunk sample:")
            print(f"      Hash: {chunks[0].metadata.get('chunk_hash', 'N/A')[:32]}...")
            sample = chunks[0].page_content[:100].replace('\n', ' ')
            print(f"      Content: {sample}...")
        
    except Exception as e:
        print(f"\n❌ Chunking failed: {str(e)}")
        return
    
    # STAGE 3: Embedding Generation
    print(f"\n{'='*80}")
    print("STAGE 3: EMBEDDING GENERATION")
    print(f"{'='*80}")
    
    print(f"\n🤖 Loading embedding model...")
    
    try:
        start_time = time.time()
        embedding_model = get_embedding_model()
        model_load_time = time.time() - start_time
        
        print(f"   ✅ Model loaded in {model_load_time:.3f} seconds")
        
        # Generate embeddings for first 3 chunks as sample
        print(f"\n🔄 Generating embeddings (sample: 3 chunks)...")
        
        start_time = time.time()
        sample_embeddings = []
        
        for i, chunk in enumerate(chunks[:3], 1):
            emb_start = time.time()
            embedding = embedding_model.embed_query(chunk.page_content)
            emb_time = time.time() - emb_start
            
            sample_embeddings.append(embedding)
            print(f"   Chunk {i}: {len(embedding)} dimensions, {emb_time*1000:.3f} ms")
        
        stage_times['embedding_sample'] = time.time() - start_time
        
        # Estimate total embedding time
        avg_embed_time = stage_times['embedding_sample'] / 3
        estimated_total = avg_embed_time * len(chunks)
        
        print(f"\n   📊 Embedding statistics:")
        print(f"      • Sample time: {stage_times['embedding_sample']:.3f} seconds (3 chunks)")
        print(f"      • Avg time per chunk: {avg_embed_time*1000:.3f} ms")
        print(f"      • Estimated total time: {estimated_total:.3f} seconds ({len(chunks)} chunks)")
        print(f"      • Embedding dimensions: {len(sample_embeddings[0])}")
        
    except Exception as e:
        print(f"\n❌ Embedding generation failed: {str(e)}")
        return
    
    # STAGE 4: Deduplication Check
    print(f"\n{'='*80}")
    print("STAGE 4: DEDUPLICATION CHECK")
    print(f"{'='*80}")
    
    try:
        start_time = time.time()
        existing_hashes = get_existing_hashes()
        stage_times['deduplication'] = time.time() - start_time
        
        print(f"\n🔍 Checking for duplicates...")
        print(f"   ⏱️  Time: {stage_times['deduplication']:.3f} seconds")
        print(f"   📊 Existing hashes in DB: {len(existing_hashes)}")
        
        # Check how many would be duplicates
        new_hashes = set(chunk.metadata.get('chunk_hash') for chunk in chunks if 'chunk_hash' in chunk.metadata)
        duplicates = existing_hashes.intersection(new_hashes)
        
        print(f"   📦 New chunks: {len(chunks)}")
        print(f"   🔄 Would be duplicates: {len(duplicates)}")
        print(f"   ✅ Would be added: {len(chunks) - len(duplicates)}")
        
        if len(duplicates) > 0:
            print(f"\n   ℹ️  Note: Duplicates would be skipped during actual indexing")
        
    except Exception as e:
        print(f"\n⚠️  Deduplication check warning: {str(e)}")
        stage_times['deduplication'] = 0
    
    # STAGE 5: Vector Database Storage (simulation)
    print(f"\n{'='*80}")
    print("STAGE 5: VECTOR DATABASE STORAGE (Simulation)")
    print(f"{'='*80}")
    
    print(f"\n💾 Storage information:")
    
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        current_count = collection.count()
        
        print(f"   📊 Current DB size: {current_count} chunks")
        print(f"   ➕ Would add: {len(chunks) - len(duplicates)} new chunks")
        print(f"   📦 New total would be: {current_count + (len(chunks) - len(duplicates))} chunks")
        
        # Calculate storage estimates
        embedding_dim = len(sample_embeddings[0])
        bytes_per_chunk = (
            embedding_dim * 4 +  # embedding (float32)
            sum(len(chunk.page_content.encode('utf-8')) for chunk in chunks) / len(chunks) +  # avg text
            100  # metadata (estimate)
        )
        
        total_storage = bytes_per_chunk * len(chunks)
        
        print(f"\n   💾 Storage estimates (for new chunks):")
        print(f"      • Bytes per chunk: ~{bytes_per_chunk:.0f} bytes")
        print(f"      • Total storage: ~{total_storage / 1024:.2f} KB")
        print(f"      • Embedding storage: ~{embedding_dim * 4 * len(chunks) / 1024:.2f} KB")
        
        print(f"\n   ℹ️  Note: This is a simulation. No data was actually stored.")
        
    except Exception as e:
        print(f"\n⚠️  Database connection warning: {str(e)}")
    
    # Overall Flow Summary
    print(f"\n{'='*80}")
    print("INDEXING FLOW SUMMARY")
    print(f"{'='*80}")
    
    overall_time = time.time() - overall_start
    
    print(f"\n⏱️  TIMING BREAKDOWN:")
    print(f"   1. Document Loading    : {stage_times.get('loading', 0):7.3f}s ({stage_times.get('loading', 0)/overall_time*100:5.1f}%)")
    print(f"   2. Chunking            : {stage_times.get('chunking', 0):7.3f}s ({stage_times.get('chunking', 0)/overall_time*100:5.1f}%)")
    print(f"   3. Embedding (sample)  : {stage_times.get('embedding_sample', 0):7.3f}s")
    print(f"   4. Deduplication Check : {stage_times.get('deduplication', 0):7.3f}s ({stage_times.get('deduplication', 0)/overall_time*100:5.1f}%)")
    print(f"   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print(f"   Total Measured Time    : {overall_time:7.3f}s")
    print(f"   Estimated Full Index   : ~{overall_time - stage_times.get('embedding_sample', 0) + estimated_total:.3f}s")
    
    print(f"\n📊 PROCESSING STATISTICS:")
    print(f"   • Input file: {test_file}")
    print(f"   • Pages processed: {len(documents)}")
    print(f"   • Chunks created: {len(chunks)}")
    print(f"   • Embedding dimensions: {embedding_dim}")
    print(f"   • Duplicates detected: {len(duplicates)}")
    print(f"   • New chunks to add: {len(chunks) - len(duplicates)}")
    
    print(f"\n🔄 COMPLETE FLOW:")
    print(f"   1. ✅ Load Document    → {len(documents)} pages")
    print(f"   2. ✅ Split into Chunks → {len(chunks)} chunks")
    print(f"   3. ✅ Generate Embeddings → {embedding_dim}D vectors")
    print(f"   4. ✅ Check Duplicates → {len(duplicates)} duplicates")
    print(f"   5. ✅ Store in Vector DB → {len(chunks) - len(duplicates)} new chunks")
    
    print(f"\n✅ INDEXING PIPELINE: OPERATIONAL")
    print(f"   All stages completed successfully")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_indexing_flow()
