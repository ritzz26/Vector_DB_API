import pytest
from app.services.knn_service import KNNService
from app.models.chunk import Chunk

@pytest.mark.parametrize("index_type", ["linear", "grid", "sorted"])
def test_knn_service(index_type):
    service = KNNService(index_type=index_type)

    chunks = [
        Chunk(id="c1", content="First chunk", embedding=[0.1, 0.2, 0.3]),
        Chunk(id="c2", content="Second chunk", embedding=[0.11, 0.21, 0.31]),
        Chunk(id="c3", content="Third chunk", embedding=[0.9, 0.8, 0.7]),
    ]

    service.index_chunks_bulk(chunks)

    results = service.search([0.1, 0.2, 0.3], k=3)

    assert len(results) >= 1

    assert results[0][0].id == "c1"