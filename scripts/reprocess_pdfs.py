"""
Script to reprocess existing PDF files in uploads folder
"""
import asyncio
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.pdf_loader import PDFLoaderUtil
from app.utils.text_splitter import text_splitter
from app.core.vector_store import vector_store_manager
from app.core.config import settings

async def reprocess_pdfs():
    """Reprocess all PDFs in uploads folder"""
    upload_dir = settings.UPLOAD_DIR
    
    print(f"Scanning {upload_dir} for PDF files...")
    
    pdf_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf')]
    
    if not pdf_files:
        print("No PDF files found to process.")
        return
    
    print(f"Found {len(pdf_files)} PDF file(s):")
    for pdf in pdf_files:
        print(f"  - {pdf}")
    
    pdf_loader = PDFLoaderUtil()
    total_chunks = 0
    
    for pdf_file in pdf_files:
        file_path = os.path.join(upload_dir, pdf_file)
        print(f"\nProcessing: {pdf_file}")
        
        try:
            # Load PDF
            documents = pdf_loader.load_pdf(file_path)
            print(f"  ✓ Loaded {len(documents)} page(s)")
            
            # Split into chunks
            chunks = text_splitter.split_documents(documents)
            print(f"  ✓ Created {len(chunks)} chunk(s)")
            
            # Add to vector store
            vector_store_manager.add_documents(chunks)
            print(f"  ✓ Added to vector store")
            
            total_chunks += len(chunks)
            
        except Exception as e:
            print(f"  ✗ Error: {e}")
    
    print(f"\n{'='*50}")
    print(f"Processing complete!")
    print(f"Total chunks indexed: {total_chunks}")
    print(f"{'='*50}")
    print("\nYou can now ask questions about your documents!")

if __name__ == "__main__":
    asyncio.run(reprocess_pdfs())
