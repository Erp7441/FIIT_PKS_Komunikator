import socket as s

from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from connection.ReceiverConnectionManager import ReceiverConnectionManager
from packet.Packet import Packet
from utils.Constants import DEFAULT_PORT
from utils.Utils import print_debug


# TODO:: If first data packet is not INFO kill connection

# Settings
# Pseudo idea
# Provides variables with settings like
# Port number
# IP address
# Segment size
# Could be aggregated inside Sender or Receiver???

# Pseudo idea
# 1. Create communication object
# 2. Handle opening of communication
# if successful add it ot connection manager
# 3. Receive INFO
# 4. Setup communication according to the info
# 5. Receive DATA packets
# 6. Handle DATA packets in communication
# 7. Receive FIN
# 8. Close connection

class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.connection_manager = ReceiverConnectionManager(self)
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.settings = None  # TODO:: Implement

        print("Waiting for connection...")

        ###############################################
        # Receiver main loop
        ###############################################
        while True:
            ip, port, packet = self.connection_manager.await_packet()
            print_debug("Received packet from {0}:{1}".format(ip, port))
            connection = self.connection_manager.get_connection(ip, port)

            # Begin establishing connection
            if packet.flags.syn and connection is None:
                self.connection_manager.start_establish_connection(packet, ip, port)
            # Begin refreshing connection
            elif packet.flags.syn and connection is not None:
                self.connection_manager.refresh_keepalive(connection)

            # Receive ACK from client
            if packet.flags.ack and connection is not None:
                self.received_ack(packet, connection)

            # Received data packet
            if Receiver.check_if_received_data_packet(packet, connection):
                self.received_data(packet, connection)

            # Closing connection
            if packet.flags.fin and connection is not None and connection.state == ConnectionState.ACTIVE:
                self.connection_manager.start_closing_connection(packet, connection)

    ###############################################
    # Received ACK from client
    ###############################################
    def received_ack(self, packet: Packet, connection: Connection):
        print_debug("Received ACK packet from {0}:{1} client".format(connection.ip, connection.port))

        # For establishing connection
        if connection.state == ConnectionState.SYN_ACK_SENT:
            self.connection_manager.finish_establish_connection(packet, connection)
            print("Connection with", str(connection.ip)+":"+str(connection.port), "established")
        # For terminating connection
        elif connection.state == ConnectionState.FIN_ACK_SENT:
            ip, port = connection.ip, connection.port
            self.connection_manager.finish_closing_connection(packet, connection)
            print("Connection with", str(ip)+":"+str(port), "closed")
        # For refreshing connection
        elif connection.state == ConnectionState.REFRESHING:
            self.connection_manager.send_ack_packet(connection)
            print("Connection with", str(connection.ip)+":"+str(connection.port), "refreshed")

    ###############################################
    # Received data packet from client
    ###############################################
    def received_data(self, packet: Packet, connection: Connection):
        connection.keepalive_event.wait(connection.keepalive_time)
        print_debug("Received DATA packet from {0}:{1} client".format(connection.ip, connection.port))
        connection.add_packet(packet)
        print_debug("Sent ACK packet to {0}:{1} client".format(connection.ip, connection.port))
        self.connection_manager.send_ack_packet(connection)

    @staticmethod
    def check_if_received_data_packet(packet: Packet, connection: Connection):
        return (
            packet.flags.info or packet.flags.file or packet.flags.msg
            and connection is not None and connection.state == ConnectionState.ACTIVE
        )