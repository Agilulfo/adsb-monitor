import logging
import datetime

logger = logging.getLogger(__name__)


class MessageHandler:
    def __init__(self):
        self.aircrafts = dict()

    def handle_message(self, message):
        segments = message.split(",")

        # filter out unexpected messagges
        if segments[0] != "MSG":
            logger.warning(f"Got an unrecognized message: {message}")
            return
        if segments[1] == "7":
            logger.debug("Ignoring message of type 7")
            return
        if segments[2] != "111" or segments[3] != "11111" or segments[5] != "111111":
            logger.warning(
                f"Got a message with unexpected values in fields 3,4 or 6: {message}"
            )
            return

        timestamp_format = "%Y/%m/%d%H:%M:%S.%f"
        timestamp = datetime.datetime.strptime(
            f"{segments[8]}{segments[9]}", timestamp_format
        )
        message_type = segments[1]
        aircraft_id = segments[4]
        relevant_segments = []
        for field_index in range(10, 22):
            if segments[field_index] != "":
                relevant_segments.append((field_index, segments[field_index]))
        print(f"MSG {timestamp} {message_type} {aircraft_id} {relevant_segments}")


class DumpHandler:
    def __init__(self, filename=None):
        self.dump_file = open(filename or self.__class__.default_filename(), "w", buffering=1)

    def default_filename():
        now = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d_%H%M%S")
        return f"{now}_dump.txt"

    def handle_message(self, message):
        self.dump_file.write(f"{message}\n")

