"""
Quick Document Indexer

This script indexes all PDF files in the data/ folder.
Run this after adding new PDFs to make them searchable.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.indexing import index_directory
from src.config.settings import PDF_DIRECTORY

def main():
    print("=" * 70)
    print("📚 ENTERPRISE RAG - DOCUMENT INDEXER")
    print("=" * 70)
    print()
    
    # Check if PDFs exist
    pdf_files = list(PDF_DIRECTORY.glob("*.pdf"))
    
    if not pdf_files:
        print("❌ No PDF files found in the data/ folder!")
        print()
        print("📁 Please add PDF files to:")
        print(f"   {PDF_DIRECTORY.absolute()}")
        print()
        print("Then run this script again.")
        return
    
    print(f"📂 Found {len(pdf_files)} PDF file(s) in data/ folder:")
    for pdf in pdf_files:
        print(f"   • {pdf.name}")
    print()
    
    # Confirm before indexing
    response = input("🔄 Do you want to index these documents? (y/n): ")
    if response.lower() not in ['y', 'yes']:
        print("❌ Indexing cancelled.")
        return
    
    print()
    print("🔄 Indexing documents... This may take a moment...")
    print("   (Loading embedding model, chunking text, creating vectors)")
    print()
    
    try:
        result = index_directory()
        
        print("=" * 70)
        print("✅ INDEXING COMPLETED SUCCESSFULLY!")
        print("=" * 70)
        print()
        print(f"📊 Results:")
        print(f"   • PDF files indexed: {result['pdf_count']}")
        print(f"   • Total documents: {result['document_count']}")
        print(f"   • Total chunks stored: {result['chunk_count']}")
        print()
        print("🎉 Your documents are now searchable in the RAG system!")
        print()
        print("💡 Next Steps:")
        print("   1. Start the server: .\\START_SERVER.ps1")
        print("   2. Open web interface: http://127.0.0.1:8000/static/index.html")
        print("   3. Ask questions about your documents!")
        print()
        
    except Exception as e:
        print()
        print("=" * 70)
        print("❌ INDEXING FAILED!")
        print("=" * 70)
        print()
        print(f"Error: {str(e)}")
        print()
        print("💡 Troubleshooting:")
        print("   • Check if PDFs are valid and not corrupted")
        print("   • Ensure PDFs contain extractable text (not just images)")
        print("   • Check logs at: logs/application.log")
        print()

if __name__ == "__main__":
    main()
