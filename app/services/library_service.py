from typing import List, Optional
from app.models.library import Library
from app.db.store import InMemoryVectorStore

store = InMemoryVectorStore()

def create_library(library: Library) -> Library:
    store.add_library(library)
    return library

def get_library(library_id: str) -> Optional[Library]:
    return store.get_library(library_id)

def update_library(library_id: str, updated_library: Library) -> bool:
    return store.update_library(library_id, updated_library)

def delete_library(library_id: str) -> bool:
    return store.delete_library(library_id)

def list_libraries() -> List[Library]:
    return list(store.list_libraries().values())
