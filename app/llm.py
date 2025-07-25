import requests
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

def generate_answer(prompt: str) -> str:
    response = requests.post(f"{Config.OLLAMA_URL}/api/generate", json={
        "model": "llama3.1:latest", 
        "prompt": prompt,
        "stream": False
    })
    return response.json()["response"]
