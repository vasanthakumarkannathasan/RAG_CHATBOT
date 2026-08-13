"""
Test 1: Document Loading
-------------------------
Tests how many documents are loaded and their page counts.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from pathlib import Path
from src.config.settings import PDF_DIRECTORY
from src.services.loader import load_document
from src.utils.logger import logger
import time

def test_document_loading():
    """Test loading documents and display statistics"""
    print("\n" + "="*80)
    print("TEST 1: DOCUMENT LOADING")
    print("="*80)
    
    # Get all supported documents
    supported_extensions = ['*.pdf', '*.docx', '*.doc', '*.pptx', '*.ppt']
    all_files = []
    
    for pattern in supported_extensions:
        all_files.extend(list(PDF_DIRECTORY.glob(pattern)))
    
    if not all_files:
        print(f"\n❌ No documents found in: {PDF_DIRECTORY}")
        print("   Supported formats: PDF, Word (.docx, .doc), PowerPoint (.pptx, .ppt)")
        return
    
    print(f"\n📁 Document Directory: {PDF_DIRECTORY}")
    print(f"📊 Total Documents Found: {len(all_files)}\n")
    
    total_pages = 0
    loading_times = []
    
    for idx, file_path in enumerate(all_files, 1):
        file_name = file_path.name
        file_type = file_path.suffix.upper()
        file_size = file_path.stat().st_size / 1024  # Size in KB
        
        print(f"\n{'─'*80}")
        print(f"📄 Document #{idx}: {file_name}")
        print(f"{'─'*80}")
        print(f"   📋 File Type     : {file_type}")
        print(f"   📏 File Size     : {file_size:.2f} KB")
        
        try:
            start_time = time.time()
            documents = load_document(file_name)
            load_time = time.time() - start_time
            loading_times.append(load_time)
            
            page_count = len(documents)
            total_pages += page_count
            
            print(f"   ✅ Load Status   : SUCCESS")
            print(f"   ⏱️  Load Time     : {load_time:.3f} seconds")
            print(f"   📖 Page Count    : {page_count} pages")
            
            # Show sample content from first page
            if documents:
                first_page_preview = documents[0].page_content[:200].replace('\n', ' ')
                print(f"   📝 First Page Preview:")
                print(f"      {first_page_preview}...")
                
                # Show metadata
                print(f"   🏷️  Metadata:")
                for key, value in documents[0].metadata.items():
                    print(f"      - {key}: {value}")
            
        except Exception as e:
            print(f"   ❌ Load Status   : FAILED")
            print(f"   ⚠️  Error        : {str(e)}")
    
    # Summary
    print(f"\n{'='*80}")
    print("LOADING SUMMARY")
    print(f"{'='*80}")
    print(f"✅ Total Documents Loaded    : {len(all_files)}")
    print(f"📖 Total Pages Loaded        : {total_pages}")
    print(f"⏱️  Average Loading Time     : {sum(loading_times)/len(loading_times):.3f} seconds" if loading_times else "N/A")
    print(f"⚡ Fastest Loading Time     : {min(loading_times):.3f} seconds" if loading_times else "N/A")
    print(f"🐌 Slowest Loading Time     : {max(loading_times):.3f} seconds" if loading_times else "N/A")
    print(f"{'='*80}\n")


if __name__ == "__main__":
    test_document_loading()
