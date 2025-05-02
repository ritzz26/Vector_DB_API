import pytest
from app.services.indexing_algorithms import LinearIndex, GridIndex, SortedListIndex

@pytest.mark.parametrize("index_class", [LinearIndex, GridIndex, SortedListIndex])
def test_index_algorithms(index_class):
    index = index_class() if index_class != GridIndex else index_class(grid_size=0.1)

    index.add("v1", [0.1, 0.2, 0.3])
    index.add("v2", [0.9, 0.8, 0.7])

    results = index.search([0.1, 0.2, 0.3], k=1)

    assert len(results) == 1
    assert results[0][0] == "v1"
    assert results[0][1] > 0.0