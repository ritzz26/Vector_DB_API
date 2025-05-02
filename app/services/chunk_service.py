from typing import Optional, List
from app.models.chunk import Chunk
from app.db import store

def add_chunk(library_id: str, document_id: str, chunk: Chunk) -> bool:
    """
    Add a chunk to a specific document in a library.

    Args:
        library_id (str): ID of the library containing the document
        document_id (str): ID of the document to add chunk to 
        chunk (Chunk): Chunk object to add

    Returns:
        bool: True if document was found and chunk added, False otherwise
    """
    return store.add_chunk(library_id, document_id, chunk)

def delete_chunk(library_id: str, document_id: str, chunk_id: str) -> bool:
    """
    Remove a chunk from a document in a library.

    Args:
        library_id (str): ID of the library containing the document
        document_id (str): ID of the document containing the chunk
        chunk_id (str): ID of the chunk to delete

    Returns:
        bool: True if chunk was found and deleted, False otherwise
    """
    return store.delete_chunk(library_id, document_id, chunk_id)

def get_all_chunks(library_id: str) -> Optional[List[Chunk]]:
    """
    Get all chunks from all documents in a library.

    Args:
        library_id (str): ID of the library to get chunks from

    Returns:
        Optional[List[Chunk]]: List of all chunks if library exists, None otherwise
    """
    return store.get_all_chunks(library_id)
