import helipad.config.logging
from helipad.streams import StreamReader
from helipad.handlers import MessageHandler, DumpHandler

helipad.config.logging.init_logging()


def main():
    stream = StreamReader("localhost", 30003)

    handlers = [DumpHandler(), MessageHandler()]

    while True:
        message = stream.read_line()
        for handler in handlers:
            handler.handle_message(message)


if __name__ == "__main__":
    main()
