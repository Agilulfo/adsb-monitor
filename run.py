import socket

import helipad.craft as c
import logging
import datetime

logger = logging.getLogger(__name__)

def timestamp():
    now = datetime.datetime.now(datetime.UTC)
    return now.strftime("%Y%m%d_%H%M%S")

def main():
    #
    # message (kinda) specs: http://woodair.net/sbs/article/barebones42_socket_data.htm
    # MSG,1 seems to have callsign
    # MSG,3 seems to have coords

    stream = StreamReader("localhost", 30003)

    handler = MessageHandler()


    with open(f"{timestamp()}_dump.txt", 'w') as dump:
        while True:
            message = stream.read_line()
            dump.write(f"{message}\n")
            dump.flush()
            handler.handle_message(message)


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
            logger.debug(f"Ignoring message of type 7")
            return
        if segments[2] != "111" or segments[3] != "11111" or segments[5] != "111111":
            logger.warning(
                f"Got a message with unexpected values in fields 3,4 or 6: {message}"
            )
            return

        timestamp_format = "%Y/%m/%d%H:%M:%S.%f"
        timestamp = datetime.datetime.strptime(f"{segments[8]}{segments[9]}", timestamp_format)
        message_type = segments[1]
        aircraft_id = segments[4]
        relevant_segments = []
        for field_index in range(10, 22):
            if segments[field_index] != "":
                relevant_segments.append((field_index, segments[field_index]))
        print(f"MSG {timestamp} {message_type} {aircraft_id} {relevant_segments}")


class StreamReader:
    def __init__(self, address, port):
        self.socket = socket.create_connection((address, port))
        self.buffer = b""

    def read_line(self):
        line = self.extract_line()

        while line is None:
            # TODO: handle socket close
            # TODO: tweak message length
            self.buffer = b"".join([self.buffer, self.socket.recv(10)])
            line = self.extract_line()
        return line.decode("utf-8")

    def extract_line(self):
        newline = b"\r\n"
        first, separator, second = self.buffer.partition(newline)
        if separator == newline:
            self.buffer = second
            return first
        return None


if __name__ == "__main__":
    main()
