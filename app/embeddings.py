import requests
import time
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

def get_embedding(text: str):
    for attempt in range(10):
        try:
            response = requests.post(f"{Config.OLLAMA_API}/api/embeddings", json={
                "model": "nomic-embed-text:latest", 
                "prompt": text
            })
            response.raise_for_status()
            return response.json()["embedding"]
        except requests.exceptions.RequestException as e:
            print(f"[Embedding Retry {attempt+1}/10] Ollama not ready yet: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to connect to Ollama embedding API after 10 retries.")
