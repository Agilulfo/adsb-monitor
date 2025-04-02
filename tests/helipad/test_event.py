from helipad.events import Event


def test_event_creation(load_pois):
    event = Event({"type": "landing", "poi": "Warsaw Chopin"})
    assert repr(event) == "EVENT: landing - Warsaw Chopin"
