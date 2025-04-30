import threading
from typing import Dict, Optional
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk

class InMemoryVectorStore:
    def __init__(self):
        self.libraries: Dict[str, Library] = {}
        self.lock = threading.RLock()

    def add_library(self, library: Library) -> None:
        with self.lock:
            self.libraries[library.id] = library

    def get_library(self, library_id: str) -> Optional[Library]:
        with self.lock:
            return self.libraries.get(library_id)

    def update_library(self, library_id: str, updated: Library) -> bool:
        with self.lock:
            if library_id in self.libraries:
                self.libraries[library_id] = updated
                return True
            return False

    def delete_library(self, library_id: str) -> bool:
        with self.lock:
            return self.libraries.pop(library_id, None) is not None

    def list_libraries(self) -> Dict[str, Library]:
        with self.lock:
            return dict(self.libraries)

    def add_document(self, library_id: str, document: Document) -> bool:
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                lib.documents.append(document)
                return True
            return False

    def get_document(self, library_id: str, document_id: str) -> Optional[Document]:
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                return next((doc for doc in lib.documents if doc.id == document_id), None)
            return None

    def delete_document(self, library_id: str, document_id: str) -> bool:
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                original_len = len(lib.documents)
                lib.documents = [doc for doc in lib.documents if doc.id != document_id]
                return len(lib.documents) != original_len
            return False

    def add_chunk(self, library_id: str, document_id: str, chunk: Chunk) -> bool:
        with self.lock:
            doc = self.get_document(library_id, document_id)
            if doc:
                doc.chunks.append(chunk)
                return True
            return False

    def delete_chunk(self, library_id: str, document_id: str, chunk_id: str) -> bool:
        with self.lock:
            doc = self.get_document(library_id, document_id)
            if doc:
                original_len = len(doc.chunks)
                doc.chunks = [c for c in doc.chunks if c.id != chunk_id]
                return len(doc.chunks) != original_len
            return False

    def get_all_chunks(self, library_id: str) -> Optional[list[Chunk]]:
        with self.lock:
            lib = self.libraries.get(library_id)
            if not lib:
                return None
            chunks = []
            for doc in lib.documents:
                chunks.extend(doc.chunks)
            return chunks
