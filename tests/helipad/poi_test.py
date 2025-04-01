from helipad.poi import load_pois, get_poi


def test_poi_loading_and_query():
    poi_list = [
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
    load_pois(poi_list)

    poi = get_poi("Frankfurt")

    assert poi.name == "Frankfurt"
