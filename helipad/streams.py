import socket
import logging
from time import sleep

logger = logging.getLogger(__name__)


class StreamReader:
    def __init__(self, address, port):
        self.address = (address, port)
        self._connect_socket()
        self.buffer = b""

    def _connect_socket(self):
        logger.info(f"Connecting to: {self.address}")

        self.socket = None
        while self.socket is None:
            try:
                self.socket = socket.create_connection(self.address)
            except ConnectionRefusedError:
                logger.warning(f"Failed connection to: {self.address}, retrying soon")
                sleep(5)

        logger.info(f"Connected to: {self.address}")

    def read_line(self):
        line = self._extract_line()

        while line is None:
            self.buffer = b"".join([self.buffer, self._read_from_socket()])
            line = self._extract_line()

        return line.decode("utf-8")

    def _read_from_socket(self):
        message = self.socket.recv(200)

        # handle socket disconnection
        if message == b"":
            logging.warning(f"Socket: {self.address} disconnected")
            self._connect_socket()
            message = self.socket.recv(200)

        return message

    def _extract_line(self):
        newline = b"\r\n"
        first, separator, second = self.buffer.partition(newline)
        if separator == newline:
            self.buffer = second
            return first
        return None


class FileReader:
    def __init__(self, filename):
        self.source = open(filename)

    def read_line(self):
        line = self.source.readline()
        if line == "":
            raise Exception("EOF")
        return line
