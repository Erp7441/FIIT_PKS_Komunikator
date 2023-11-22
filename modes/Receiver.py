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
        # self.socket.settimeout(SOCKET_TIMEOUT)  # TODO:: Remove
        self.socket.bind((ip, port))

        print_color("Waiting for connection...", color="blue")

        ###############################################
        # Receiver main loop
        ###############################################
        while True:
            ip, port, packet = self.connection_manager.await_packet()

            print_debug("Received {0} packet from {1}:{2}".format(str(packet.flags), ip, port))
            connection = self.connection_manager.get_connection(ip, port)

            # Checking if packet was not damaged and if it is a first packet then it has to be a SYN
            if packet is None or (connection is None and not packet.flags.syn):
                print_debug("Received invalid packet!")
                continue

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
        connection.add_packet(packet)
        # TODO:: Implement sending of multiple ACKs here (server)
        self.connection_manager.send_ack_packet(connection)

    @staticmethod
    def check_if_received_data_packet(packet: Packet, connection: Connection):
        return (
            packet.flags.info or packet.flags.file or packet.flags.msg
            and connection is not None and connection.state == ConnectionState.ACTIVE
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
