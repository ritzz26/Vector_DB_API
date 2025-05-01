from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services import chunk_service, knn_service
from app.models.chunk import Chunk

router = APIRouter(prefix="/search", tags=["search"])

class SearchQuery(BaseModel):
    library_id: str
    embedding: List[float]
    k: int = 5

@router.post("/", response_model=List[Chunk])
def search(query: SearchQuery):
    chunks = chunk_service.get_all_chunks(query.library_id)
    if chunks is None:
        raise HTTPException(status_code=404, detail="Library not found")

    top_k = knn_service.knn_search(chunks, query.embedding, k=query.k)
    return [chunk for chunk, _ in top_k]
