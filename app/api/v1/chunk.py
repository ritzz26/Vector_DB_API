from fastapi import APIRouter, HTTPException
from app.models.chunk import Chunk
from app.services import chunk_service

router = APIRouter(prefix="/libraries/{library_id}/documents/{document_id}/chunks", tags=["chunks"])

@router.post("/", response_model=bool)
def add_chunk(library_id: str, document_id: str, chunk: Chunk):
    """
    Add a new chunk to a document in a library.
    
    Args:
        library_id (str): The ID of the library containing the document
        document_id (str): The ID of the document to add the chunk to
        chunk (Chunk): The chunk data to add
        
    Returns:
        bool: True if chunk was added successfully
    """
    return chunk_service.add_chunk(library_id, document_id, chunk)

@router.delete("/{chunk_id}", response_model=bool)
def delete_chunk(library_id: str, document_id: str, chunk_id: str):
    """
    Delete a chunk from a document in a library.
    
    Args:
        library_id (str): The ID of the library containing the document
        document_id (str): The ID of the document containing the chunk
        chunk_id (str): The ID of the chunk to delete
        
    Returns:
        bool: True if chunk was deleted successfully
    """
    return chunk_service.delete_chunk(library_id, document_id, chunk_id)
