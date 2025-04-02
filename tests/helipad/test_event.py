from helipad.events import Event, load_events, get_events


def test_event_creation(load_pois):
    event = Event({"type": "landing", "poi": "Warsaw Chopin"})
    assert repr(event) == "EVENT: landing - Warsaw Chopin"


def test_event_loading(load_pois):
    events = [
        {"type": "landing", "poi": "Warsaw Chopin"},
        {"type": "takeoff", "poi": "Frankfurt"}
    ]

    load_events(events)
    events = get_events()
    created_events = {(event.type, event.poi.name) for event in events}
    assert ("landing", "Warsaw Chopin") in created_events
