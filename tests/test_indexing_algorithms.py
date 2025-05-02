import pytest
from app.services.indexing_algorithms import LinearIndex, GridIndex, SortedListIndex

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
    # Initialize index, with special handling for GridIndex which needs grid_size
    index = index_class() if index_class != GridIndex else index_class(grid_size=0.1)

    # Add test vectors
    index.add("v1", [0.1, 0.2, 0.3])  # Vector that matches search query
    index.add("v2", [0.9, 0.8, 0.7])  # Distant vector

    # Search for nearest neighbor to first vector
    results = index.search([0.1, 0.2, 0.3], k=1)

    # Verify results
    assert len(results) == 1  # Should return exactly one result
    assert results[0][0] == "v1"  # First result should be v1 since query matches it
    assert results[0][1] > 0.0  # Similarity score should be positive