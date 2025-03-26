import logging
import datetime

import helipad.config.logging
from helipad.streams import StreamReader
from helipad.handlers import MessageHandler

helipad.config.logging.init_logging()
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

    with open(f"{timestamp()}_dump.txt", "w") as dump:
        while True:
            message = stream.read_line()
            dump.write(f"{message}\n")
            dump.flush()
            handler.handle_message(message)


if __name__ == "__main__":
    main()
