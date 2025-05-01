from fastapi import APIRouter, HTTPException
from app.models.library import Library
from app.services import library_service

router = APIRouter(prefix="/libraries", tags=["libraries"])

@router.post("/", response_model=Library)
def create_library(library: Library):
    return library_service.create_library(library)

@router.get("/{library_id}", response_model=Library)
def get_library(library_id: str):
    lib = library_service.get_library(library_id)
    if not lib:
        raise HTTPException(status_code=404, detail="Library not found")
    return lib

@router.get("/", response_model=list[Library])
def list_libraries():
    return library_service.list_libraries()

@router.put("/{library_id}", response_model=bool)
def update_library(library_id: str, updated: Library):
    return library_service.update_library(library_id, updated)

@router.delete("/{library_id}", response_model=bool)
def delete_library(library_id: str):
    return library_service.delete_library(library_id)
