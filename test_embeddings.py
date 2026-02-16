"""
Test local embeddings directly
"""
from app.core.local_embeddings import get_local_embeddings

print("🔄 Loading local embeddings model...")
try:
    embeddings = get_local_embeddings()
    print("✅ Model loaded successfully")
    
    # Test embedding a simple text
    print("\n📝 Testing embeddings with sample text...")
    test_text = "This is a test document about artificial intelligence."
    result = embeddings.embed_query(test_text)
    
    print(f"✅ Embedding created!")
    print(f"   Dimension: {len(result)}")
    print(f"   First 5 values: {result[:5]}")
    
    # Test batch embeddings
    print("\n📝 Testing batch embeddings...")
    test_docs = ["Document 1", "Document 2", "Document 3"]
    batch_results = embeddings.embed_documents(test_docs)
    print(f"✅ Batch embeddings created!")
    print(f"   Number: {len(batch_results)}")
    print(f"   Each dimension: {len(batch_results[0])}")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
