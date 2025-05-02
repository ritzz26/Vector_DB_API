from fastapi import APIRouter, HTTPException
from app.models.library import Library
from app.services import library_service

router = APIRouter(prefix="/libraries", tags=["libraries"])

@router.post("/", response_model=Library)
def create_library(library: Library):
    """
    Create a new library.
    
    Args:
        library (Library): The library data to create
        
    Returns:
        Library: The created library
    """
    return library_service.create_library(library)

@router.get("/{library_id}", response_model=Library)
def get_library(library_id: str):
    """
    Get a library by ID.
    
    Args:
        library_id (str): The ID of the library to retrieve
        
    Returns:
        Library: The requested library
        
    Raises:
        HTTPException: If library is not found (404)
    """
    lib = library_service.get_library(library_id)
    if not lib:
        raise HTTPException(status_code=404, detail="Library not found")
    return lib

@router.get("/", response_model=list[Library])
def list_libraries():
    """
    List all libraries.
    
    Returns:
        list[Library]: List of all libraries
    """
    return library_service.list_libraries()

@router.put("/{library_id}", response_model=bool)
def update_library(library_id: str, updated: Library):
    """
    Update a library.
    
    Args:
        library_id (str): The ID of the library to update
        updated (Library): The updated library data
        
    Returns:
        bool: True if library was updated successfully
    """
    return library_service.update_library(library_id, updated)

@router.delete("/{library_id}", response_model=bool)
def delete_library(library_id: str):
    """
    Delete a library.
    
    Args:
        library_id (str): The ID of the library to delete
        
    Returns:
        bool: True if library was deleted successfully
    """
    return library_service.delete_library(library_id)
