# app/services/embedding_service.py
import httpx
import os
from dotenv import load_dotenv

load_dotenv()

COHERE_API_KEY = os.getenv("COHERE_API_KEY")
COHERE_URL = "https://api.cohere.ai/v1/embed"

def get_embedding(text: str) -> list[float]:
    headers = {
        "Authorization": f"Bearer {COHERE_API_KEY}",
        "Content-Type": "application/json",
    }
    payload = {
        "texts": [text],
        "model": "embed-english-v3.0",
        "input_type": "search_document"
    }

    response = httpx.post(COHERE_URL, json=payload, headers=headers, timeout=10)
    response.raise_for_status()
    return response.json()["embeddings"][0]