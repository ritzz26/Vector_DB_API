from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime

class Chunk(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    content: str
    embedding: Optional[List[float]] = None # Created using Cohere API
    metadata: Dict[str, str] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.utcnow)
