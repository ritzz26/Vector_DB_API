from fastapi import APIRouter, HTTPException
from app.models.chunk import Chunk
from app.services import chunk_service

router = APIRouter(prefix="/libraries/{library_id}/documents/{document_id}/chunks", tags=["chunks"])

@router.post("/", response_model=bool)
def add_chunk(library_id: str, document_id: str, chunk: Chunk):
    return chunk_service.add_chunk(library_id, document_id, chunk)

@router.delete("/{chunk_id}", response_model=bool)
def delete_chunk(library_id: str, document_id: str, chunk_id: str):
    return chunk_service.delete_chunk(library_id, document_id, chunk_id)
