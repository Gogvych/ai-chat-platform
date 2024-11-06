from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel
from datetime import datetime
from database import init_db
from user_model import Message  # Import your Message model
from database import SessionLocal
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
from config import Config
from openai import OpenAI



# Add lifespan event to initialize database
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)
templates = Jinja2Templates(directory="templates")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse(
        "index.html", 
        {"request": request}
    )


# Update the message handling endpoint
@app.post("/")
async def create_message(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        # Add debug logging
        body = await request.body()
        print("Raw request body:", body)
        
        data = await request.json()
        print("Parsed JSON data:", data)
        
        message = Message(
            is_ai=False,
            content=data.get("content"),
            timestamp=datetime.utcnow()
        )
        db.add(message)
        db.commit()
        db.refresh(message)
        
        # Get classification
        category = await classify_message(data.get("content"))
        category_response = None
        
        if category == "food":
            category_response = "Processing food request"
        elif category == "weather":
            category_response = "Processing weather request"
        else:
            category_response = "Processing other request"
        print("Category response:", category_response)

        response_data = {
            "id": message.id,
            "is_ai": message.is_ai,
            "content": message.content,
            "timestamp": message.timestamp
        }
        print("Sending response:", response_data)  # Debug log
        print("Category:", category)
        #return response_data, category_response
        return 12
    
    except Exception as e:
        print("Error:", str(e))  # Add error logging
        raise HTTPException(status_code=400, detail=str(e))
    

async def classify_message(content: str) -> str:
    """Classify if a message is about food, weather, or other topics."""
    client = OpenAI(api_key=Config.OPENAI_API_KEY)
    completion = client.chat.completions.create(
        model=Config.OPENAI_MODEL,
        messages=[
            {"role": "system", "content": "Classify if this message is about food or weather. Reply with only 'food' or 'weather' or 'other'."},
            {"role": "user", "content": content}
        ]
    )
    return completion.choices[0].message.content.strip().lower()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
