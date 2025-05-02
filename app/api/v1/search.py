from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from app.services import chunk_service
from app.services.knn_service import KNNService
from app.models.chunk import Chunk

router = APIRouter(prefix="/search", tags=["search"])
knn_service = KNNService(index_type="grid")

class SearchQuery(BaseModel):
    library_id: str
    embedding: List[float]
    k: int = 5

@router.post("/", response_model=List[Chunk])
def search(query: SearchQuery):
    chunks = chunk_service.get_all_chunks(query.library_id)
    if not chunks:
        raise HTTPException(status_code=404, detail="Library not found")

    knn_service.index_chunks_bulk(chunks)
    top_k = knn_service.search(query.embedding, k=query.k)
    return [chunk for chunk, _ in top_k]
