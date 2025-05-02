from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services import chunk_service
from app.services.knn_service import KNNService
from app.models.chunk import Chunk

router = APIRouter(prefix="/search", tags=["search"])
knn_service = KNNService(index_type="grid")

class SearchQuery(BaseModel):
    """
    Model for search query parameters.
    
    Attributes:
        library_id (str): ID of the library to search in
        embedding (List[float]): Vector embedding to search for similar chunks
        k (int): Number of results to return (default: 5)
    """
    library_id: str
    embedding: List[float]
    k: int = 5

@router.post("/", response_model=List[Chunk])
def search(query: SearchQuery):
    """
    Search for chunks in a library using KNN similarity search.
    
    Args:
        query (SearchQuery): The search parameters including library_id, embedding vector, and k
        
    Returns:
        List[Chunk]: List of k most similar chunks to the query embedding
        
    Raises:
        HTTPException: If library is not found (404)
    """
    chunks = chunk_service.get_all_chunks(query.library_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="Library not found")

    knn_service.index_chunks_bulk(chunks)
    top_k = knn_service.search(query.embedding, k=query.k)
    return [chunk for chunk, _ in top_k]
