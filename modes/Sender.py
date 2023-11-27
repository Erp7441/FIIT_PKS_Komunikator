import socket as s
from time import sleep

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
        self.settings = settings
        self.establish_connection()

    def establish_connection(self):
        if (
            self.connection_manager is not None and self.ip is not None and self.port is not None and
            self.get_current_connection() is None
        ):
            self.connection_manager.establish_connection(self.ip, self.port)

    def close_connection(self):
        if (
            self.connection_manager is not None and self.ip is not None and self.port is not None and
            self.get_current_connection() is not None
        ):
            self.connection_manager.close_connection(self.ip, self.port)

    def send(self, data: Data):
        connection = self.get_current_connection()
        if connection is None:
            print_debug("No connection to send data to", color="orange")
            return

        stopped = False
        dead = False

        packets = disassemble(data)
        for i, packet in enumerate(packets):

            # If connection is dead, return
            if dead:
                return

            # Stop sending while connection is not active
            while connection.state != ConnectionState.ACTIVE:
                stopped = True
                # If connection was killed while waiting for it to become active, break waiting loop and mark it as dead
                if connection.state == ConnectionState.CLOSED or connection.state == ConnectionState.RESET:
                    dead = True
                    break
                sleep(1)

            # If we were stopped in previous iteration, send the last packet again
            if stopped:
                self.connection_manager.send_data_packet(connection, packets[i-1])
                stopped = False

            self.connection_manager.send_data_packet(connection, packet)
        self.close_connection()  # Closing connection upon sending all the data so the server may assemble them
        self.establish_connection()  # Reestablishing connection for sending more data

    def send_file(self, path: str = None):
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

    def close(self):
        print_debug("Exiting sender...")
        self.close_connection()
        self.socket.shutdown(s.SHUT_RDWR)
        self.socket.close()

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

    def get_current_connection(self):
        if self.connection_manager is not None:
            return self.connection_manager.get_connection(self.ip, self.port)

    def swap_roles(self):
        connection = self.get_current_connection()

        swp_packet = Segment()
        swp_packet.flags.swp = True
        client_info_packet = Segment(data=self.settings.encode())
        client_info_packet.flags.info = True

        with self.connection_manager.lock:
            # Sending SWP Received ACK
            if self.connection_manager.send_data_packet(connection, swp_packet) is True:
                # Sending settings Received ACK
                if self.connection_manager.send_data_packet(connection, client_info_packet) is True:
                    # Receive server settings
                    _, _, packet = self.connection_manager.await_packet()

                    # Send ACK for server settings
                    self.connection_manager.send_ack_packet(connection)

                    # Decode server settings and swap roles
                    if packet is not None and packet.flags.info:
                        settings = Settings().decode(packet.data)

                        self.connection_manager.kill_connection(connection)
                        self.close()

                        from cli.MenuSystem import run_receiver_mode
                        run_receiver_mode(settings)  # Start server mode

                        print_debug("Exiting from SWP (Sender)...")

            self.connection_manager.kill_connection(connection)
