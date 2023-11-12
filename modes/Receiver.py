import socket as s
from packet.Packet import Packet
from data.File import File
from utils.Constants import DEFAULT_PORT, MTU


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))

        print("Waiting for connection...")

        while True:
            data, addr = self.socket.recvfrom(MTU)
            print("Connected from", addr)
            print("Received data", data)

            # TODO REMOVE THIS TEST
            packet = Packet().decode(data)
            file = File().decode(packet.data)
            file.save("C:/Users/Martin/Downloads")
            pass
            # TODO:: Wait for SYN packet to start transmitting data. If SYN is received. Send ACK, etc...
