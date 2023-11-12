import socket as s

from connection.SenderConnectionManager import SenderConnectionManager
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.connections = SenderConnectionManager(self)
        # self.socket.bind(('0.0.0.0', 33333))  # TODO:: Enforce client port?
        self.server = (ip, port)
        self.establish_connection()

    def send_packet(self, data: Packet):
        data.send_to(self.server, self.socket)

    def establish_connection(self):
        # Send syn packet
        # Wait for one response packet of SYN ACK
        # Send ack packet
        # Add to active connections
        self.connections.establish_connection(self.server[0], self.server[1])

    def close_connection(self):
        # Send fin packet
        # Wait for one response packet of FINACK
        # Send ack packet
        # Remove connection from connections
        self.connections.close_connection(self.server[0], self.server[1])

    # Pseudo idea
    # Receive communication from assembler
    # Create some kind of main loop like in client for data sending
    # Receive ACK per packet
    # Handle errors by resending packets
