---
title: AI Document Search Assistant
emoji: 📚
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
license: mit
---

# AI Document Search Assistant

A production-ready AI-powered document search and question-answering system built with **FastAPI**, **LangChain**, and **ChromaDB**. Upload PDF documents and ask questions - the AI will find answers using Retrieval Augmented Generation (RAG).

🚀 **[Try the Demo on Hugging Face Spaces](https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME)**

## 🚀 Features

- **PDF Document Upload**: Upload and process PDF documents
- **AI-Powered Search**: Ask questions in natural language
- **RAG Pipeline**: Retrieval Augmented Generation for accurate answers
- **Vector Database**: ChromaDB for efficient semantic search
- **Chat Interface**: Clean, responsive Bootstrap UI
- **Document Management**: View and delete uploaded documents
- **Chat History**: Persistent storage of conversations
- **Production-Ready**: Clean architecture with proper error handling
- **Free Local Models**: Uses Sentence Transformers (no API key needed)

## 🏗️ Architecture

### Backend (FastAPI)
```
app/
├── api/              # API endpoints
│   ├── documents.py  # Document upload/management
│   └── chat.py       # Query and chat endpoints
├── core/             # Core configuration
│   ├── config.py     # Settings management
│   ├── database.py   # MongoDB connection
│   ├── vector_store.py  # ChromaDB management
│   ├── embeddings.py    # OpenAI embeddings
│   └── llm.py          # LLM configuration
├── services/         # Business logic
│   ├── document_service.py  # Document processing
│   └── chat_service.py      # RAG pipeline
├── models/           # Pydantic models
│   ├── document_model.py
│   └── chat_model.py
├── utils/            # Utilities
│   ├── pdf_loader.py    # PDF processing
│   └── text_splitter.py # Text chunking
└── main.py          # FastAPI application
```

### Frontend (Bootstrap)
```
frontend/
├── index.html       # Home page
├── upload.html      # Document upload page
├── chat.html        # Chat interface
├── css/
│   └── style.css    # Custom styles
└── js/
    ├── upload.js    # Upload functionality
    └── chat.js      # Chat interface
```

## 📋 Prerequisites

- Python 3.10+
- MongoDB (for local development) or SQLite (for Hugging Face deployment)
- Optional: OpenAI API key (if using GPT models instead of local models)

## 🔧 Local Installation

### 1. Clone the Repository
```bash
git clone https://github.com/YOUR_USERNAME/document-search-assistant.git
cd document-search-assistant
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment Variables
```bash
cp .env.example .env
```

Edit `.env` and configure:
- `USE_LOCAL_MODELS=True` (for free local models)
- `OPENAI_API_KEY` (only if using OpenAI models)
- `MONGO_URI` (MongoDB connection string)

### 4. Run the Application
```bash
uvicorn app.main:app --reload
```

Visit http://localhost:8000

## 🤗 Deploy to Hugging Face Spaces

### Option 1: Direct Upload
1. Create a new Space on Hugging Face
2. Choose **Docker** as the SDK
3. Upload all files from this repository
4. Add secrets in Space Settings:
   - `OPENAI_API_KEY` (optional, only if using OpenAI models)
5. Your Space will automatically build and deploy!

### Option 2: GitHub Integration
1. Push this code to GitHub
2. Create a new Space on Hugging Face
3. Connect your GitHub repository
4. Configure secrets as needed
5. HF will auto-deploy on every push

## 🌐 Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `USE_LOCAL_MODELS` | Use free local models instead of OpenAI | `True` | No |
| `OPENAI_API_KEY` | OpenAI API key | - | Only if `USE_LOCAL_MODELS=False` |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `DATABASE_NAME` | Database name | `document_search_db` | No |
| `CHUNK_SIZE` | Text chunk size for embeddings | `1000` | No |
| `CHUNK_OVERLAP` | Chunk overlap size | `200` | No |

## 🎯 Usage

### Upload Documents
1. Navigate to the Upload page
2. Select PDF files
3. Click Upload
4. Documents are processed and indexed automatically

### Ask Questions
1. Go to Chat page
2. Type your question
3. AI retrieves relevant context and provides answers
4. View sources used for the answer

## 🧪 API Endpoints

### Documents
- `POST /api/documents/upload` - Upload PDF document
- `GET /api/documents/` - List all documents
- `DELETE /api/documents/{id}` - Delete document

### Chat
- `POST /api/chat/query` - Ask a question
- `GET /api/chat/history` - Get chat history
- `DELETE /api/chat/history/{id}` - Delete specific chat
- `DELETE /api/chat/history` - Clear all history

### Health
- `GET /health` - Health check

## 🛠️ Technology Stack

- **Backend**: FastAPI, Python 3.10+
- **Vector Database**: ChromaDB
- **Database**: MongoDB / SQLite
- **LLM Framework**: LangChain
- **Models**: 
  - Local: Sentence Transformers (all-MiniLM-L6-v2)
  - Option: OpenAI (GPT-4o-mini, text-embedding-3-small)
- **Frontend**: HTML, CSS, Bootstrap 5, JavaScript
- **Deployment**: Docker, Hugging Face Spaces

## 📝 License

MIT License - see LICENSE file for details

## 🤝 Contributing

Contributions are welcome! Please open an issue or submit a pull request.

## 📧 Contact

For questions or support, please open an issue on GitHub.

---

Built with ❤️ using FastAPI, LangChain, and ChromaDB
