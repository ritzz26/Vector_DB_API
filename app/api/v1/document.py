from fastapi import APIRouter, HTTPException
from app.models.document import Document
from app.services import document_service

router = APIRouter(prefix="/libraries/{library_id}/documents", tags=["documents"])

@router.post("/", response_model=bool)
def add_document(library_id: str, document: Document):
    """
    Add a new document to a library.
    
    Args:
        library_id (str): The ID of the library to add the document to
        document (Document): The document data to add
        
    Returns:
        bool: True if document was added successfully
    """
    return document_service.add_document(library_id, document)

@router.get("/{document_id}", response_model=Document)
def get_document(library_id: str, document_id: str):
    """
    Get a document from a library by ID.
    
    Args:
        library_id (str): The ID of the library containing the document
        document_id (str): The ID of the document to retrieve
        
    Returns:
        Document: The requested document
        
    Raises:
        HTTPException: If document is not found (404)
    """
    doc = document_service.get_document(library_id, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}", response_model=bool)
def delete_document(library_id: str, document_id: str):
    """
    Delete a document from a library.
    
    Args:
        library_id (str): The ID of the library containing the document
        document_id (str): The ID of the document to delete
        
    Returns:
        bool: True if document was deleted successfully
    """
    return document_service.delete_document(library_id, document_id)
