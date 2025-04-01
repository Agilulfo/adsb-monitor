import argparse
import helipad.config.logging as app_logging
import helipad.config

from helipad.streams import StreamReader, FileReader
from helipad.handlers import FootprintDetector, DumpHandler, AirTracking
from helipad.message import ADSBMessage
from helipad.poi import load_pois

app_logging.init_logging()


def init_parser():
    parser = argparse.ArgumentParser()

    # source options
    parser.add_argument(
        "-p", "--port", type=int, help="port for the socket", default=30003
    )
    parser.add_argument(
        "-H", "--host", help="address for the socket", default="localhost"
    )
    parser.add_argument("-f", "--fromfile", help="load data from dumpfile")

    # dump creation options
    parser.add_argument("-d", "--dump", help="produce a dump file", action="store_true")
    parser.add_argument("-D", "--dumpto", help="produce a dump to a specific file")

    return parser


def main():
    # parse CLI arguments
    parser = init_parser()
    args = parser.parse_args()

    # Load configuration
    config = helipad.config.from_file("config.yaml")
    load_pois(config["poi"])

    # Pick stream
    stream = None
    if args.fromfile:
        stream = FileReader(args.fromfile)
    else:
        stream = StreamReader(args.host, args.port)

    # build handlers
    handlers = []

    # optional handlers
    if args.dump or args.dumpto:
        handlers.append(DumpHandler(args.dumpto))

    # mandatory handlers
    handlers.append(FootprintDetector())
    # handlers.append(AirTracking())

    # main loop
    while True:
        message = ADSBMessage(stream.read_line())
        if not message.ignore():
            for handler in handlers:
                handler.handle_message(message)


if __name__ == "__main__":
    main()
