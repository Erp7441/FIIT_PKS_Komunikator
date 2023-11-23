import socket as s

from connection.ConnectionState import ConnectionState
from connection.SenderConnectionManager import SenderConnectionManager
from data.Builder import disassemble
from data.Data import Data
from packet.Flags import Flags
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT, SENDER_SOCKET_TIMEOUT
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
        self._bad_packets = []

    def _send_packet_(self, packet: Packet):
        connection = self.connection_manager.get_connection(self.ip, self.port)
        if connection is None or connection.state != ConnectionState.ACTIVE:
            return False

        packet.send_to(self.ip, self.port, self.socket)

        print_debug_data("Sent packet to {0}:{1} server with data: {2}".format(self.ip, self.port, packet.data))
        ip, port, packet = self.connection_manager.await_packet(connection)

        # TODO:: Implement sending of multiple ACKs here (client)
        # TODO:: How to handle faulty ACK?
        if ip != self.ip or port != self.port or not packet.flags.ack:
            self.connection_manager.kill_connection(connection)
            return False

        if packet.flags.nack:
            print_debug("Received NACK packet from {0}:{1}".format(self.ip, self.port))
            self._bad_packets.append(packet)
        return True

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
        # Sending packets
        packets = disassemble(data)
        packet_count = len(packets)

        for i, packet in enumerate(packets):
            if self._send_packet_(packet):
                print_debug("Sending packet {0}/{1}".format(i+1, packet_count))

        self._resend_bad_packets()

        self.close_connection()

    def _resend_bad_packets(self):
        # Resending failed packets
        # TODO:: Add attempts here for safety. If over 3 failed attempts, close connection
        while len(self._bad_packets) != 0:
            info_packet = Packet(Flags(info=True, nack=True))

            # TODO:: Add attempts here for safety. If over 3 failed attempts, close connection
            while not self._send_packet_(info_packet):
                pass

            bad_packets = self._bad_packets
            self._bad_packets = []
            for packet in bad_packets:
                if self._send_packet_(packet):
                    print_debug("Resending packet {0}".format(packet.seq))

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
