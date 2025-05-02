from app.services.indexing_algorithms import LinearIndex, GridIndex, SortedListIndex
from typing import List, Tuple

class VectorIndexManager:
    """
    Manages a vector index implementation (Linear, Grid, Sorted).

    Usage:
        index = VectorIndexManager(index_type="grid")
        index.add("chunk_id", [0.1, 0.2, 0.3])
        results = index.search([0.1, 0.2, 0.3], k=5)
    """

    def __init__(self, index_type: str = "linear"):
        if index_type == "linear":
            self.index = LinearIndex()
        elif index_type == "grid":
            self.index = GridIndex(grid_size=0.1)
        elif index_type == "sorted":
            self.index = SortedListIndex()
        else:
            raise ValueError(f"Invalid index type: {index_type}")

    def add(self, id: str, vector: List[float]):
        """
        Add a vector to the index.
        """
        self.index.add(id, vector)

    def search(self, query: List[float], k: int) -> List[Tuple[str, float]]:
        """
        Search for k nearest neighbors.

        Returns:
            List of tuples (id, similarity score)
        """
        return self.index.search(query, k)
