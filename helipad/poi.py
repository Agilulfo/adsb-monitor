POIs = dict()


def load_pois(descriptions):
    for description in descriptions:
        poi = PointOfIntrest(description)
        POIs[poi.name] = poi


def get_poi(name):
    return POIs.get(name)


def reset_pois():
    POIs = dict()


class PointOfIntrest:
    def __init__(self, description):
        self.name = description["name"]
        self.location = (description["latitude"], description["longitude"])

    def __hash__(self):
        return hash(self.name)
