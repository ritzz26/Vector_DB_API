from typing import Optional
from app.models.document import Document
from app.db import store

def add_document(library_id: str, document: Document) -> bool:
    """
    Add a document to a library.

    Args:
        library_id (str): ID of the library to add document to
        document (Document): Document object to add

    Returns:
        bool: True if library was found and document added, False otherwise
    """
    return store.add_document(library_id, document)

def get_document(library_id: str, document_id: str) -> Optional[Document]:
    """
    Get a document from a library by ID.

    Args:
        library_id (str): ID of the library containing the document
        document_id (str): ID of the document to retrieve

    Returns:
        Optional[Document]: Document if found, None otherwise
    """
    return store.get_document(library_id, document_id)

def delete_document(library_id: str, document_id: str) -> bool:
    """
    Delete a document from a library.

    Args:
        library_id (str): ID of the library containing the document
        document_id (str): ID of the document to delete

    Returns:
        bool: True if document was found and deleted, False otherwise
    """
    return store.delete_document(library_id, document_id)
