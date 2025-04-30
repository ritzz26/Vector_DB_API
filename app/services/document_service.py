from typing import Optional
from app.models.document import Document
from app.db.store import store  # reuse the same global store

def add_document(library_id: str, document: Document) -> bool:
    return store.add_document(library_id, document)

def get_document(library_id: str, document_id: str) -> Optional[Document]:
    return store.get_document(library_id, document_id)

def delete_document(library_id: str, document_id: str) -> bool:
    return store.delete_document(library_id, document_id)
