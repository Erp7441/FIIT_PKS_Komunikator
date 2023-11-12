import socket as s
from utils.Constants import DEFAULT_PORT


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.bind((ip, port))
        self.socket.listen(1)

        print("Waiting for connection...")

        while True:
            conn, addr = self.socket.accept()
            print("Connected from", addr)

            # TODO:: Wait for SYN packet to start transmitting data. If SYN is received. Send ACK, etc...

            conn.close()
