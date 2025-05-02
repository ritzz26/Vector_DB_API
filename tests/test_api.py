from fastapi.testclient import TestClient
from app.main import app
from uuid import uuid4

client = TestClient(app)

def test_create_and_get_library():
    """
    Test creating a new library and retrieving it.
    
    Tests:
        - POST /api/v1/libraries/ endpoint for creating a library
        - GET /api/v1/libraries/{id} endpoint for retrieving a library
        - Validates response status codes and data consistency
    """
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
    """
    Test adding a document to a library.
    
    Tests:
        - Creating a library
        - POST /api/v1/libraries/{id}/documents/ endpoint for adding a document
        - GET /api/v1/libraries/{id}/documents/{doc_id} endpoint for retrieving a document
        - Validates response status codes and document data consistency
    """
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
    """
    Test adding a chunk to a document and searching for it.
    
    Tests:
        - Creating a library and document
        - POST /api/v1/libraries/{id}/documents/{doc_id}/chunks/ endpoint for adding a chunk
        - POST /api/v1/search/ endpoint for searching chunks by embedding
        - Validates response status codes, search results and chunk data consistency
        - Verifies that search returns the correct chunk with matching embedding
    """
    lib_id = str(uuid4())
    doc_id = str(uuid4())
    chunk_id = str(uuid4())

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
