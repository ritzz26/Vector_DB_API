from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

def test_create_and_get_library():
    lib_data = {
        "id": str(uuid4()),
        "name": "Test Library",
        "description": "Testing",
        "documents": [],
        "metadata": {}
    }
    response = client.post("/api/v1/libraries/", json=lib_data)
    assert response.status_code == 200
    created = response.json()
    assert created["name"] == "Test Library"

    get_resp = client.get(f"/api/v1/libraries/{lib_data['id']}")
    assert get_resp.status_code == 200
    assert get_resp.json()["id"] == lib_data["id"]

def test_add_document_to_library():
    # Create library first
    lib_id = str(uuid4())
    client.post("/api/v1/libraries/", json={
        "id": lib_id,
        "name": "DocTestLib",
        "description": "",
        "documents": [],
        "metadata": {}
    })

    doc_id = str(uuid4())
    doc = {
        "id": doc_id,
        "title": "Doc Title",
        "chunks": [],
        "metadata": {}
    }
    resp = client.post(f"/api/v1/libraries/{lib_id}/documents/", json=doc)
    assert resp.status_code == 200

    get_doc = client.get(f"/api/v1/libraries/{lib_id}/documents/{doc_id}")
    assert get_doc.status_code == 200
    assert get_doc.json()["title"] == "Doc Title"

def test_chunk_and_search():
    lib_id = str(uuid4())
    doc_id = str(uuid4())
    chunk_id = str(uuid4())

    # Setup
    client.post("/api/v1/libraries/", json={
        "id": lib_id,
        "name": "SearchLib",
        "description": "",
        "documents": [],
        "metadata": {}
    })

    client.post(f"/api/v1/libraries/{lib_id}/documents/", json={
        "id": doc_id,
        "title": "Doc",
        "chunks": [],
        "metadata": {}
    })

    chunk = {
        "id": chunk_id,
        "content": "test",
        "embedding": [0.1, 0.2, 0.3],
        "metadata": {}
    }
    client.post(f"/api/v1/libraries/{lib_id}/documents/{doc_id}/chunks/", json=chunk)

    # Search
    search = {
        "library_id": lib_id,
        "embedding": [0.1, 0.2, 0.3],
        "k": 1
    }
    resp = client.post("/api/v1/search/", json=search)
    assert resp.status_code == 200
    results = resp.json()
    assert len(results) == 1
    assert results[0]["id"] == chunk_id
