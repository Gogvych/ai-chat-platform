# AI Chat Platform

A conversational AI platform built with FastAPI that processes messages and documents using various AI models. The system uses RAG (Retrieval-Augmented Generation) for food-related queries and integrates with a weather API for weather-related questions.

## Features

- **Message Processing**
  - Classification of messages (food/weather)
  - RAG-based responses for food queries using llama-3.1-70b-versatile
  - Weather information for New York using OpenAI GPT-4o

- **Document Management**
  - PDF processing and chunking
  - Vector embeddings using OpenAI's text-embedding-3-small
  - Storage in ChromaDB for efficient retrieval

- **API Endpoints**
  - `/documents/` - Process and store PDF documents
  - `/messages/` - Handle user queries and generate AI responses
  - `/` - Root endpoint with API information

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLAlchemy + ChromaDB
- **AI Models**:
  - OpenAI GPT-4o for weather responses
  - llama-3.1-70b-versatile (via Groq) for food queries
  - OpenAI text-embedding-3-small for document embeddings
- **Document Processing**: LangChain

## Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/ai-chat-platform.git
   cd ai-chat-platform
   ```

2. **Create and activate virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the project root with:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   WEATHER_API_KEY=your_weather_api_key
   WEATHER_API_URL=http://api.weatherapi.com/v1/current.json
   WEATHER_LOCATION=New York
   OPENAI_CHAT_MODEL=gpt-4o
   OPENAI_EMBEDDING_MODEL=text-embedding-3-small
   GROQ_CHAT_MODEL=llama-3.1-70b-versatile
   CHROMA_DB_PATH=./chroma_db
   SQLALCHEMY_DATABASE_URL=sqlite:///./sql_app.db
   PDF_URL=your_pdf_url
   ```

5. **Run the application**
   ```bash
   uvicorn main:app --reload
   ```

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage

1. **Process Document**
   ```bash
   curl -X POST "http://localhost:8000/documents/"
   ```

2. **Send Message**
   ```bash
   curl -X POST "http://localhost:8000/messages/" \
   -H "Content-Type: application/json" \
   -d '{"content": "What does the document say about Hawaiian food?"}'
   ```


## Acknowledgments

- OpenAI for GPT-4o and embeddings
- Groq for llama-3.1-70b-versatile access
- WeatherAPI for weather data
- FastAPI team for the amazing framework