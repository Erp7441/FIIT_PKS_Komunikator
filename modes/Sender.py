import socket as s

from connection.SenderConnectionManager import SenderConnectionManager
from data.Builder import disassemble
from data.Data import Data
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT
from utils.Utils import print_debug


# Settings
# Pseudo idea
# Provides variables with settings like
# Port number
# IP address
# Segment size
# Could be aggregated inside Sender or Receiver???


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.connection_manager = SenderConnectionManager(self)
        self.ip = ip
        self.port = port
        self.establish_connection()
        self.settings = None  # TODO:: Implement settings

    def _send_packet_(self, packet: Packet):
        print_debug("Sent packet to {0}:{1} server with data: {2}".format(self.ip, self.port, packet.data))

        packet.send_to(self.ip, self.port, self.socket)
        ip, port, packet = self.connection_manager.await_packet()

        # TODO:: Implement sending of multiple ACKs here (client)
        # TODO:: How to handle faulty ACK?
        if ip != self.ip or port != self.port or not packet.flags.ack:
            connection = self.connection_manager.get_connection(self.ip, self.port)
            self.connection_manager.kill_connection(connection)

    def establish_connection(self):
        # Send syn packet
        # Wait for one response packet of SYN ACK
        # Send ack packet
        # Add to active connections
        self.connection_manager.establish_connection(self.ip, self.port)

    def close_connection(self):
        # Send fin packet
        # Wait for one response packet of FINACK
        # Send ack packet
        # Remove connection from connections
        self.connection_manager.close_connection(self.ip, self.port)

    def send(self, data: Data):
        packets = disassemble(data)
        for packet in packets:
            self._send_packet_(packet)
        self.close_connection()

    def __str__(self):
        _str = "Sender:\n"
        if self.connection_manager is not None:
            _str += str(self.connection_manager) + "\n"

        _str += "Connected to:\n"
        if self.ip is not None:
            _str += "IP: " + str(self.ip) + "\n"
        if self.port is not None:
            _str += "Port: " + str(self.port) + "\n"

        if self.settings is not None:
            _str += "Settings: " + str(self.settings) + "\n"
        return _str


    # Pseudo idea
    # Receive communication from assembler
    # Create some kind of main loop like in client for data sending
    # Receive ACK per packet
    # Handle errors by resending packets
