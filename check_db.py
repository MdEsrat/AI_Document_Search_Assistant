"""
Check ChromaDB contents
"""
from app.core.vector_store import vector_store_manager

print("\n🔍 Checking ChromaDB contents...\n")

try:
    vector_store = vector_store_manager.get_vector_store()
    
    # Get collection
    collection = vector_store._collection
    print(f"Collection name: {collection.name}")
    print(f"Total documents: {collection.count()}")
    
    if collection.count() > 0:
        # Try to get some documents
        results = collection.get(limit=3)
        print(f"\n📄 Sample documents:")
        if results and 'documents' in results:
            for i, doc in enumerate(results['documents'][:3], 1):
                print(f"\n{i}. {doc[:100]}...")
        print("\n✅ Documents are in ChromaDB!")
    else:
        print("\n⚠️  ChromaDB is empty")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
