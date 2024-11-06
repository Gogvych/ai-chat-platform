from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from document_processor import DocumentProcessor
from message_processor import MessageProcessor
from db import get_db, engine
from models import Base
from pydantic import BaseModel
from config import Config
import os

# Initialize database tables
Base.metadata.create_all(bind=engine)

# Create FastAPI app with metadata for documentation
app = FastAPI(
    title="AI Chat Platform",
    description="""
    A conversational AI platform that processes messages and documents using various AI models.
    
    Features:
    * Message processing with classification (food/weather)
    * Food queries using RAG with Llama 3.1 70b
    * Weather queries using OpenAI GPT-4o
    * Document processing with vector storage
    """,
    version="1.0.0",
    contact={
        "name": "AI Chat Platform Team",
        "url": "https://github.com/yourusername/ai-chat-platform",
    }
)

# Pydantic models for request/response
class MessageRequest(BaseModel):
    content: str

@app.post("/documents/", 
    tags=["Documents"],
    summary="Process a PDF document",
    description="""
    Processes a PDF document by:
    1. Splitting it into pages
    2. Chunking the content
    3. Embedding chunks using OpenAI's text-embedding-3-small
    4. Storing in ChromaDB for vector search
    5. Storing metadata in SQL database
    """)

async def process_document(db: Session = Depends(get_db)):
    """Process the configured PDF document"""
    try:
        # Get file path from config
        file_path = Config.PDF_STORAGE_PATH

        if not file_path:
            raise HTTPException(status_code=400, detail="PDF_URL not configured in .env")
        
        # Extract filename from the path
        file_name = os.path.basename(file_path)
        if not file_name:
            raise HTTPException(status_code=400, detail="Invalid PDF URL format")
        
        # Remove extension for title
        title = os.path.splitext(file_name)[0]
        
        # Add debug logging
        print(f"Processing document: {file_path}")
        print(f"Title: {title}")

        processor = DocumentProcessor(db)
        result = await processor.process_document(file_path, title)
        print("Document has been processed") #TODO: Remove this
        return result
    except Exception as e:
        print(f"Error processing document: {str(e)}")  # Add debug logging
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/messages/",
    tags=["Messages"],
    summary="Process a user message",
    description="""
    Processes a user message by:
    1. Classifying it as food or weather related
    2. For food queries: Uses RAG with Llama 3.1 70b to answer based on processed documents
    3. For weather queries: Fetches current NY weather and formats response using GPT-4o
    4. Stores both user message and AI response in database
    """)

async def create_message(
    message: MessageRequest,
    db: Session = Depends(get_db)
):
    """Process a user message and generate response"""
    try:
        processor = MessageProcessor(db)
        result = await processor.process_message(message.content)
        print("Your message has been processed") #TODO: Remove this
        return result
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/", 
    tags=["Root"],
    summary="Root endpoint",
    description="Returns basic information about the API")
async def root():
    """Root endpoint returning API information"""
    return {
        "name": "AI Chat Platform API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": [
            "/documents/",
            "/messages/"
        ]
    }

    
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
