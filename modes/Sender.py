import socket as s
from utils.Constants import DEFAULT_PORT
from packet.Packet import Packet
from utils.Coder import encode_str_to_bytes


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        # self.socket.bind(('0.0.0.0', 33333))  # TODO:: Enforce client port?
        self.server = (ip, port)

    def send_packet(self, data: Packet):
        encoded_data_string = data.encode()
        encoded_data_bytes = encode_str_to_bytes(encoded_data_string)
        self.socket.sendto(encoded_data_bytes, self.server)

    # Pseudo idea
    # Receive communication from assembler
    # Create some kind of main loop like in client for data sending
    # Receive ACK per packet
    # Handle errors by resending packets
