import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    POSTGRES_URI = os.getenv("POSTGRES_URI")
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    OLLAMA_URL = os.getenv("OLLAMA_URL")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_data")
