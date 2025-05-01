from fastapi import APIRouter
from .library import router as library_router
from .document import router as document_router
from .chunk import router as chunk_router
from .search import router as search_router

api_router = APIRouter()
api_router.include_router(library_router)
api_router.include_router(document_router)
api_router.include_router(chunk_router)
api_router.include_router(search_router)
