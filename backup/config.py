import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # OpenAI
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    OPENAI_MODEL = os.getenv('OPENAI_CHAT_MODEL')
    OPENAI_EMBEDDING_MODEL = os.getenv('OPENAI_EMBEDDING_MODEL')
    
    #Groq
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    GROQ_MODEL = os.getenv('GROQ_CHAT_MODEL')

    # Database
    CHROMADB_PATH = os.getenv('CHROMA_DB_PATH')
    SQLALCHEMY_DATABASE_URL = os.getenv('SQLALCHEMY_DATABASE_URL')
    
    # PDF Processing
    CHUNK_SIZE = 1000
    CHUNK_OVERLAP = 200
    
    # API Configuration
    #API_HOST = "localhost"
    #API_PORT = 8000
    
    # Other constants
    PDF_STORAGE_PATH = os.getenv('PDF_URL')

    # Weather API
    WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
    WEATHER_API_URL = os.getenv('WEATHER_API_URL')
    WEATHER_LOCATION = os.getenv('WEATHER_LOCATION')
    