from typing import List, Optional
from app.models.library import Library
from app.db import store

def create_library(library: Library) -> Library:
    """
    Create a new library.

    Args:
        library (Library): Library object to create

    Returns:
        Library: The created library object
    """
    store.add_library(library)
    return library

def get_library(library_id: str) -> Optional[Library]:
    """
    Get a library by ID.

    Args:
        library_id (str): ID of the library to retrieve

    Returns:
        Optional[Library]: Library if found, None otherwise
    """
    return store.get_library(library_id)

def update_library(library_id: str, updated_library: Library) -> bool:
    """
    Update an existing library.

    Args:
        library_id (str): ID of the library to update
        updated_library (Library): New library object with updates

    Returns:
        bool: True if library was found and updated, False otherwise
    """
    return store.update_library(library_id, updated_library)

def delete_library(library_id: str) -> bool:
    """
    Delete a library.

    Args:
        library_id (str): ID of the library to delete

    Returns:
        bool: True if library was found and deleted, False otherwise
    """
    return store.delete_library(library_id)

def list_libraries() -> List[Library]:
    """
    Get a list of all libraries.

    Returns:
        List[Library]: List of all library objects
    """
    return list(store.list_libraries().values())
