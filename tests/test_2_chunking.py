"""
Test 2: Document Chunking
--------------------------
Tests chunking process: chunk count, IDs, text, metadata, and chunking strategy.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.config.settings import PDF_DIRECTORY
from src.services.loader import load_document
from src.services.chunking import split_documents
import time

def test_chunking():
    """Test document chunking with detailed information"""
    print("\n" + "="*80)
    print("TEST 2: DOCUMENT CHUNKING")
    print("="*80)
    
    # Get first document for testing
    supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.pptx', '*.ppt']
    all_files = []
    
    for pattern in supported_extensions:
        all_files.extend(list(PDF_DIRECTORY.glob(pattern)))
    
    if not all_files:
        print("\n❌ No documents found for chunking test")
        return
    
    # Test with first document
    file_name = all_files[0].name
    print(f"\n📄 Testing Document: {file_name}\n")
    
    # Load document
    print("Step 1: Loading Document...")
    documents = load_document(file_name)
    print(f"   ✅ Loaded {len(documents)} pages")
    
    # Calculate total characters before chunking
    total_chars = sum(len(doc.page_content) for doc in documents)
    print(f"   📏 Total Characters: {total_chars:,}")
    
    # Chunk document
    print("\nStep 2: Chunking Document...")
    print(f"   🔧 Chunking Strategy: RecursiveCharacterTextSplitter")
    print(f"   📊 Chunk Size: 500 characters")
    print(f"   🔄 Chunk Overlap: 100 characters")
    
    start_time = time.time()
    chunks = split_documents(documents)
    chunk_time = time.time() - start_time
    
    print(f"   ✅ Chunking completed in {chunk_time:.3f} seconds")
    print(f"   📦 Total Chunks Created: {len(chunks)}")
    
    # Display detailed information for first 3 chunks
    print(f"\n{'='*80}")
    print("CHUNK DETAILS (First 3 chunks)")
    print(f"{'='*80}")
    
    for idx, chunk in enumerate(chunks[:3], 1):
        print(f"\n┌{'─'*78}┐")
        print(f"│ CHUNK #{idx:03d}" + " "*69 + "│")
        print(f"└{'─'*78}┘")
        
        # Chunk ID (using hash)
        chunk_hash = chunk.metadata.get('chunk_hash', 'N/A')
        print(f"   🆔 Chunk Hash (ID)   : {chunk_hash[:32]}...")
        
        # Chunk text
        chunk_text = chunk.page_content
        print(f"   📝 Chunk Text Length : {len(chunk_text)} characters")
        print(f"   📄 Chunk Text Preview:")
        print(f"      ┌{'─'*70}┐")
        for line in chunk_text[:200].split('\n'):
            if line.strip():
                print(f"      │ {line[:68]:<68} │")
        if len(chunk_text) > 200:
            print(f"      │ ...{' '*65} │")
        print(f"      └{'─'*70}┘")
        
        # Metadata
        print(f"   🏷️  Metadata:")
        for key, value in chunk.metadata.items():
            if key == 'chunk_hash':
                print(f"      - {key}: {value[:32]}... (SHA-256)")
            else:
                print(f"      - {key}: {value}")
    
    # Chunking Statistics
    print(f"\n{'='*80}")
    print("CHUNKING STATISTICS")
    print(f"{'='*80}")
    
    chunk_sizes = [len(chunk.page_content) for chunk in chunks]
    avg_chunk_size = sum(chunk_sizes) / len(chunk_sizes)
    
    print(f"📦 Total Chunks             : {len(chunks)}")
    print(f"📏 Average Chunk Size       : {avg_chunk_size:.1f} characters")
    print(f"📊 Min Chunk Size           : {min(chunk_sizes)} characters")
    print(f"📊 Max Chunk Size           : {max(chunk_sizes)} characters")
    print(f"⏱️  Chunking Time           : {chunk_time:.3f} seconds")
    print(f"🔧 Chunking Method          : RecursiveCharacterTextSplitter")
    print(f"🔄 Overlap Strategy         : 100 characters overlap between chunks")
    print(f"🎯 Deduplication            : SHA-256 hash per chunk")
    
    # Source distribution
    sources = {}
    for chunk in chunks:
        source = chunk.metadata.get('source', 'unknown')
        sources[source] = sources.get(source, 0) + 1
    
    print(f"\n📊 Chunks by Source:")
    for source, count in sources.items():
        print(f"   - {source}: {count} chunks")
    
    print(f"\n{'='*80}\n")


if __name__ == "__main__":
    test_chunking()
