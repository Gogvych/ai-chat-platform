from openai import OpenAI
from groq import Groq
from database.chroma_client import ChromaDatabase
from models import Message
from sqlalchemy.orm import Session
from datetime import datetime
from config import Config
from weatherapi import get_current_weather

class MessageProcessor:
    def __init__(self, db_session: Session):
        self.db_session = db_session
        self.chroma_db = ChromaDatabase()
        self.openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
        self.groq_client = Groq(api_key=Config.GROQ_API_KEY)

    async def classify_message(self, content: str) -> str:
        """Classify message as food or weather related"""
        completion = self.openai_client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Classify if this message is about food or weather. Reply with only 'food' or 'weather' or 'other'."},
                {"role": "user", "content": content}
            ],
            temperature=0.0
        )
        print(f"MSG classification completed: {completion.choices[0].message.content.strip().lower()}")
        return completion.choices[0].message.content.strip().lower()

    async def process_food_query(self, query: str) -> str:
        """Process food-related query using RAG with Llama"""
        try:
            # Get relevant chunks from ChromaDB
            collection = self.chroma_db.get_collection("document_chunks")
            results = collection.query(
                query_texts=[query],
                n_results=3  # Get top 3 most relevant chunks
        )
        
            # Detailed logging of retrieved chunks
            print("\n=== Retrieved Chunks from PDF ===")
            for i, chunk in enumerate(results['documents'][0]):
                print(f"\nChunk {i + 1}:")
                print(f"Content: {chunk[:200]}...")  # Print first 200 chars of each chunk
                print(f"Metadata: {results['metadatas'][0][i]}")  # Print metadata (page numbers etc.)
                print("-" * 50)
            
            # Construct context from relevant chunks
            context = "\n".join(results['documents'][0])
            
            # Log the complete prompt being sent to Groq
            print("\n=== Prompt to Groq ===")
            prompt = f"""Based on the following excerpts from the document:

    Context: {context}

    Question: {query}

    Please answer the question using ONLY the information from the provided context. 
    If the context doesn't contain relevant information, please say "I don't find relevant information about this in the document."
    """
            print(prompt)
            print("=" * 50)
            
            # Generate response using Groq
            messages = [
                {
                    "role": "system",
                    "content": "You are a helpful assistant that answers questions STRICTLY based on the provided context. Do not make up information or use external knowledge."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
            
            completion = self.groq_client.chat.completions.create(
                model=Config.GROQ_MODEL,
                messages=messages,
                temperature=0.3,  # Lower temperature for more focused responses
                max_tokens=500
            )
            
            response = completion.choices[0].message.content
            print("\n=== Groq Response ===")
            print(response)
            
            return response
        
        except Exception as e:
            print(f"Error in process_food_query: {str(e)}")
            return "I encountered an error while processing your food-related query. Please try again."

    async def process_weather_query(self, query: str) -> str:
        """Process weather-related query"""
        try:
            weather_data = get_current_weather()
        
            if weather_data:
                # Format weather data into a clear prompt
                weather_info = {
                    'temperature': weather_data['current']['temp_c'],
                    'condition': weather_data['current']['condition']['text'],
                    'humidity': weather_data['current']['humidity'],
                    'wind_speed': weather_data['current']['wind_kph']
                }
            
                prompt = f"""Current weather in New York:
                Temperature: {weather_info['temperature']}°C
                Condition: {weather_info['condition']}
                Humidity: {weather_info['humidity']}%
                Wind Speed: {weather_info['wind_speed']} km/h"""
                
                print("Weather data formatted:", prompt)  # Debug print
                
                completion = self.openai_client.chat.completions.create(
                    model=Config.OPENAI_MODEL,  # Make sure this matches your .env
                    messages=[
                        {"role": "system", "content": "You are a helpful weather assistant. Convert the weather data into a natural, friendly response."},
                        {"role": "user", "content": f"Based on this data: {prompt}, provide a natural language summary of the weather."}
                    ],
                    temperature=0.7
                )
                
                response = completion.choices[0].message.content
                print("Generated response:", response)  # Debug print
                return response
        
            return "Sorry, I couldn't fetch the weather data at the moment."
        except Exception as e:
            print(f"Weather processing error: {str(e)}")
            return f"I encountered an error while processing the weather data: {str(e)}"

    async def process_message(self, content: str):
        """Process incoming message and generate response"""
        try:
            # Store user message
            user_message = Message(
                is_ai=False,
                content=content,
                timestamp=datetime.utcnow()
            )
            self.db_session.add(user_message)
            
            # Classify message
            category = await self.classify_message(content)
            
            # Generate response based on classification
            if category == "food":
                response_content = await self.process_food_query(content)
            elif category == "weather":
                response_content = await self.process_weather_query(content)
            else:
                response_content = "I can only help with food and weather related queries."

            # Store AI response
            ai_message = Message(
                is_ai=True,
                content=response_content,
                timestamp=datetime.utcnow()
            )
            self.db_session.add(ai_message)
            self.db_session.commit()

            return {
                "user_message": user_message,
                "ai_message": ai_message,
                "category": category
            }

        except Exception as e:
            self.db_session.rollback()
            raise Exception(f"Error processing message: {str(e)}")