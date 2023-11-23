import socket as s

from connection.ConnectionState import ConnectionState
from connection.SenderConnectionManager import SenderConnectionManager
from data.Builder import disassemble
from data.Data import Data
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT, SENDER_SOCKET_TIMEOUT, RESEND_ATTEMPTS, SENDER_BAD_PACKETS_SEQ, \
    SENDER_BAD_PACKETS_ATTEMPTS
from utils.Utils import print_debug, print_debug_data


class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT, settings: dict = None):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.settimeout(SENDER_SOCKET_TIMEOUT)  # TODO:: Reconsider this method of timeout from server side
        self.connection_manager = SenderConnectionManager(self)
        self.ip = ip
        self.port = port
        self.establish_connection()
        self.settings = settings  # TODO:: Implement settings

    def _send_packet_(self, packet: Packet):
        connection = self.connection_manager.get_connection(self.ip, self.port)
        if connection is None or connection.state != ConnectionState.ACTIVE:
            return None

        for attempt in range(RESEND_ATTEMPTS):
            if packet.seq in SENDER_BAD_PACKETS_SEQ and attempt < SENDER_BAD_PACKETS_ATTEMPTS-1:
                packet.send_to_with_error(self.ip, self.port, self.socket)
            elif packet.seq in SENDER_BAD_PACKETS_SEQ:
                SENDER_BAD_PACKETS_SEQ.remove(packet.seq)
                packet.send_to(self.ip, self.port, self.socket)
            else:
                packet.send_to(self.ip, self.port, self.socket)

            print_debug("Sent packet SEQ {0} to {1}:{2} server (attempt {3})".format(packet.seq, self.ip, self.port, attempt+1))
            ip, port, response = self.connection_manager.await_packet(connection)  # Awaiting ACK

            # TODO:: Implement sending of multiple ACKs here (client)
            # TODO:: How to handle faulty ACK?
            if ip != self.ip or port != self.port:
                break

            if response.flags.ack:
                return True  # If we received ACK, success
            elif response.flags.nack:
                continue  # If we received NACK, retry
            else:
                break  # If we received something else stop.

        self.connection_manager.kill_connection(connection)
        return None

    def establish_connection(self):
        # Send syn packet
        # Wait for one response packet of SYN ACK
        # Send ack packet
        # Add to active connections
        if (
            self.connection_manager is not None and self.ip is not None and self.port is not None and
            self.connection_manager.get_connection(self.ip, self.port) is None
        ):
            self.connection_manager.establish_connection(self.ip, self.port)

    def close_connection(self):
        # Send fin packet
        # Wait for one response packet of FINACK
        # Send ack packet
        # Remove connection from connections
        if (
            self.connection_manager is not None and self.ip is not None and self.port is not None and
            self.connection_manager.get_connection(self.ip, self.port) is not None
        ):
            self.connection_manager.close_connection(self.ip, self.port)

    def send(self, data: Data):
        packets = disassemble(data)
        packet_count = len(packets)
        for i, packet in enumerate(packets):
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
