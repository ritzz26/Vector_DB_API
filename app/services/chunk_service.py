from typing import Optional
from app.models.chunk import Chunk
from app.db.store import store

def add_chunk(library_id: str, document_id: str, chunk: Chunk) -> bool:
    return store.add_chunk(library_id, document_id, chunk)

def delete_chunk(library_id: str, document_id: str, chunk_id: str) -> bool:
    return store.delete_chunk(library_id, document_id, chunk_id)

def get_all_chunks(library_id: str) -> Optional[List[Chunk]]:
    return store.get_all_chunks(library_id)
