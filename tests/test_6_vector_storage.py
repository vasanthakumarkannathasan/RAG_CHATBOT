"""
Test 6: Vector Database Storage
--------------------------------
Tests vector DB: storage count, memory usage, chunk details.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import VECTOR_DB_PATH, COLLECTION_NAME
from src.services.database import get_vector_db, get_collection_count
import numpy as np
import time

def get_directory_size(path):
    """Calculate total size of directory"""
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(path):
        for filename in filenames:
            filepath = os.path.join(dirpath, filename)
            if os.path.exists(filepath):
                total_size += os.path.getsize(filepath)
    return total_size

def test_vector_storage():
    """Test vector database storage with detailed information"""
    print("\n" + "="*80)
    print("TEST 6: VECTOR DATABASE STORAGE")
    print("="*80)
    
    print(f"\n📂 Vector DB Path: {VECTOR_DB_PATH}")
    print(f"📦 Collection Name: {COLLECTION_NAME}")
    
    # Database size
    if os.path.exists(VECTOR_DB_PATH):
        db_size = get_directory_size(VECTOR_DB_PATH)
        print(f"💾 Database Size: {db_size / (1024*1024):.2f} MB ({db_size:,} bytes)")
    
    # Get vector database
    print(f"\n{'─'*80}")
    print("Connecting to Vector Database...")
    print(f"{'─'*80}")
    
    try:
        start_time = time.time()
        vector_db = get_vector_db()
        connect_time = time.time() - start_time
        
        print(f"   ✅ Connected successfully")
        print(f"   ⏱️  Connection time: {connect_time:.3f} seconds")
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return
    
    # Get collection info
    collection = vector_db._collection
    
    print(f"\n{'='*80}")
    print("COLLECTION INFORMATION")
    print(f"{'='*80}")
    
    # Get all documents
    try:
        results = collection.get(include=['embeddings', 'metadatas', 'documents'])
        
        total_vectors = len(results['ids'])
        print(f"\n📊 Storage Statistics:")
        print(f"   🔢 Total Vectors Stored  : {total_vectors:,}")
        print(f"   📦 Collection Name       : {COLLECTION_NAME}")
        print(f"   💾 Storage Location      : {VECTOR_DB_PATH}")
        
        if total_vectors > 0:
            # Calculate embedding dimensions
            if results['embeddings'] and len(results['embeddings']) > 0:
                embedding_dim = len(results['embeddings'][0])
                total_embedding_values = total_vectors * embedding_dim
                embedding_memory = total_embedding_values * 4  # 4 bytes per float32
                
                print(f"   🔢 Embedding Dimensions  : {embedding_dim}")
                print(f"   📈 Total Embedding Values: {total_embedding_values:,}")
                print(f"   💾 Embeddings Memory     : {embedding_memory / (1024*1024):.2f} MB")
            
            # Document sources
            sources = {}
            for metadata in results['metadatas']:
                if metadata and 'source' in metadata:
                    source = metadata['source']
                    sources[source] = sources.get(source, 0) + 1
            
            print(f"\n📄 Documents Indexed:")
            for source, count in sources.items():
                print(f"   • {source}: {count} chunks")
        
        # Display detailed info for first 3 vectors
        print(f"\n{'='*80}")
        print("VECTOR DETAILS (First 3 vectors)")
        print(f"{'='*80}")
        
        for i in range(min(3, total_vectors)):
            print(f"\n┌{'─'*78}┐")
            print(f"│ VECTOR #{i+1}" + " "*67 + "│")
            print(f"└{'─'*78}┘")
            
            # Chunk ID
            chunk_id = results['ids'][i]
            print(f"\n🆔 Chunk ID:")
            print(f"   {chunk_id}")
            
            # Original text
            original_text = results['documents'][i]
            print(f"\n📝 Chunk Original Text:")
            text_preview = original_text[:200].replace('\n', ' ')
            print(f"   \"{text_preview}...")
            print(f"   Length: {len(original_text)} characters")
            
            # Embedding info
            if results['embeddings'] and len(results['embeddings']) > i:
                embedding = np.array(results['embeddings'][i])
                
                print(f"\n🔢 Chunk Embedding Info:")
                print(f"   📊 Dimensions    : {len(embedding)}")
                print(f"   📏 Vector shape  : {embedding.shape}")
                print(f"   📉 Min value     : {embedding.min():.6f}")
                print(f"   📈 Max value     : {embedding.max():.6f}")
                print(f"   🎯 Mean value    : {embedding.mean():.6f}")
                print(f"   📐 Std deviation : {embedding.std():.6f}")
                print(f"   🔗 L2 Norm       : {np.linalg.norm(embedding):.6f}")
                
                print(f"\n   🔢 Embedding values (first 10):")
                first_10 = ', '.join(f"{val:.4f}" for val in embedding[:10])
                print(f"      [{first_10}, ...]")
                
                print(f"\n   🔢 Embedding values (last 10):")
                last_10 = ', '.join(f"{val:.4f}" for val in embedding[-10:])
                print(f"      [..., {last_10}]")
            
            # Metadata
            metadata = results['metadatas'][i]
            print(f"\n🏷️  Metadata:")
            if metadata:
                for key, value in metadata.items():
                    if key == 'chunk_hash':
                        print(f"   - {key}: {value[:32]}... (SHA-256)")
                    else:
                        print(f"   - {key}: {value}")
            else:
                print(f"   No metadata available")
            
            # Storage calculation
            if results['embeddings'] and len(results['embeddings']) > i:
                vector_size = len(results['embeddings'][i]) * 4  # 4 bytes per float32
                text_size = len(original_text.encode('utf-8'))
                metadata_size = len(str(metadata).encode('utf-8'))
                total_size = vector_size + text_size + metadata_size
                
                print(f"\n💾 Storage Breakdown:")
                print(f"   • Embedding  : {vector_size:,} bytes ({vector_size/1024:.2f} KB)")
                print(f"   • Text       : {text_size:,} bytes")
                print(f"   • Metadata   : {metadata_size:,} bytes")
                print(f"   • Total      : {total_size:,} bytes ({total_size/1024:.2f} KB)")
        
        # Summary
        print(f"\n{'='*80}")
        print("STORAGE SUMMARY")
        print(f"{'='*80}")
        
        if total_vectors > 0 and results['embeddings']:
            embedding_dim = len(results['embeddings'][0])
            total_embedding_memory = total_vectors * embedding_dim * 4
            
            # Calculate text memory
            total_text_memory = sum(len(doc.encode('utf-8')) for doc in results['documents'])
            
            # Calculate metadata memory
            total_metadata_memory = sum(len(str(m).encode('utf-8')) for m in results['metadatas'])
            
            print(f"\n💾 Memory Usage Breakdown:")
            print(f"   📊 Embeddings        : {total_embedding_memory / (1024*1024):.2f} MB")
            print(f"   📝 Original Text     : {total_text_memory / (1024*1024):.2f} MB")
            print(f"   🏷️  Metadata          : {total_metadata_memory / (1024*1024):.2f} MB")
            print(f"   ━━━━━━━━━━━━━━━━━━━━")
            print(f"   📦 Total (estimated) : {(total_embedding_memory + total_text_memory + total_metadata_memory) / (1024*1024):.2f} MB")
            
            print(f"\n📊 Storage Statistics:")
            print(f"   🔢 Total Vectors         : {total_vectors:,}")
            print(f"   📏 Vector Dimensions     : {embedding_dim}")
            print(f"   📦 Total Values          : {total_vectors * embedding_dim:,}")
            print(f"   💾 Database Size (disk)  : {db_size / (1024*1024):.2f} MB")
            print(f"   🗂️  Collection Name       : {COLLECTION_NAME}")
            print(f"   📂 Storage Type          : ChromaDB (Persistent)")
            print(f"   🔍 Search Type           : Similarity Search (Cosine)")
            
            print(f"\n📄 Indexed Documents:")
            for source, count in sources.items():
                avg_chunk_size = total_text_memory / total_vectors
                print(f"   • {source}:")
                print(f"       - Chunks: {count}")
                print(f"       - Avg chunk size: {avg_chunk_size:.0f} bytes")
        
    except Exception as e:
        print(f"\n❌ Error retrieving collection data: {str(e)}")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_vector_storage()
