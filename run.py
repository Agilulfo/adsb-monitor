import socket

import helipad.craft as c


def main():
    stream = StreamReader("localhost", 30003)

    while True:
        print(stream.read_line())
    # planes = {}

    # while True:
    #     message = stream.read_line()
    #     message_sections = message.split(',')

    #     if message_sections[0] != "MSG":
    #         print(f"interesting... got: {message}")


class StreamReader:
    def __init__(self, address, port):
        self.socket = socket.create_connection((address, port))
        self.buffer = b""

    def read_line(self):
        line = self.extract_line()

        while line is None:
            # TODO: handle socket close
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
