import chromadb
from chromadb.utils import embedding_functions
from config import Config
from typing import List, Dict, Any

class ChromaDatabase:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.CHROMADB_PATH)
        # Update the embedding function initialization
        self.embedding_function = embedding_functions.OpenAIEmbeddingFunction(
            api_key=Config.OPENAI_API_KEY,
            model_name=Config.OPENAI_EMBEDDING_MODEL,  # Use the config value
            dimensions=1536  # Add dimensions parameter
        )

    def get_collection(self, collection_name: str):
        """Get or create a collection with the specified name"""
        try:
            return self.client.get_or_create_collection(
                name=collection_name,
                embedding_function=self.embedding_function
            )
        except Exception as e:
            print(f"Error creating collection: {str(e)}")
            raise

    def add_pages(self, collection_name: str, pages: List[Any]):
        """Add PDF pages to the specified collection"""
        try:
            collection = self.get_collection(collection_name)
            documents = []
            metadatas = []
            ids = []
            
            for i, page in enumerate(pages):
                # Clean and validate the text
                text = str(page.page_content).strip()
                if text:  # Only add non-empty documents
                    documents.append(text)
                    metadatas.append({
                        "source": str(page.metadata.get("source", "")),
                        "page": i + 1
                    })
                    ids.append(f"page_{i + 1}")
            
            if documents:  # Only add if we have valid documents
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Added {len(documents)} pages to collection {collection_name}")
            return collection.peek()
        except Exception as e:
            print(f"Error adding pages: {str(e)}")
            raise

    def add_chunks(self, collection_name: str, chunks: List[Any]):
        """Add text chunks to the specified collection"""
        try:
            collection = self.get_collection(collection_name)
            documents = []
            metadatas = []
            ids = []
            
            for i, chunk in enumerate(chunks):
                # Clean and validate the text
                text = str(chunk.page_content).strip()
                if text:  # Only add non-empty documents
                    documents.append(text)
                    metadatas.append({
                        "source": str(chunk.metadata.get("source", "")),
                        "page": chunk.metadata.get("page", 0),
                        "chunk": i + 1
                    })
                    ids.append(f"chunk_{i + 1}")
            
            if documents:  # Only add if we have valid documents
                collection.add(
                    documents=documents,
                    metadatas=metadatas,
                    ids=ids
                )
                print(f"Added {len(documents)} chunks to collection {collection_name}")
            return collection.peek()
        except Exception as e:
            print(f"Error adding chunks: {str(e)}")
            raise