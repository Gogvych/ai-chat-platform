from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from database.chroma_client import ChromaDatabase
from models import Document, DocumentPage
from sqlalchemy.orm import Session
from config import Config
import os

class DocumentProcessor:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.chroma_db = ChromaDatabase()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=Config.CHUNK_SIZE,
            chunk_overlap=Config.CHUNK_OVERLAP,
            length_function=len,
            is_separator_regex=False,
        )

    async def process_document(self, file_path: str, title: str):
        """Process PDF document and store in both SQL and ChromaDB"""
        try:
            # 1. Create document record in SQL
            document = Document(
                title=title,
                file_path=Config.PDF_STORAGE_PATH,
                is_processed=False
            )
            self.db_session.add(document)
            self.db_session.flush()

            # 2. Load and process PDF
            loader = PyPDFLoader(file_path)
            pages = loader.load()

            # 3. Store pages in SQL
            for page_number, page in enumerate(pages, 1):
                doc_page = DocumentPage(
                    document_id=document.id,
                    page_number=page_number,
                    content=str(page.page_content),
                    is_processed=True
                )
                self.db_session.add(doc_page)

            # 4. Store in ChromaDB for vector search
            self.chroma_db.add_pages("document_pages", pages)

            # 5. Create and store chunks for RAG
            chunks = self.text_splitter.split_documents(pages)
            self.chroma_db.add_chunks("document_chunks", chunks)

            # 6. Mark document as processed
            document.is_processed = True
            self.db_session.commit()

            return {
                "status": "success",
                "document_id": document.id,
                "pages_processed": len(pages),
                "chunks_processed": len(chunks)
            }

        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error processing document: {str(e)}")