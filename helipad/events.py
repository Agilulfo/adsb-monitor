from helipad.poi import get_poi


class Event:
    def __init__(self, description):
        self.type = description["type"]
        poi = get_poi(description["poi"])
        self.poi = poi

    def __repr__(self):
        return f"EVENT: {self.type} - {self.poi.name}"
