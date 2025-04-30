from typing import List, Dict
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from .chunk import Chunk

class Document(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    chunks: List[Chunk] = []
    metadata: Dict[str, str] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
