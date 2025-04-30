from typing import List, Tuple
from app.models.chunk import Chunk
import math

def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
    dot = sum(a * b for a, b in zip(vec1, vec2))
    norm1 = math.sqrt(sum(a * a for a in vec1))
    norm2 = math.sqrt(sum(b * b for b in vec2))
    return dot / (norm1 * norm2 + 1e-8)

def knn_search(chunks: List[Chunk], query_vector: List[float], k: int = 5) -> List[Tuple[Chunk, float]]:
    scored = [(chunk, cosine_similarity(chunk.embedding, query_vector)) for chunk in chunks]
    return sorted(scored, key=lambda x: x[1], reverse=True)[:k]
