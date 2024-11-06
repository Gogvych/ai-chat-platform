from sqlalchemy import Column, Integer, Boolean, String, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class Message(Base):
    __tablename__ = 'messages'
    
    id = Column(Integer, primary_key=True, index=True)
    is_ai = Column(Boolean, default=False)
    content = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

class Document(Base):
    __tablename__ = 'documents'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    file_path = Column(String)
    is_processed = Column(Boolean, default=False)

class DocumentPage(Base):
    __tablename__ = 'document_pages'
    
    id = Column(Integer, primary_key=True, index=True)
    document_id = Column(Integer, ForeignKey('documents.id'))
    page_number = Column(Integer)
    content = Column(Text)  # Using Text for potentially large content
    is_processed = Column(Boolean, default=False)