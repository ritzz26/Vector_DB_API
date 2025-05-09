from app.services.vector_index import VectorIndexManager
import app.services.chunk_service as chunk_srv
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

    def index_all_chunks_from_store(self):
        all_libraries = chunk_srv.store.list_libraries()
        for lib in all_libraries.values():
            for doc in lib.documents:
                for chunk in doc.chunks:
                    if chunk.embedding:
                        self.index_chunk(chunk)


# convert to singleton usage
knn_service = KNNService(index_type="grid")
