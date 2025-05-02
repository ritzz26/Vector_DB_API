from typing import List, Dict, Tuple
from math import sqrt
import bisect

class VectorUtils:
    @staticmethod
    def cosine_similarity(vec1: List[float], vec2: List[float]) -> float:
        dot = sum(x * y for x, y in zip(vec1, vec2))
        norm1 = sqrt(sum(x * x for x in vec1))
        norm2 = sqrt(sum(y * y for y in vec2))
        if norm1 == 0 or norm2 == 0:
            return 0.0
        return dot / (norm1 * norm2)


class LinearIndex:
    def __init__(self):
        self.data: Dict[str, List[float]] = {}

    def add(self, id: str, vector: List[float]):
        self.data[id] = vector

    def search(self, query: List[float], k: int) -> List[Tuple[str, float]]:
        results = [(id, VectorUtils.cosine_similarity(query, vec)) for id, vec in self.data.items()]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]


class GridIndex:
    def __init__(self, grid_size: float = 0.1):
        self.grid_size = grid_size
        self.buckets: Dict[str, List[Tuple[str, List[float]]]] = {}

    def _hash(self, vector: List[float]) -> str:
        return "-".join(str(int(x // self.grid_size)) for x in vector)

    def add(self, id: str, vector: List[float]):
        key = self._hash(vector)
        if key not in self.buckets:
            self.buckets[key] = []
        self.buckets[key].append((id, vector))

    def search(self, query: List[float], k: int) -> List[Tuple[str, float]]:
        key = self._hash(query)
        candidates = self.buckets.get(key, [])
        results = [(id, VectorUtils.cosine_similarity(query, vec)) for id, vec in candidates]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]


class SortedListIndex:
    def __init__(self):
        self.data: List[Tuple[float, str, List[float]]] = []

    def _norm(self, vector: List[float]) -> float:
        return sqrt(sum(x * x for x in vector))

    def add(self, id: str, vector: List[float]):
        norm = self._norm(vector)
        bisect.insort(self.data, (norm, id, vector))

    def search(self, query: List[float], k: int) -> List[Tuple[str, float]]:
        query_norm = self._norm(query)
        idx = bisect.bisect_left(self.data, (query_norm, "", []))
        candidates = self.data[max(0, idx - 10):idx + 10]

        results = [(id, VectorUtils.cosine_similarity(query, vec)) for _, id, vec in candidates]
        results.sort(key=lambda x: x[1], reverse=True)
        return results[:k]


# Example usage:
if __name__ == "__main__":
    index = GridIndex()
    index.add("1", [0.1, 0.2, 0.3])
    index.add("2", [0.11, 0.19, 0.31])
    index.add("3", [0.9, 0.8, 0.7])
    
    print("Results:", index.search([0.1, 0.2, 0.3], k=2))
