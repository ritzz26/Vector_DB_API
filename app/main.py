from fastapi import FastAPI
from app.api.v1 import api_router

app = FastAPI(title="Vector DB API")
app.include_router(api_router, prefix="/api/v1")
