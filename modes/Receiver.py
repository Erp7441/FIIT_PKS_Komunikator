import socket as s

from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from connection.ReceiverConnectionManager import ReceiverConnectionManager
from data.Builder import assemble
from data.File import File
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT
from utils.Utils import print_debug, print_color


# TODO:: Implement Selective repeat ARQ
# 1. Send X packets at once from client (add number of expected packets to INFO packet?).
# 2. Await X packets on server.
# 3. If one packet is broken. Take its order number (maybe SEQ but could be broken at this point) write it down to a bad packets list and send N
# 4. Client will receive NACK and write down which packet broken
# 5. After the communication ends (this needs to be done before fin ack). Await N wrong packets on server side
# 6. After the communication ends (this needs to be done before fin ack). Send N wrong packets back to the server.


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0", settings: dict = None):
        self.connection_manager = ReceiverConnectionManager(self)
        self.ip = ip,
        self.port = port
        self.settings = settings  # TODO:: Implement settings

        # Socket initialization
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))

        print_color("Waiting for connection...", color="blue")

        ###############################################
        # Receiver main loop
        ###############################################
        while True:
            # Handling first packet of the batch
            ip, port, packet = self.connection_manager.await_packet()
            connection = self.connection_manager.get_connection(ip, port)

            # Debug output (TODO:: Remove?)
            if packet is not None:
                print_debug("Received a packet with flags {0} from {1}:{2}".format(str(packet.flags), ip, port))
            else:
                print_debug("Received a broken packet from {0}:{1}!".format(ip, port))

            # If the batch size is bigger than one. Handle the rest of the packets.
            if (
                connection is not None and connection.batch_size > 1
                and self.check_if_received_data_packet(packet, connection)
            ):
                self.handle_multiple_packets(packet, connection)
            else:
                self.handle_single_packet(ip, port, packet, connection)

    ###############################################
    # Handle packets from client
    ###############################################
    def handle_single_packet(self, ip: str, port: int, packet: Packet, connection: Connection = None):

        # Checking if packet was damaged. If so, write its order number to the list of bad packets
        if packet is None:
            print_debug("Received broken packet!")
            if connection is not None:
                self.connection_manager.send_nack_packet(connection)
                connection.bad_packets_count += 1
            return

        # Checking if first packet is SYN
        if connection is None and not packet.flags.syn:
            print_debug("Received invalid packet!")
            return

        # Begin establishing connection
        if packet.flags.syn and connection is None:
            self.connection_manager.start_establish_connection(packet, ip, port)
        # Begin refreshing connection
        elif packet.flags.syn and connection is not None:
            print_debug("Received SYN packet from {0}:{1}. Refreshing connection...".format(connection.ip, connection.port))
            self.connection_manager.refresh_keepalive(connection)

        # Receive ACK from client
        elif packet.flags.ack and connection is not None:
            self.received_ack(packet, connection)

        # Received data packet
        elif Receiver.check_if_received_data_packet(packet, connection):
            self.received_data(packet, connection)

        # Closing connection
        elif packet.flags.fin and connection is not None and connection.state == ConnectionState.ACTIVE:
            self.connection_manager.start_closing_connection(packet, connection)

    def handle_multiple_packets(self, first_packet, connection):
        if first_packet is None:
            print_debug(
                "Received broken first packet of the batch! From {0}:{1}".format(connection.ip, connection.port),
                color="orange"
            )

        packets = [first_packet]
        if first_packet is not None and first_packet.flags.fin:
            print_debug("Handling last data packet", color="cyan")
            self.handle_single_packet(connection.ip, connection.port, first_packet, connection)
            print_debug("Handled last data packet", color="cyan")
            return

        print_debug("Awaiting {0} more packets from {1}:{2}".format(connection.batch_size - 1, connection.ip, connection.port))
        for _ in range(connection.batch_size - 1):
            ip, port, packet = self.connection_manager.await_packet()

            if packet is None:
                packets.append(None)
                continue

            print_debug("Received {0} packet from {1}:{2}".format(str(packet.flags), ip, port))
            if ip != connection.ip or port != connection.port:
                print_debug("Packet from {0}:{1} is not from {2}:{3}".format(ip, port, connection.ip, connection.port))
                return None

            packets.append(packet)
            if packet.flags.fin:
                break

        for i, packet in enumerate(packets):
            print_debug("Handling packet {0}".format(i), color="cyan")
            self.handle_single_packet(connection.ip, connection.port, packet, connection)
            print_debug("Handled packet {0}".format(i), color="cyan")

    ###############################################
    # Received ACK from client
    ###############################################
    def received_ack(self, packet: Packet, connection: Connection):
        # For establishing connection
        if connection.state == ConnectionState.SYN_ACK_SENT:
            self.connection_manager.finish_establish_connection(packet, connection)
            print_color("Connection with", str(connection.ip)+":"+str(connection.port), "established", color='green')
        # For terminating connection
        elif connection.state == ConnectionState.FIN_ACK_SENT:
            ip, port = connection.ip, connection.port
            self.connection_manager.finish_closing_connection(packet, connection)
            print_color("Connection with", str(ip)+":"+str(port), "closed", color="green")

            Receiver.reassemble_and_output_data(connection)

    ###############################################
    # Received data packet from client
    ###############################################
    def received_data(self, packet: Packet, connection: Connection):
        print_debug("Received DATA packet from {0}:{1}".format(connection.ip, connection.port))
        self.connection_manager.send_ack_packet(connection, packet.seq)

        connection.add_packet(packet)
        if packet.flags.fin and (packet.flags.file or packet.flags.msg) and connection.bad_packets_count > 0:
            self.connection_manager.receive_resent_packets(connection)

        # TODO:: Implement sending of multiple ACKs here (server)

    @staticmethod
    def check_if_received_data_packet(packet: Packet, connection: Connection):
        return (
            packet is not None and (packet.flags.info or packet.flags.file or packet.flags.msg
            and connection is not None and connection.state == ConnectionState.ACTIVE)
        )

    @staticmethod
    def reassemble_and_output_data(connection: Connection):
        data = assemble(connection.packets)

        if isinstance(data, File):
            data.save("C:\\Users\\Martin\\Downloads")  # TODO:: Move path to settings
        else:
            print_color(str(data), color="blue")

    def __str__(self):
        _str = "Receiver:\n"
        if self.connection_manager is not None:
            _str += str(self.connection_manager)

        if self.ip is not None:
            _str += "IP: " + str(self.ip) + "\n"
        if self.port is not None:
            _str += "Port: " + str(self.port) + "\n"

        if self.settings is not None:
            _str += "Settings: " + str(self.settings) + "\n"
        return _str
