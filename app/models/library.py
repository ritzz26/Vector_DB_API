from typing import List, Dict, Optional
from pydantic import BaseModel, Field
from uuid import uuid4
from datetime import datetime
from .document import Document

class Library(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    name: str
    description: Optional[str] = None
    documents: List[Document] = []
    metadata: Dict[str, str] = {}
    created_at: datetime = Field(default_factory=datetime.utcnow)
