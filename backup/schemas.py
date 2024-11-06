from pydantic import BaseModel
from datetime import datetime

class MessageRequest(BaseModel):
    content: str

    class Config:
        json_schema_extra = {
            "example": {
                "content": "What's the weather like in New York?"
            }
        }

class MessageResponse(BaseModel):
    user_message: dict
    ai_message: dict
    category: str

    class Config:
        json_schema_extra = {
            "example": {
                "user_message": {
                    "content": "What's the weather like in New York?",
                    "timestamp": "2024-11-06T00:52:27"
                },
                "ai_message": {
                    "content": "Currently in New York, it's 16.7°C with partly cloudy conditions...",
                    "timestamp": "2024-11-06T00:52:28"
                },
                "category": "weather"
            }
        }

class DocumentResponse(BaseModel):
    status: str
    document_id: int
    pages_processed: int
    chunks_processed: int

    class Config:
        json_schema_extra = {
            "example": {
                "status": "success",
                "document_id": 1,
                "pages_processed": 83,
                "chunks_processed": 219
            }
        }