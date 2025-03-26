import socket


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


class FileReader:
    def __init__(self, filename):
        self.source = open(filename)

    def read_line(self):
        line = self.source.readline()
        if line == "":
            raise Exception("EOF")
        return line
