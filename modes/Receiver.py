import socket as s
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))

        print("Waiting for connection...")

        while True:
            data, addr = self.socket.recvfrom(1024)
            print("Connected from", addr)
            print("Received data", data)

            packet = Packet().decode(data)

            # TODO:: Wait for SYN packet to start transmitting data. If SYN is received. Send ACK, etc...
