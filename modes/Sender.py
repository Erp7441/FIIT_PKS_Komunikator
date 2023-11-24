import socket as s

from cli.Settings import Settings
from connection.ConnectionState import ConnectionState
from connection.manager.SenderConnectionManager import SenderConnectionManager
from data.Builder import disassemble
from data.Data import Data
from data.File import File
from packet.Segment import Segment
from utils.Constants import DEFAULT_PORT, SENDER_SOCKET_TIMEOUT
from utils.Utils import print_debug, get_string_safely


class Sender:
    def __init__(self, ip: str = None, port: int = DEFAULT_PORT, settings: Settings = None):
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.settimeout(SENDER_SOCKET_TIMEOUT)
        self.connection_manager = SenderConnectionManager(self)
        self.ip = ip if settings is None else settings.ip
        self.port = port if settings is None else settings.port
        self.establish_connection()
        self.settings = settings

    def _send_packet(self, packet: Segment):
        connection = self.connection_manager.get_connection(self.ip, self.port)
        if connection is None or connection.state != ConnectionState.ACTIVE:
            return None

        bad_packets_seq = self.settings.bad_packets_seq
        for attempt in range(self.settings.packet_resend_attempts):

            if packet.seq in bad_packets_seq and attempt < self.settings.bad_packets_attempts-1:
                packet.send_to_with_error(self.ip, self.port, self.socket)

            elif packet.seq in bad_packets_seq:
                bad_packets_seq.remove(packet.seq)
                packet.send_to(self.ip, self.port, self.socket)

            else:
                packet.send_to(self.ip, self.port, self.socket)

            print_debug("Sent packet SEQ {0} to {1}:{2} server (attempt {3})".format(packet.seq, self.ip, self.port, attempt+1))
            ip, port, response = self.connection_manager.await_packet(connection)  # Awaiting ACK

            # TODO:: Implement sending of multiple ACKs here (client)
            # TODO:: How to handle faulty ACK? Not sure, can rensend? If server detects duplicate. Resend ack but not append?
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
        for i, packet in enumerate(packets):
            self._send_packet(packet)

        self.close_connection()

    def send_file(self, path: str = None):
        # TODO:: Add  check for active connection to send methods
        if path is None:
            data = File(select=True)
        else:
            data = File(path=path)
        self.send(data)

    def send_message(self, message: str = None):
        if message is None:
            message = get_string_safely("Enter message: ", error_msg="Invalid message")
        data = Data(message)
        self.send(data)

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
