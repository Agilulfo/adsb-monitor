from helipad.poi import get_poi

EVENTS = []

def load_events(descriptions):
    for description in descriptions:
        event = Event(description)
        EVENTS.append(event)

def reset_events():
    EVENTS.clear()

def get_events():
    return EVENTS

class Event:
    def __init__(self, description):
        self.type = description["type"]
        poi = get_poi(description["poi"])
        self.poi = poi

    def __repr__(self):
        return f"EVENT: {self.type} - {self.poi.name}"
