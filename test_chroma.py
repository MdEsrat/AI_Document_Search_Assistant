"""
Test adding documents to ChromaDB with local embeddings
"""
from app.core.local_embeddings import get_local_embeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
import shutil
import os

# Clean test directory
test_dir = "data/test_chroma"
if os.path.exists(test_dir):
    shutil.rmtree(test_dir)
os.makedirs(test_dir)

print("🔄 Loading local embeddings...")
embeddings = get_local_embeddings()
print("✅ Embeddings loaded")

print("\n🔄 Creating ChromaDB vector store...")
vector_store = Chroma(
    collection_name="test_collection",
    embedding_function=embeddings,
    persist_directory=test_dir
)
print("✅ Vector store created")

print("\n🔄 Creating test documents...")
test_docs = [
    Document(page_content="This is the first test document about AI.", metadata={"source": "test1"}),
    Document(page_content="This is the second document about machine learning.", metadata={"source": "test2"}),
    Document(page_content="This is the third document about deep learning.", metadata={"source": "test3"})
]
print(f"✅ Created {len(test_docs)} documents")

print("\n🔄 Adding documents to vector store...")
try:
    vector_store.add_documents(test_docs)
    print("✅ Documents added successfully!")
    
    # Test retrieval
    print("\n🔄 Testing retrieval...")
    results = vector_store.similarity_search("What is AI?", k=2)
    print(f"✅ Retrieved {len(results)} documents")
    for i, doc in enumerate(results, 1):
        print(f"\n   Document {i}:")
        print(f"   Content: {doc.page_content[:80]}...")
        print(f"   Source: {doc.metadata.get('source')}")
    
    print("\n✅ SUCCESS! Local embeddings work with ChromaDB!")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Cleanup
shutil.rmtree(test_dir)
