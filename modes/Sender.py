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
        self._connection = None
        self.establish_connection(ip, port)
        self.settings = settings  # TODO:: Implement settings
        self._bad_packets = []

    def _send_packet_(self, packet: Packet):
        if self._connection is None or self._connection.state != ConnectionState.ACTIVE:
            return False

        packet.send_to(self._connection.ip, self._connection.port, self.socket)

        print_debug_data("Sent packet to {0}:{1} server with data: {2}".format(self._connection.ip, self._connection.port, packet.data))

    def _await_ack_for_data(self):
        with self.connection_manager.lock:
            ip, port, packet = self.connection_manager.await_packet(self._connection)

            # TODO:: Implement sending of multiple ACKs here (client)
            # TODO:: How to handle faulty ACK?
            if ip != self._connection.ip or port != self._connection.port or packet is None or not packet.flags.ack:
                self.connection_manager.kill_connection(self._connection)
                self._connection = None
                return None

            if packet.flags.nack:
                print_debug("Received NACK packet from {0}:{1}".format(self._connection.ip, self._connection.port))
                self._bad_packets.append(packet)
            return packet

    def establish_connection(self, ip, port):
        # Send syn packet
        # Wait for one response packet of SYN ACK
        # Send ack packet
        # Add to active connections
        if (
            self.connection_manager is not None and ip is not None and port is not None and
            self.connection_manager.get_connection(ip, port) is None
        ):
            self._connection = self.connection_manager.establish_connection(ip, port)

    def close_connection(self):
        # Send fin packet
        # Wait for one response packet of FINACK
        # Send ack packet
        # Remove connection from connections
        if (
            self.connection_manager is not None and self._connection.ip is not None and self._connection.port is not None and
            self.connection_manager.get_connection(self._connection.ip, self._connection.port) is not None
        ):
            self.connection_manager.close_connection(self._connection.ip, self._connection.port)
            self._connection = None

    def _batch_send(self, packets: list[Packet]):
        packet_count = len(packets)

        k = 0
        for _ in range(0, len(packets), self._connection.batch_size):
            sent_packets_this_batch = 0
            for _ in range(self._connection.batch_size):
                if k >= packet_count:
                    break
                self._send_packet_(packets[k])
                print_debug("Sending packet {0}/{1}".format(k+1, packet_count))
                k += 1
                sent_packets_this_batch += 1

            for j in range(sent_packets_this_batch):
                ack_packet = self._await_ack_for_data()
                print_debug("ACK with SEQ value {0} received".format(ack_packet.seq))
                if ack_packet is None or ack_packet.seq != packets[k - sent_packets_this_batch + j].seq:
                    print_debug("Broken or incorrect ACK packet received!", color="orange")

    def send(self, data: Data):
        # Sending packets
        packets = disassemble(data)
        self._batch_send(packets)
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
            self._batch_send(bad_packets)

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
