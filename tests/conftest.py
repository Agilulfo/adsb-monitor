import pytest
import helipad.poi as poi


DEFAULT_POIS = [
    {
        "name": "Frankfurt",
        "latitude": 50.033333,
        "longitude": 8.570556,
        "altitude": 200,
    },
    {
        "name": "Warsaw Chopin",
        "latitude": 52.165833,
        "longitude": 20.967222,
        "altitude": 600,
    },
]


@pytest.fixture
def load_pois():
    """
    load some default PointOfInterests
    """
    poi.load_pois(DEFAULT_POIS)
    yield
    poi.reset_pois()
