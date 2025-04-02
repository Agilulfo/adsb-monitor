import datetime

from helipad.aircraft import Aircraft

class FootprintDetector:
    def __init__(self):
        self.seen_messages = set()

    def handle_message(self, message):
        # build message footprint
        reported_fields = message.reported_fields()
        footprint = tuple([message.subtype()] + reported_fields)

        # detect new footprints
        if footprint not in self.seen_messages:
            self.seen_messages.add(footprint)
            print(f"New message: {footprint} - {message.raw_message}")


class AirTracking:
    def __init__(self):
        self.aircrafts = {}

    def handle_message(self, message):
        hex_code = message.hex_code()

        if hex_code not in self.aircrafts:
            new_aircraft = Aircraft(hex_code)
            self.aircrafts[hex_code] = new_aircraft

        aircraft = self.aircrafts[hex_code]
        aircraft.track(message)

        print(aircraft)


class DumpHandler:
    def __init__(self, filename=None):
        self.dump_file = open(
            filename or self.__class__.default_filename(), "w", buffering=1
        )

    def default_filename():
        now = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
        return f"{now}_dump.txt"

    def handle_message(self, message):
        self.dump_file.write(f"{message}\n")
