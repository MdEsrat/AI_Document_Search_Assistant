# AI Document Search Assistant

A production-ready AI-powered document search and question-answering system built with **FastAPI**, **MongoDB**, **LangChain**, and **OpenAI**. Upload PDF documents and ask questions - the AI will find answers using Retrieval Augmented Generation (RAG).

## 🚀 Features

- **PDF Document Upload**: Upload and process PDF documents
- **AI-Powered Search**: Ask questions in natural language
- **RAG Pipeline**: Retrieval Augmented Generation for accurate answers
- **Vector Database**: ChromaDB for efficient semantic search
- **Chat Interface**: Clean, responsive Bootstrap UI
- **Document Management**: View and delete uploaded documents
- **Chat History**: Persistent storage of conversations
- **Production-Ready**: Clean architecture with proper error handling

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
    ├── upload.js    # Upload logic
    └── chat.js      # Chat logic
```

## 📋 Prerequisites

- Python 3.9+
- MongoDB (local or Atlas)
- OpenAI API Key

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone <repository-url>
cd document_search_assistant
```

### 2. Create Virtual Environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
```bash
# Copy example environment file
copy .env.example .env

# Edit .env and add your credentials
# REQUIRED: Add your OpenAI API key
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. Start MongoDB
```bash
# If using local MongoDB
mongod

# Or use MongoDB Atlas (update MONGO_URI in .env)
```

### 6. Run the Application
```bash
# Development mode
python app/main.py

# Or with uvicorn
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 7. Access the Application
Open your browser and navigate to:
```
http://localhost:8000
```

## 🎯 Usage

### 1. Upload Documents
- Navigate to the **Upload** page
- Select a PDF file
- Click "Upload Document"
- Wait for processing to complete

### 2. Ask Questions
- Navigate to the **Chat** page
- Type your question in the input field
- Press Enter or click "Send"
- View the AI-generated answer

### 3. View Documents
- Check the documents list on the Upload page
- See metadata like upload date, chunks, and file size
- Delete documents if needed

## 🔌 API Endpoints

### Documents
- `POST /api/documents/upload` - Upload PDF document
- `GET /api/documents/` - Get all documents
- `DELETE /api/documents/{document_id}` - Delete document

### Chat
- `POST /api/chat/query` - Query documents
- `GET /api/chat/history` - Get chat history

### Health Check
- `GET /health` - Health check endpoint

## 🧪 API Examples

### Upload Document
```bash
curl -X POST "http://localhost:8000/api/documents/upload" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@document.pdf"
```

### Query Documents
```bash
curl -X POST "http://localhost:8000/api/chat/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

## 🏗️ RAG Pipeline

The system uses a complete RAG pipeline:

1. **Document Loading**: PyPDF for PDF text extraction
2. **Text Splitting**: Recursive character splitter (1000 chars, 200 overlap)
3. **Embeddings**: OpenAI `text-embedding-3-small`
4. **Vector Store**: ChromaDB with persistence
5. **Retrieval**: Similarity search (top 4 chunks)
6. **Generation**: OpenAI `gpt-4o-mini`
7. **Chain**: LangChain RetrievalQA

## 📦 Technology Stack

### Backend
- **FastAPI**: Modern, fast web framework
- **MongoDB**: Document database for metadata
- **Motor**: Async MongoDB driver
- **LangChain**: LLM orchestration framework
- **OpenAI**: Embeddings and LLM
- **ChromaDB**: Vector database
- **PyPDF**: PDF processing
- **Pydantic**: Data validation

### Frontend
- **Bootstrap 5**: Responsive UI framework
- **Vanilla JavaScript**: No framework overhead
- **Fetch API**: HTTP requests

## 🔒 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `OPENAI_API_KEY` | OpenAI API key | **Required** |
| `MONGO_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `DATABASE_NAME` | MongoDB database name | `document_search_db` |
| `UPLOAD_DIR` | Document upload directory | `data/uploads` |
| `CHROMA_DIR` | ChromaDB persistence directory | `data/chroma` |
| `CHUNK_SIZE` | Text chunk size | `1000` |
| `CHUNK_OVERLAP` | Text chunk overlap | `200` |
| `EMBEDDING_MODEL` | OpenAI embedding model | `text-embedding-3-small` |
| `LLM_MODEL` | OpenAI LLM model | `gpt-4o-mini` |
| `TEMPERATURE` | LLM temperature | `0.0` |

## 📁 Data Storage

### File System
- **Uploads**: `data/uploads/` - PDF files
- **Vector DB**: `data/chroma/` - ChromaDB persistence

### MongoDB Collections
- **documents**: Document metadata
- **chat_history**: Conversation history

## 🚦 Error Handling

The application includes comprehensive error handling:
- File validation (PDF only)
- Database connection errors
- API request errors
- Document processing errors
- User-friendly error messages

## 🎨 UI Features

- **Responsive Design**: Works on all devices
- **Loading Indicators**: Visual feedback during processing
- **Chat Bubbles**: ChatGPT-style interface
- **Document List**: View all uploaded documents
- **Progress Bars**: Upload progress tracking
- **Alert Messages**: Success/error notifications

## 🔧 Development

### Project Structure
- Clean architecture with separation of concerns
- Modular design for maintainability
- Async/await for performance
- Type hints for code clarity
- Logging for debugging

### Best Practices
- Pydantic models for validation
- Environment-based configuration
- Connection pooling
- Error handling at all levels
- RESTful API design

## 📝 Notes

- Only PDF files are supported
- Documents are processed asynchronously
- Chat history is stored in MongoDB
- Vector embeddings are persisted in ChromaDB
- The system answers based only on uploaded documents

## 🐛 Troubleshooting

### MongoDB Connection Error
```bash
# Check if MongoDB is running
mongo --eval "db.version()"

# Or use MongoDB Compass to verify connection
```

### OpenAI API Error
```bash
# Verify your API key is set correctly in .env
# Check your OpenAI account has credits
```

### Port Already in Use
```bash
# Change port in main.py or use:
uvicorn app.main:app --port 8001
```

## 🚀 Production Deployment

### Environment Setup
1. Set production environment variables
2. Use production MongoDB instance
3. Configure proper CORS origins
4. Set up HTTPS
5. Use gunicorn or similar WSGI server

### Recommended Stack
- **Server**: Linux VPS or cloud (AWS, GCP, Azure)
- **Database**: MongoDB Atlas
- **Vector DB**: Persistent volume for ChromaDB
- **Web Server**: Nginx as reverse proxy
- **Process Manager**: Supervisor or systemd

## 📄 License

This project is open source and available under the MIT License.

## 👥 Author

Built with ❤️ using FastAPI, MongoDB, LangChain, and OpenAI.

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- LangChain for RAG orchestration
- OpenAI for embeddings and LLM
- Bootstrap for the UI framework

---

**Ready to search your documents? Start uploading!** 🚀
