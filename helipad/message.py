import logging
import datetime

logger = logging.getLogger(__name__)

# ordered list representing the format of messages
FORMAT = [
    "type",
    "subtype",
    "session_id",
    "aircraft_id",
    "hex",
    "flight_id",
    "data_gen",
    "time_gen",
    "data_log",
    "time_log",
    "callsign",
    "alt",
    "ground_speed",
    "direction",
    "lat",
    "lon",
    "vert_rate",
    "squawk",
    "squawk_changed",
    "emergency",
    "spi",
    "on_ground",
]


# fileds that are relavant for tracking purposes
RELEVANT_FIELDS = set(
    [
        "callsign",
        "alt",
        "ground_speed",
        "direction",
        "lat",
        "lon",
        "vert_rate",
        "squawk",
        "squawk_changed",
        "emergency",
        "spi",
        "on_ground",
    ]
)


class ADSBMessage:
    def __init__(self, raw_message):
        self.raw_message = raw_message
        self.fields = parse(raw_message)

    def subtype(self):
        return int(self.fields["subtype"])

    def hex_code(self):
        return self.fields["hex"]

    def callsign(self):
        return self.fields.get("callsign")

    def squawk(self):
        return self.fields.get("squawk")

    def timestamp(self):
        return parse_time(self.fields["data_gen"], self.fields["time_gen"])

    def position(self):
        if self.fields["subtype"] == "3":
            return (
                int(self.fields["alt"]),
                float(self.fields["lat"]),
                float(self.fields["lon"]),
            )
        return None

    def direction(self):
        """
        speed - direction - vertical rate
        New message: (4, 12, 13, 16, 21)
        MSG 2025-03-26 13:53:05.899000 4 4B1A27 [(12, '302'), (13, '78'), (16, '-1728'), (21, '0\n')]

        """
        pass

    def reported_fields(self):
        return list(set(self.fields.keys()) & RELEVANT_FIELDS)

    def ignore(self):
        for function in BASIC_FILTERS:
            if function(self.fields):
                return True
        return False


def parse(message):
    segments = message.split(",")

    dict_message = {"raw": message}
    for index in range(22):
        if segments[index]:
            dict_message[FORMAT[index]] = segments[index]
    return dict_message


def parse_time(date, time):
    timestamp_format = "%Y/%m/%d%H:%M:%S.%f"
    return datetime.datetime.strptime(f"{date}{time}", timestamp_format)


# Filtering function to discard unwanted messages
# take a message and return true if the message has to be discarded


def not_msg_type_filter(message):
    """
    Log and pass messages that
    """
    if message["type"] != "MSG":
        logger.warning(f"Got an unrecognized message: {message['raw']}")
        return True
    return False


def ignore_seven_type_filter(message):
    """
    Ignore ground station message (not relevant for plane tracking)
    """
    return message["type"] == "MSG" and message["subtype"] == "7"


def unusual_ids_filter(message):
    """
    Discard and log messages with values different than the ones seen here
    """
    if (
        message["session_id"] != "111"
        or message["aircraft_id"] != "11111"
        or message["flight_id"] != "111111"
    ):
        logger.warning(f"Got message with unexpected values: {message['raw']}")
        return True
    return False


BASIC_FILTERS = [not_msg_type_filter, ignore_seven_type_filter, unusual_ids_filter]
