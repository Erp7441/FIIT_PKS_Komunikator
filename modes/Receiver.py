import socket as s
from threading import Thread
from time import sleep

from keyboard import is_pressed

from cli.Settings import Settings
from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from connection.manager.ReceiverConnectionManager import ReceiverConnectionManager
from data.Builder import assemble
from data.File import File
from packet.Segment import Segment
from utils.Constants import DEFAULT_PORT
from utils.Utils import print_debug, print_color


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0", settings: Settings = None):
        self.connection_manager = ReceiverConnectionManager(self)
        self.ip = ip if settings is None else settings.ip
        self.port = port if settings is None else settings.port
        self.settings = settings  # TODO:: BIG Implement settings into receiver

        # Socket initialization
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))
        self.socket_closed = False  # Flag to check if socket is closed
        self.thread = Thread(target=self.run)
        self.thread.start()  # Running on a separate thread

        # When user presses esc then kill the thread
        while True:
            sleep(1)  # Slows down the loop
            if is_pressed("esc"):
                print_color("Exiting receiver...", color="blue")
                self.close()
                break

    def run(self):
        if self.settings is not None:
            print(self.settings)

        print_color("Waiting for connection...", color="blue")

        # Receiver main loop
        while True:
            # Receiving packet from client
            ip, port, packet = self.connection_manager.await_packet()
            connection = self.connection_manager.get_connection(ip, port)

            # Socket was closed. Exiting main loop
            if self.socket_closed:
                break

            # Debug output
            if packet is None:
                print_debug("Received broken packet from {0}:{1}".format(ip, port))
            else:
                print_debug("Received {0} packet from {1}:{2}".format(str(packet.flags), ip, port))

            # Checking if packet was not damaged and if it is a first packet then it has to be a SYN
            if packet is None or (connection is None and not packet.flags.syn):
                self.connection_manager.send_nack_packet(connection)
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
            elif (
                packet.flags.info or packet.flags.file or packet.flags.msg
                and connection is not None and connection.state == ConnectionState.ACTIVE
            ):
                self.received_data(packet, connection)

            # Closing connection
            elif packet.flags.fin and connection is not None and connection.state == ConnectionState.ACTIVE:
                self.connection_manager.start_closing_connection(packet, connection)

    # Received ACK from client
    def received_ack(self, packet: Segment, connection: Connection):
        # For establishing connection
        if connection.state == ConnectionState.SYN_ACK_SENT:
            self.connection_manager.finish_establish_connection(packet, connection)
            print_color("Connection with", str(connection.ip)+":"+str(connection.port), "established", color='green')
        # For terminating connection
        elif connection.state == ConnectionState.FIN_ACK_SENT:
            ip, port = connection.ip, connection.port
            self.connection_manager.finish_closing_connection(packet, connection)
            print_color("Connection with", str(ip)+":"+str(port), "closed", color="green")

            if connection.packets is not None and len(connection.packets) > 1:
                self.reassemble_and_output_data(connection)
            else:
                print_color("No data received from {0}:{1}".format(ip, port), color="blue")

    # Received data packet from client
    def received_data(self, packet: Segment, connection: Connection):
        print_debug("Received DATA packet from {0}:{1}".format(connection.ip, connection.port))
        connection.add_packet(packet)
        # TODO:: Implement sending of multiple ACKs here (server)
        self.connection_manager.send_ack_packet(connection)

    # Build data using builder function and output them to the system
    def reassemble_and_output_data(self, connection: Connection):
        data = assemble(connection.packets)

        # TODO:: Check if download dir is present if not download it to user directory or to current directory
        # TODO:: Check if settings exists?
        if isinstance(data, File):
            data.save(self.settings.downloads_dir)
        else:
            print_color(str(data), color="blue")

    def close(self):
        self.socket.shutdown(s.SHUT_RDWR)
        self.socket_closed = True
        self.socket.close()
        self.thread.join(timeout=0)

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
