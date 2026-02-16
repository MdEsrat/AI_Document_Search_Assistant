"""
Test script to upload PDF with local models (try Resume PDF)
"""
import requests
import os

# Get PDF files
upload_dir = "data/uploads"
pdf_files = [f for f in os.listdir(upload_dir) if f.endswith('.pdf') and f != '.gitkeep']

print(f"\n📂 Found {len(pdf_files)} PDF files:")
for i, pdf in enumerate(pdf_files, 1):
    size = os.path.getsize(os.path.join(upload_dir, pdf)) / 1024
    print(f"   {i}. {pdf} ({size:.1f} KB)")

# Try the Resume PDF (second file)
if len(pdf_files) < 2:
    print("\n❌ Need at least 2 PDF files to try alternate")
    exit(1)

pdf_file = os.path.join(upload_dir, pdf_files[1])
print(f"\n📄 Testing upload with: {pdf_files[1]}")
print(f"   File size: {os.path.getsize(pdf_file) / 1024:.1f} KB")
print("\n⏳ Processing with FREE local models (no OpenAI credits needed)...\n")

# Upload file
with open(pdf_file, 'rb') as f:
    files = {'file': (pdf_files[1], f, 'application/pdf')}
    try:
        response = requests.post('http://localhost:8000/api/documents/upload', files=files, timeout=120)
        data = response.json()
        
        if data.get('success'):
            print("✅ SUCCESS! File uploaded using FREE local models!")
            print(f"   Message: {data['message']}")
            print(f"   Chunks created: {data['chunks_created']}")
            print(f"\n🎉 No OpenAI credits needed - everything runs locally!")
        else:
            print(f"❌ Upload failed: {data.get('message')}")
    except Exception as e:
        print(f"❌ Error: {e}")
