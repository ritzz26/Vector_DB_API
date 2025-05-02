# app/services/knn_service.py

from app.services.vector_index import VectorIndexManager
from app.models.chunk import Chunk
from typing import List, Tuple, Dict

class KNNService:
    """
    Handles indexing and searching chunks using VectorIndexManager.
    """

    def __init__(self, index_type: str = "linear"):
        self.index_manager = VectorIndexManager(index_type=index_type)
        self.chunk_lookup: Dict[str, Chunk] = {}

    def index_chunk(self, chunk: Chunk):
        """
        Index a chunk's embedding for search.
        """
        self.index_manager.add(chunk.id, chunk.embedding)
        self.chunk_lookup[chunk.id] = chunk

    def search(self, query_embedding: List[float], k: int) -> List[Tuple[Chunk, float]]:
        """
        Search for k nearest chunks based on query embedding.

        Returns:
            List of tuples (Chunk, similarity score)
        """
        results = self.index_manager.search(query_embedding, k)
        return [(self.chunk_lookup[chunk_id], score) for chunk_id, score in results]

    def index_chunks_bulk(self, chunks: List[Chunk]):
        """
        Bulk index chunks.
        """
        for chunk in chunks:
            self.index_chunk(chunk)


# Example usage
if __name__ == "__main__":
    from app.models.chunk import Chunk

    chunks = [
        Chunk(id="c1", content="First chunk", embedding=[0.1, 0.2, 0.3]),
        Chunk(id="c2", content="Second chunk", embedding=[0.11, 0.21, 0.31]),
        Chunk(id="c3", content="Third chunk", embedding=[0.9, 0.8, 0.7]),
    ]

    service = KNNService(index_type="grid")
    service.index_chunks_bulk(chunks)

    results = service.search([0.1, 0.2, 0.3], k=2)

    for chunk, score in results:
        print(f"Found: {chunk.id} with score {score}")
