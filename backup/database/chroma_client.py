import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from config import Config

class ChromaDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.DB_PATH)
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=Config.OPENAI_API_KEY,
            model_name=Config.OPENAI_EMBEDDING_MODEL
        )

    def get_collection(self, collection_name: str):
        """Get or create a collection with the specified name"""
        return self.client.get_or_create_collection(
            name=collection_name,
            embedding_function=self.embedding_function
        )

    def add_pages(self, collection_name: str, pages: list):
        """Add PDF pages to the specified collection"""
        collection = self.get_collection(collection_name)
        
        for page_number, content in enumerate(pages):
            collection.upsert(
                ids=[str(page_number + 1)],
                documents=[str(content)]
            )
        
        return collection.peek()

    def add_chunks(self, collection_name: str, chunks: list):
        """Add text chunks to the specified collection"""
        collection = self.get_collection(collection_name)
        
        for chunk_id, chunk_content in enumerate(chunks):
            collection.upsert(
                ids=[f"chunk_{chunk_id + 1}"],
                documents=[str(chunk_content)]
            )
        
        return collection.peek()