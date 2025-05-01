from fastapi import APIRouter, HTTPException
from app.models.document import Document
from app.services import document_service

router = APIRouter(prefix="/libraries/{library_id}/documents", tags=["documents"])

@router.post("/", response_model=bool)
def add_document(library_id: str, document: Document):
    return document_service.add_document(library_id, document)

@router.get("/{document_id}", response_model=Document)
def get_document(library_id: str, document_id: str):
    doc = document_service.get_document(library_id, document_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")
    return doc

@router.delete("/{document_id}", response_model=bool)
def delete_document(library_id: str, document_id: str):
    return document_service.delete_document(library_id, document_id)
