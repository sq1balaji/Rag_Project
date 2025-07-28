import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL")
    QDRANT_HOST = os.getenv("QDRANT_HOST")
    QDRANT_URL = os.getenv("QDRANT_URL")
    OLLAMA_API = os.getenv("OLLAMA_API")
    COLLECTION_NAME = os.getenv("COLLECTION_NAME", "rag_data")
