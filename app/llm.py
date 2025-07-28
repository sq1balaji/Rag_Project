# import requests
# from app.config import Config
# from dotenv import load_dotenv

# load_dotenv()

# def generate_answer(prompt: str) -> str:
#     header = {"Content-Type": "application/json"}
#     response = requests.post(f"{Config.OLLAMA_API}/api/generate", json={
#         "model": "llama3.2:1b", 
#         "prompt": prompt,
#         "stream": False
#     }, headers = header)
#     return response.json()["response"]


import requests
import time
from app.config import Config
from dotenv import load_dotenv

load_dotenv()

def generate_answer(prompt: str) -> str:
    headers = {"Content-Type": "application/json"}
    for attempt in range(10):
        try:
            response = requests.post(f"{Config.OLLAMA_API}/api/generate", json={
                "model": "llama3.2:1b", 
                "prompt": prompt,
                "stream": False
            }, headers=headers)
            response.raise_for_status()
            return response.json()["response"]
        except requests.exceptions.RequestException as e:
            print(f"[Generate Retry {attempt+1}/10] Ollama not ready yet: {e}")
            time.sleep(2)
    raise RuntimeError("Failed to connect to Ollama generate API after 10 retries.")
