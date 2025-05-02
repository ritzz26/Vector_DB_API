from app.services.vector_index import VectorIndexManager
import pytest

@pytest.mark.parametrize("index_type", ["linear", "grid", "sorted"])
def test_vector_index_manager(index_type):
    """
    Test the core functionality of the vector index manager.
    
    Tests:
        - Creating vector index manager instances with different index types
        - Adding vectors to the index
        - Searching for nearest neighbors
        - Verifying search results format and correctness
        
    Args:
        index_type: The type of index to use ("linear", "grid", or "sorted")
    """
    index = VectorIndexManager(index_type=index_type)

    index.add("v1", [0.1, 0.2, 0.3])
    index.add("v2", [0.9, 0.8, 0.7])

    results = index.search([0.1, 0.2, 0.3], k=1)

    assert len(results) == 1
    assert results[0][0] == "v1"
    assert results[0][1] > 0.0