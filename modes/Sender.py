import socket as s

from connection.SenderConnectionManager import SenderConnectionManager
from data.Builder import disassemble
from data.Data import Data
from utils.Constants import DEFAULT_PORT, SENDER_SOCKET_TIMEOUT, GENERATE_BAD_PACKET


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT, settings: dict = None):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.settimeout(SENDER_SOCKET_TIMEOUT)  # TODO:: Reconsider this method of timeout from server side
        self.connection_manager = SenderConnectionManager(self)
        self.connection = self.establish_connection(ip, port)
        self.settings = settings  # TODO:: Implement settings
        self.generate_bad_packet = GENERATE_BAD_PACKET

    ###############################################
    # Sending
    ###############################################
    # Main sending interface method
    def send(self, data: Data):
        # Sending packets
        packets = disassemble(data)
        self.connection_manager.batch_send(packets, self.connection)
        self.close_connection()

    ###############################################
    # Connection
    ###############################################
    def establish_connection(self, ip, port):
        # Send syn packet
        # Wait for one response packet of SYN ACK
        # Send ack packet
        # Add to active connections
        if (
            self.connection_manager is not None and ip is not None and port is not None and
            self.connection_manager.get_connection(ip, port) is None
        ):
            return self.connection_manager.establish_connection(ip, port)
        return None

    def close_connection(self):
        # Send fin packet
        # Wait for one response packet of FINACK
        # Send ack packet
        # Remove connection from connections
        if (
            self.connection_manager is not None and self.connection.ip is not None and self.connection.port is not None and
            self.connection_manager.get_connection(self.connection.ip, self.connection.port) is not None
        ):
            self.connection_manager.close_connection(self.connection.ip, self.connection.port)
            self.connection = None

    def __str__(self):
        _str = "Sender:\n"
        if self.connection_manager is not None:
            _str += str(self.connection_manager) + "\n"

        _str += "Connected to:\n"
        if self.connection.ip is not None:
            _str += "IP: " + str(self.connection.ip) + "\n"
        if self.connection.port is not None:
            _str += "Port: " + str(self.connection.port) + "\n"

        if self.settings is not None:
            _str += "Settings: " + str(self.settings) + "\n"
        return _str


    # Pseudo idea
    # Receive communication from assembler
    # Create some kind of main loop like in client for data sending
    # Receive ACK per packet
    # Handle errors by resending packets
