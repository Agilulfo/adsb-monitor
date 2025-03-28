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

# handlers


class FootprintDetector:
    def __init__(self):
        self.filters = BASIC_FILTERS
        self.seen_messages = set()

    def run_filters(self, message):
        for function in self.filters:
            if function(message):
                return True
        return False

    def handle_message(self, message):
        message = parse(message)

        if self.run_filters(message):
            return

        # build message footprint
        reported_fields = list(set(message.keys()) & RELEVANT_FIELDS)
        footprint = tuple([int(message["subtype"])] + reported_fields)

        # detect new footprints
        if footprint not in self.seen_messages:
            self.seen_messages.add(footprint)
            print(f"New message: {footprint} - {message['raw']}")


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
