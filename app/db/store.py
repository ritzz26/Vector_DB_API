import threading
from typing import Dict, Optional
from app.models.library import Library
from app.models.document import Document
from app.models.chunk import Chunk

class InMemoryVectorStore:
    """
    An in-memory store for managing libraries, documents and chunks with thread-safe operations.
    Uses RLock for thread safety to allow multiple operations from the same thread.
    
    Usage:
        -  Use this class to manage hierarchical data structures.
        - Call the appropriate methods to perform CRUD operations on data.
    """
    
    def __init__(self):
        """
        Initialize the store with empty libraries dictionary and reentrant lock.
        """
        self.libraries: Dict[str, Library] = {}
        self.lock = threading.RLock()

    def add_library(self, library: Library) -> None:
        """
        Add a new library to the store.

        Args:
            library (Library): The library object to add

        Returns:
            None
        """
        with self.lock:
            self.libraries[library.id] = library

    def get_library(self, library_id: str) -> Optional[Library]:
        """
        Retrieve a library by its ID.

        Args:
            library_id (str): ID of the library to retrieve

        Returns:
            Optional[Library]: The library if found, None otherwise
        """
        with self.lock:
            return self.libraries.get(library_id)

    def update_library(self, library_id: str, updated: Library) -> bool:
        """
        Update an existing library with new data.

        Args:
            library_id (str): ID of the library to update
            updated (Library): New library data

        Returns:
            bool: True if library was found and updated, False otherwise
        """
        with self.lock:
            if library_id in self.libraries:
                self.libraries[library_id] = updated
                return True
            return False

    def delete_library(self, library_id: str) -> bool:
        """
        Remove a library from the store.

        Args:
            library_id (str): ID of the library to delete

        Returns:
            bool: True if library was found and deleted, False otherwise
        """
        with self.lock:
            return self.libraries.pop(library_id, None) is not None

    def list_libraries(self) -> Dict[str, Library]:
        """
        Get all libraries in the store.

        Returns:
            Dict[str, Library]: Dictionary mapping library IDs to Library objects
        """
        with self.lock:
            return dict(self.libraries)

    def add_document(self, library_id: str, document: Document) -> bool:
        """
        Add a document to a specific library.

        Args:
            library_id (str): ID of the library to add document to
            document (Document): Document object to add

        Returns:
            bool: True if library was found and document added, False otherwise
        """
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                lib.documents.append(document)
                return True
            return False

    def get_document(self, library_id: str, document_id: str) -> Optional[Document]:
        """
        Retrieve a document from a library by its ID.

        Args:
            library_id (str): ID of the library containing the document
            document_id (str): ID of the document to retrieve

        Returns:
            Optional[Document]: The document if found, None otherwise
        """
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                return next((doc for doc in lib.documents if doc.id == document_id), None)
            return None

    def delete_document(self, library_id: str, document_id: str) -> bool:
        """
        Remove a document from a library.

        Args:
            library_id (str): ID of the library containing the document
            document_id (str): ID of the document to delete

        Returns:
            bool: True if document was found and deleted, False otherwise
        """
        with self.lock:
            lib = self.libraries.get(library_id)
            if lib:
                original_len = len(lib.documents)
                lib.documents = [doc for doc in lib.documents if doc.id != document_id]
                return len(lib.documents) != original_len
            return False

    def add_chunk(self, library_id: str, document_id: str, chunk: Chunk) -> bool:
        """
        Add a chunk to a specific document in a library.

        Args:
            library_id (str): ID of the library containing the document
            document_id (str): ID of the document to add chunk to
            chunk (Chunk): Chunk object to add

        Returns:
            bool: True if document was found and chunk added, False otherwise
        """
        with self.lock:
            doc = self.get_document(library_id, document_id)
            if doc:
                doc.chunks.append(chunk)
                return True
            return False

    def delete_chunk(self, library_id: str, document_id: str, chunk_id: str) -> bool:
        """
        Remove a chunk from a document in a library.

        Args:
            library_id (str): ID of the library containing the document
            document_id (str): ID of the document containing the chunk
            chunk_id (str): ID of the chunk to delete

        Returns:
            bool: True if chunk was found and deleted, False otherwise
        """
        with self.lock:
            doc = self.get_document(library_id, document_id)
            if doc:
                original_len = len(doc.chunks)
                doc.chunks = [c for c in doc.chunks if c.id != chunk_id]
                return len(doc.chunks) != original_len
            return False

    def get_all_chunks(self, library_id: str) -> Optional[list[Chunk]]:
        """
        Get all chunks from all documents in a library.

        Args:
            library_id (str): ID of the library to get chunks from

        Returns:
            Optional[list[Chunk]]: List of all chunks if library exists, None otherwise
        """
        with self.lock:
            lib = self.libraries.get(library_id)
            if not lib:
                return None
            chunks = []
            for doc in lib.documents:
                chunks.extend(doc.chunks)
            return chunks
