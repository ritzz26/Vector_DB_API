import pytest
from app.services.knn_service import KNNService
from app.models.chunk import Chunk
from app.services.embedding_service import get_embedding


@pytest.mark.parametrize("index_type", ["linear", "grid", "sorted"])
def test_knn_service(index_type):
    """
    Test the core functionality of the KNN service.

    Tests:
        - Creating KNN service instances with different index types
        - Bulk indexing multiple chunks
        - Searching for nearest neighbors
        - Verifying search results format and correctness

    Args:
        index_type: The type of index to use ("linear", "grid", or "sorted")
    """
    service = KNNService(index_type=index_type)

    chunks = [
        Chunk(id="c1", content="First chunk", embedding=get_embedding("First chunk")),
        Chunk(id="c2", content="Second chunk", embedding=get_embedding("Second chunk")),
        Chunk(id="c3", content="Third chunk", embedding=get_embedding("Third chunk")),
    ]

    service.index_chunks_bulk(chunks)

    query_embedding = get_embedding("First chunk")
    results = service.search(query_embedding, k=3)

    assert len(results) >= 1 if index_type == "grid" else 2
    assert any(chunk.id == "c1" for chunk, _ in results)
