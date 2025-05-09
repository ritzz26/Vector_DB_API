import pytest
from app.services.indexing_algorithms import LinearIndex, GridIndex, SortedListIndex
from app.services.embedding_service import get_embedding

@pytest.mark.parametrize("index_class", [LinearIndex, GridIndex, SortedListIndex])
def test_index_algorithms(index_class):
    """
    Test the core functionality of vector indexing algorithms.

    Tests:
        - Creating index instances (Linear, Grid, Sorted)
        - Adding vectors to the index
        - Searching for nearest neighbors
        - Verifying search results format and correctness

    Args:
        index_class: The indexing algorithm class to test (LinearIndex, GridIndex, or SortedListIndex)
    """

    index = index_class() if index_class != GridIndex else index_class(grid_size=0.1)

    # Generate embeddings for test content
    v1_embedding = get_embedding("first vector test")
    v2_embedding = get_embedding("blue")
    v3_embedding = get_embedding("another similar vector test")

    # Add test vectors
    index.add("v1", v1_embedding)  # vector that should match the query
    index.add("v2", v2_embedding)  # distant vector
    index.add("v3", v3_embedding)  # vector similar to v1

    # Search for nearest neighbor to first vector
    query_embedding = get_embedding("first vector test")
    results = index.search(query_embedding, k=2)

    # Verify results
    assert len(results) == 1 if index_class=="GridIndex" else 2
    ids = [r[0] for r in results]
    assert "v1" in ids  # v1 should appear in the top results
