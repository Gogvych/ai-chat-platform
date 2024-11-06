from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
import chromadb
import chromadb.utils.embedding_functions as embedding_functions
from config import Config

client = chromadb.PersistentClient(path=Config.DB_PATH)
# DocumentPage Model: document_id, page_number, content, is_processed 

openai_ef = embedding_functions.OpenAIEmbeddingFunction(
                api_key=Config.OPENAI_API_KEY,
                model_name=Config.OPENAI_EMBEDDING_MODEL
            )

def process_pdf_pages(file_path: str):
    loader = PyPDFLoader(file_path)
    docs = loader.load()
    #lst=[]
    collection = client.get_or_create_collection(
        name="DocumentPage", 
        embedding_function=openai_ef
        )

    for page_number, content in enumerate(docs):
        #lst.append(content)
        collection.upsert(
            #document_id=collection.name,
            ids=[str(page_number+1)],
            documents = [str(content)]
            #is_processed = [True]
        )
        #print(f"Processing page {page_number}, length: {len(lst)}")
    #print(lst[2])
    text_splitter = RecursiveCharacterTextSplitter(
        # Set a really small chunk size, just to show.
        chunk_size=100,
        chunk_overlap=20,
        length_function=len,
        is_separator_regex=False,
    )   
    texts = text_splitter.split_documents(docs)
    #print(texts[0])
    #print(texts[1])
    print(collection.peek())
    return collection.peek()

processed_data = process_pdf("https://scholarspace.manoa.hawaii.edu/server/api/core/bitstreams/34fca09a-e2fd-4bb5-a411-8c5dd8e45b23/content")

#print(len(processed_data))