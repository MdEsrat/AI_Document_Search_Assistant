"""
Test chat with uploaded documents (using FREE local models)
"""
import requests

print("\n💬 Testing chat with uploaded document...")
print("   Using FREE local models (no OpenAI credits needed)\n")

# Test query
question = "What is the person's name and email in the resume?"

try:
    response = requests.post(
        'http://localhost:8000/api/chat/query',
        json={'question': question},
        timeout=30
    )
    data = response.json()
    
    print(f"Question: {question}\n")
    print(f"Answer:\n{data['answer']}\n")
    
    if data.get('sources'):
        print(f"Sources: {', '.join(data['sources'])}")
    
    print("\n✅ Chat is working with FREE local models!")
    print("   No OpenAI API credits needed at all!")
    
except Exception as e:
    print(f"❌ Error: {e}")
