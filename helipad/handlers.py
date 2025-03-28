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


class Aircraft:
    def __init__(self, hex_code):
        self.positions = []
        self.hex_code = hex_code
        self.callsign = None
        self.squawk = None
        self.first_message_time = None
        self.last_message_time = None

    def _track_timestamp(self, timestamp):
        self.first_message_time = self.first_message_time or timestamp
        self.last_message_time = timestamp

    def _put_callsign(self, callsign):
        old_callsign = self.callsign
        if old_callsign != callsign:
            self.callsign = callsign

    def _put_squawk(self, squawk):
        old_squawk = self.squawk
        if old_squawk != squawk:
            self.squawk = squawk

    def track(self, message):
        time = message.timestamp()
        self._track_timestamp(time)

        position = message.position()
        if position:
            self.positions.append((time, position))

        callsign = message.callsign()
        if callsign:
            self._put_callsign(callsign)

        squawk = message.squawk()
        if squawk:
            self._put_squawk(squawk)

    def _last_position(self):
        if len(self.positions) > 0:
            return self.positions[-1]
        return None

    def __repr__(self):
        return f"""---
plane:    {self.hex_code} - {self.callsign} - {self.squawk}
times:    {self.first_message_time} - {self.last_message_time}
position: {self._last_position() or "unknown"}"""


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
