import socket

def main():
    connection = socket.create_connection(("localhost", 30003))
    while True:
        print (connection.recvmsg(100))


if __name__ == "__main__":
    main()
