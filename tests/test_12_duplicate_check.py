"""
Test 12: Duplicate Chunk Detection
-----------------------------------
Tests duplicate detection using SHA-256 hashing.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.services.database import get_vector_db, get_existing_hashes
from src.services.chunking import generate_chunk_hash
import hashlib

def test_duplicate_detection():
    """Test duplicate chunk detection system"""
    print("\n" + "="*80)
    print("TEST 12: DUPLICATE CHUNK DETECTION")
    print("="*80)
    
    # Get vector database
    print(f"\n{'─'*80}")
    print("Connecting to Vector Database...")
    print(f"{'─'*80}")
    
    try:
        vector_db = get_vector_db()
        collection = vector_db._collection
        print(f"   ✅ Connected successfully")
        
        # Get all chunks
        results = collection.get(include=['metadatas', 'documents'])
        total_chunks = len(results['ids'])
        print(f"   📊 Total chunks in database: {total_chunks}")
        
    except Exception as e:
        print(f"   ❌ Connection failed: {str(e)}")
        return
    
    # Analyze chunk hashes
    print(f"\n{'='*80}")
    print("HASH ANALYSIS")
    print(f"{'='*80}")
    
    print(f"\n🔐 Hashing Method: SHA-256")
    print(f"   • Algorithm: Secure Hash Algorithm 256-bit")
    print(f"   • Output: 64 hexadecimal characters")
    print(f"   • Purpose: Unique identification of chunks")
    
    # Collect hashes
    chunk_hashes = {}
    chunks_without_hash = 0
    hash_sources = {}
    
    for i, (chunk_id, metadata, content) in enumerate(zip(results['ids'], results['metadatas'], results['documents'])):
        if metadata and 'chunk_hash' in metadata:
            chunk_hash = metadata['chunk_hash']
            
            if chunk_hash not in chunk_hashes:
                chunk_hashes[chunk_hash] = []
            
            chunk_hashes[chunk_hash].append({
                'id': chunk_id,
                'content': content,
                'source': metadata.get('source', 'unknown'),
                'page': metadata.get('page', 'N/A')
            })
            
            # Track hash distribution by source
            source = metadata.get('source', 'unknown')
            hash_sources[source] = hash_sources.get(source, 0) + 1
        else:
            chunks_without_hash += 1
    
    # Statistics
    print(f"\n📊 Hash Statistics:")
    print(f"   • Total chunks         : {total_chunks}")
    print(f"   • Chunks with hash     : {total_chunks - chunks_without_hash}")
    print(f"   • Chunks without hash  : {chunks_without_hash}")
    print(f"   • Unique hashes        : {len(chunk_hashes)}")
    
    if chunks_without_hash > 0:
        print(f"\n   ⚠️  Warning: {chunks_without_hash} chunks don't have hash metadata")
        print(f"       These chunks were indexed before deduplication was implemented")
    
    # Check for duplicates
    print(f"\n{'='*80}")
    print("DUPLICATE DETECTION")
    print(f"{'='*80}")
    
    duplicates_found = {hash_val: chunks for hash_val, chunks in chunk_hashes.items() if len(chunks) > 1}
    
    if duplicates_found:
        print(f"\n❌ DUPLICATES FOUND!")
        print(f"   • Duplicate hash groups: {len(duplicates_found)}")
        print(f"   • Total duplicate chunks: {sum(len(chunks) for chunks in duplicates_found.values())}")
        
        print(f"\n📋 Duplicate Details:")
        for idx, (hash_val, chunks) in enumerate(duplicates_found.items(), 1):
            print(f"\n   ┌{'─'*74}┐")
            print(f"   │ DUPLICATE GROUP #{idx}" + " "*51 + "│")
            print(f"   └{'─'*74}┘")
            
            print(f"\n   🆔 Hash: {hash_val}")
            print(f"   📦 Duplicate count: {len(chunks)}")
            
            for j, chunk in enumerate(chunks, 1):
                print(f"\n   Occurrence {j}:")
                print(f"      • Chunk ID: {chunk['id']}")
                print(f"      • Source: {chunk['source']}")
                print(f"      • Page: {chunk['page']}")
                content_preview = chunk['content'][:100].replace('\n', ' ')
                print(f"      • Content: {content_preview}...")
    else:
        print(f"\n✅ NO DUPLICATES FOUND")
        print(f"   All {len(chunk_hashes)} chunks are unique")
        print(f"   Deduplication system working correctly!")
    
    # Hash generation demonstration
    print(f"\n{'='*80}")
    print("HASH GENERATION DEMONSTRATION")
    print(f"{'='*80}")
    
    demo_content = "Docker is a platform for developing applications in containers."
    demo_source = "docker.pdf"
    demo_page = 1
    
    print(f"\n📝 Sample Chunk:")
    print(f"   Content: \"{demo_content}\"")
    print(f"   Source: {demo_source}")
    print(f"   Page: {demo_page}")
    
    # Generate hash
    demo_hash = generate_chunk_hash(demo_content, demo_source, demo_page)
    
    print(f"\n🔐 Hash Generation Process:")
    print(f"   1. Combine: content + '|' + source + '|' + page")
    hash_input = f"{demo_content}|{demo_source}|{demo_page}"
    print(f"      Input string: \"{hash_input}\"")
    
    print(f"\n   2. Encode to bytes:")
    hash_bytes = hash_input.encode('utf-8')
    print(f"      Bytes length: {len(hash_bytes)}")
    
    print(f"\n   3. Apply SHA-256:")
    print(f"      Hash (hex): {demo_hash}")
    print(f"      Hash length: {len(demo_hash)} characters")
    
    # Test hash uniqueness
    print(f"\n🧪 Hash Uniqueness Test:")
    
    # Same content, same source, same page → Same hash
    hash1 = generate_chunk_hash(demo_content, demo_source, demo_page)
    print(f"\n   Test 1: Same content, same source, same page")
    print(f"      Hash 1: {hash1[:32]}...")
    print(f"      Hash 2: {hash1[:32]}...")
    print(f"      Result: {'✅ IDENTICAL (as expected)' if hash1 == demo_hash else '❌ DIFFERENT'}")
    
    # Same content, different source → Different hash
    hash2 = generate_chunk_hash(demo_content, "container.pdf", demo_page)
    print(f"\n   Test 2: Same content, different source")
    print(f"      Hash 1: {demo_hash[:32]}...")
    print(f"      Hash 2: {hash2[:32]}...")
    print(f"      Result: {'✅ DIFFERENT (as expected)' if hash2 != demo_hash else '❌ IDENTICAL'}")
    
    # Same content, same source, different page → Different hash
    hash3 = generate_chunk_hash(demo_content, demo_source, 2)
    print(f"\n   Test 3: Same content, same source, different page")
    print(f"      Hash 1: {demo_hash[:32]}...")
    print(f"      Hash 2: {hash3[:32]}...")
    print(f"      Result: {'✅ DIFFERENT (as expected)' if hash3 != demo_hash else '❌ IDENTICAL'}")
    
    # Hash distribution
    print(f"\n{'='*80}")
    print("HASH DISTRIBUTION BY SOURCE")
    print(f"{'='*80}")
    
    print(f"\n📊 Chunks per Document:")
    for source, count in sorted(hash_sources.items()):
        percentage = (count / total_chunks) * 100
        print(f"   • {source:30s}: {count:4d} chunks ({percentage:5.1f}%)")
    
    # Summary
    print(f"\n{'='*80}")
    print("DUPLICATE DETECTION SUMMARY")
    print(f"{'='*80}")
    
    print(f"\n📊 Statistics:")
    print(f"   • Total chunks         : {total_chunks}")
    print(f"   • Unique chunks        : {len(chunk_hashes)}")
    print(f"   • Duplicate groups     : {len(duplicates_found)}")
    print(f"   • Duplication rate     : {(sum(len(chunks) - 1 for chunks in duplicates_found.values()) / max(total_chunks, 1) * 100):.2f}%")
    
    print(f"\n🔐 Deduplication Method:")
    print(f"   • Algorithm: SHA-256 hashing")
    print(f"   • Hash input: content + source + page")
    print(f"   • Hash output: 64-character hex string")
    print(f"   • Storage: Stored in chunk metadata")
    
    print(f"\n✅ Deduplication Benefits:")
    print(f"   • Prevents duplicate storage")
    print(f"   • Reduces database size")
    print(f"   • Improves search performance")
    print(f"   • Maintains data consistency")
    
    print(f"\n🎯 Status:")
    if not duplicates_found:
        print(f"   ✅ PASS: No duplicates detected")
        print(f"   System is functioning correctly!")
    else:
        print(f"   ⚠️  WARNING: {len(duplicates_found)} duplicate groups found")
        print(f"   Consider re-indexing to remove duplicates")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_duplicate_detection()
