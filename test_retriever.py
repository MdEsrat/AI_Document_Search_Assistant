"""
Direct test of retriever
"""
from app.core.vector_store import vector_store_manager

print("\n🔍 Testing retriever directly...\n")

try:
    # Get vector store and retriever
    vector_store = vector_store_manager.get_vector_store()
    retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 4})
    
    # Try to retrieve documents
    question = "What is the person's name?"
    print(f"Query: {question}\n")
    
    # Use invoke() for LangChain v0.2+
    docs = retriever.invoke(question)
    
    print(f"Retrieved {len(docs)} documents:\n")
    for i, doc in enumerate(docs, 1):
        print(f"Document {i}:")
        print(f"  Content: {doc.page_content[:150]}...")
        print(f"  Metadata: {doc.metadata}\n")
    
    if len(docs) > 0:
        print("✅ Retriever is working!")
    else:
        print("⚠️  Retriever returned no documents")
        
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()
