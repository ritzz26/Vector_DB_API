import pytest
import httpx
import os
from dotenv import load_dotenv

@pytest.fixture(scope="module")
def cohere_client():
    load_dotenv()
    
    api_key = os.getenv("COHERE_API_KEY")
    if not api_key:
        pytest.skip("COHERE_API_KEY not found in environment")
        
    return {
        "url": "https://api.cohere.ai/v1/embed",
        "headers": {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    }

def test_cohere_embedding(cohere_client):
    payload = {
        "texts": ["test"],
        "model": "embed-english-v3.0", 
        "input_type": "search_document"
    }

    response = httpx.post(
        cohere_client["url"],
        json=payload,
        headers=cohere_client["headers"]
    )

    assert response.status_code == 200
    response_data = response.json()
    assert "embeddings" in response_data
    assert len(response_data["embeddings"]) == 1
    assert isinstance(response_data["embeddings"][0], list)
