"""
Chat service with RAG pipeline
"""
from typing import Dict, List
from datetime import datetime
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from app.core.database import mongodb
from app.core.vector_store import vector_store_manager
from app.core.config import settings
from app.models.chat_model import QueryRequest, QueryResponse, ChatHistory
import logging

logger = logging.getLogger(__name__)


class ChatService:
    """Service for handling chat operations with RAG"""
    
    def __init__(self):
        # Use local LLM (FREE) or OpenAI
        if settings.USE_LOCAL_MODELS or not settings.OPENAI_API_KEY:
            from app.core.local_llm import LocalLLM
            self.llm = LocalLLM()
            self.use_local = True
            logger.info("Using FREE local LLM (no API key needed)")
        else:
            from app.core.llm import get_llm
            self.llm = get_llm()
            self.use_local = False
            logger.info("Using OpenAI LLM")
        
        # Don't initialize retriever here - do it fresh each query
        if not self.use_local:
            self.qa_chain = self._create_qa_chain()
    
    def _get_retriever(self):
        """Get a fresh retriever (to ensure latest documents are included)"""
        vector_store = vector_store_manager.get_vector_store()
        return vector_store.as_retriever(
            search_type="similarity",
            search_kwargs={"k": 4}
        )
    
    async def get_uploaded_documents_info(self) -> str:
        """Get information about uploaded documents from MongoDB"""
        try:
            collection = mongodb.get_collection("documents")
            if collection is None:
                return "No documents database available."
            
            docs = []
            async for doc in collection.find():
                docs.append({
                    "filename": doc.get("filename", "Unknown"),
                    "upload_date": doc.get("upload_date"),
                    "num_chunks": doc.get("num_chunks", 0),
                    "file_size": doc.get("file_size", 0)
                })
            
            if not docs:
                return "No documents have been uploaded yet."
            
            info = f"I have access to {len(docs)} document(s):\n\n"
            for i, doc in enumerate(docs, 1):
                size_mb = doc['file_size'] / (1024 * 1024)
                info += f"{i}. **{doc['filename']}**\n"
                info += f"   - Uploaded: {doc['upload_date']}\n"
                info += f"   - Size: {size_mb:.2f} MB\n"
                info += f"   - Chunks: {doc['num_chunks']}\n\n"
            
            return info
        except Exception as e:
            logger.error(f"Error getting document info: {e}")
            return "Error retrieving document information."
    
    def _format_docs(self, docs):
        """Format documents for context"""
        return "\n\n".join(doc.page_content for doc in docs)
    
    def _create_qa_chain(self):
        """Create RAG chain using LCEL"""
        
        # Custom prompt template
        template = """You are an AI assistant that answers questions based on uploaded PDF documents.

You can answer:
1. Questions about the CONTENT of uploaded documents (using the context below)
2. Questions about WHICH documents are uploaded (list files, show details)
3. General questions about the documents

If someone asks "what files do you have", "what documents are uploaded", "list files", or similar:
- Respond that you can list the documents and they should ask you to show them.

For content questions, use the context below:

Context:
{context}

Question: {question}

Answer: """
        
        prompt = PromptTemplate(
            template=template,
            input_variables=["context", "question"]
        )
        
        # Create RAG chain using LCEL
        qa_chain = (
            {"context": self.retriever | self._format_docs, "question": RunnablePassthrough()}
            | prompt
            | self.llm
            | StrOutputParser()
        )
        
        return qa_chain
    
    async def process_query(self, query: QueryRequest) -> QueryResponse:
        """
        Process user query using RAG pipeline
        
        Args:
            query: QueryRequest object
            
        Returns:
            QueryResponse with answer and sources
        """
        try:
            # Check if user is asking about uploaded files
            question_lower = query.question.lower()
            file_questions = [
                "what files", "which files", "what documents", "which documents",
                "list files", "list documents", "show files", "show documents",
                "uploaded files", "uploaded documents", "what do you have",
                "what pdfs", "file details", "document details"
            ]
            
            if any(keyword in question_lower for keyword in file_questions):
                # Return document information from MongoDB
                docs_info = await self.get_uploaded_documents_info()
                return QueryResponse(
                    answer=docs_info,
                    sources=["MongoDB Database"],
                    timestamp=datetime.utcnow()
                )
            
            # Get relevant documents (run synchronously in async context)
            import asyncio
            loop = asyncio.get_event_loop()
            
            # Get fresh retriever to ensure latest documents
            retriever = self._get_retriever()
            # Use invoke() for LangChain v0.2+
            docs = await loop.run_in_executor(
                None, 
                retriever.invoke, 
                query.question
            )
            
            # Generate answer
            if self.use_local:
                # Use simple extractive method (FREE, no API)
                context = "\n\n".join([doc.page_content for doc in docs])
                answer = self.llm.generate_answer(query.question, context)
            else:
                # Use OpenAI with LCEL chain
                answer = await loop.run_in_executor(
                    None,
                    self.qa_chain.invoke,
                    query.question
                )
            
            # Extract source information
            sources = []
            for doc in docs:
                if hasattr(doc, 'metadata') and 'source' in doc.metadata:
                    sources.append(doc.metadata['source'])
            
            # Remove duplicates
            sources = list(set(sources))
            
            # Store chat history in MongoDB
            chat_history = ChatHistory(
                question=query.question,
                answer=answer,
                sources=sources if sources else None
            )
            
            collection = mongodb.get_collection("chat_history")
            if collection is not None:
                await collection.insert_one(chat_history.dict())
            else:
                logger.warning("MongoDB not available. Chat history not stored.")
            
            logger.info(f"Query processed: {query.question[:50]}...")
            
            return QueryResponse(
                answer=answer,
                sources=sources if sources else None,
                timestamp=datetime.utcnow()
            )
            
        except Exception as e:
            logger.error(f"Error processing query: {e}", exc_info=True)
            # Return a helpful error message instead of raising
            return QueryResponse(
                answer="I'm sorry, but I don't have any documents to search through yet. Please upload a PDF document first from the Upload page.",
                sources=None,
                timestamp=datetime.utcnow()
            )
    
    async def get_chat_history(self, limit: int = 50) -> List[Dict]:
        """
        Get chat history from MongoDB
        
        Args:
            limit: Maximum number of records to return
            
        Returns:
            List of chat history records
        """
        try:
            collection = mongodb.get_collection("chat_history")
            if collection is None:
                logger.warning("MongoDB not available. Returning empty chat history.")
                return []
            history = []
            async for record in collection.find().sort("timestamp", -1).limit(limit):
                record["id"] = str(record["_id"])
                del record["_id"]
                history.append(record)
            return history
        except Exception as e:
            logger.error(f"Error retrieving chat history: {e}")
            return []


# Global chat service instance
chat_service = ChatService()
