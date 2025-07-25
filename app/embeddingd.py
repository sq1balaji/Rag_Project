import requests
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str):
    print("Started embedding...")
    response = requests.post(f"{Config.OLLAMA_URL}/api/embeddings", json={
        "model": "nomic-embed-text:latest", 
        "prompt": text
    })
    print("Finished Embedding")
    return response.json()["embedding"]
