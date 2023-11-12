import socket as s
from utils.Constants import DEFAULT_PORT
from packet.Packet import Packet


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        # self.socket.bind(('0.0.0.0', 33333))  # TODO:: Enforce client port?
        self.server = (ip, port)

    def send_packet(self, data: Packet):
        self.socket.sendto(data.encode(), self.server)