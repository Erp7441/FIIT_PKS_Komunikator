import os
import signal
import threading

from cli.Settings import Settings
from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from packet.Segment import Segment
from utils.Constants import MTU
from utils.Utils import print_debug


###############################################
# Connection manager handles everything about
# connections. How to establish connections,
# keep them alive and close them as well as
# sending and receiving packets from hosts.
###############################################


class ConnectionManager:
    def __init__(self, parent):
        self.active_connections = []
        self.inactive_connections = []
        self.parent = parent
        self.lock = threading.Lock()

    ###############################################
    # Connection
    ###############################################
    def get_connection(self, ip: str, port: int):
        if ip is None or port is None:
            return None

        # Searches for connections in all lists
        for connection in self.inactive_connections + self.active_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        return None

    def remove_connection(self, connection: Connection):
        if connection is None:
            print_debug("Connection does not exist!")
            return

        connection.keepalive_thread.stop()  # Stop keepalive thread

        # Remove connection from lists
        if connection in self.inactive_connections:
            self.inactive_connections.remove(connection)
        elif connection in self.active_connections:
            self.active_connections.remove(connection)

        # Mark connection as closed
        connection.state = ConnectionState.CLOSED
        print_debug("Connection with", connection.ip+":"+str(connection.port), "was removed!")

    def kill_connection(self, connection: Connection):
        if connection.state == ConnectionState.CLOSED or connection.state == ConnectionState.RESET:
            print_debug("Connection with", connection.ip+":"+str(connection.port), "is already dead!")
            return

        # Sends RST packet to the other end so signalize connection termination
        self.send_rst_packet(connection)
        connection.state = ConnectionState.RESET
        self.remove_connection(connection)
        print_debug("Connection with", connection.ip+":"+str(connection.port), "was killed!")

    def move_connection_to_active(self, connection: Connection):
        if connection in self.inactive_connections:
            self.inactive_connections.remove(connection)
            self.active_connections.append(connection)

    def move_connection_to_inactive(self, connection: Connection):
        if connection in self.active_connections:
            self.active_connections.remove(connection)
            self.inactive_connections.append(connection)

    ###############################################
    # Send packet (types)
    ###############################################
    def send_syn_packet(self, connection: Connection):
        syn_packet = Segment()
        syn_packet.flags.syn = True
        syn_packet.send_to(connection.ip, connection.port, self.parent.socket)
        connection.state = ConnectionState.SYN_SENT
        print_debug("Sent SYN packet to {0}:{1}".format(connection.ip, connection.port))
        return syn_packet

    def send_fin_packet(self, connection: Connection):
        fin_packet = Segment()
        fin_packet.flags.fin = True
        fin_packet.send_to(connection.ip, connection.port, self.parent.socket)
        connection.state = ConnectionState.FIN_SENT
        print_debug("Sent FIN packet to {0}:{1}".format(connection.ip, connection.port))
        return fin_packet

    def send_syn_ack_packet(self, connection: Connection, swap: bool = False):
        syn_ack_packet = Segment()
        syn_ack_packet.flags.syn = True
        syn_ack_packet.flags.ack = True
        syn_ack_packet.flags.swp = swap
        syn_ack_packet.send_to(connection.ip, connection.port, self.parent.socket)
        connection.state = ConnectionState.SYN_ACK_SENT
        print_debug("Sent SYN-ACK packet to {0}:{1}".format(connection.ip, connection.port))
        return syn_ack_packet

    def send_fin_ack_packet(self, connection: Connection):
        fin_ack_packet = Segment()
        fin_ack_packet.flags.fin = True
        fin_ack_packet.flags.ack = True
        fin_ack_packet.send_to(connection.ip, connection.port, self.parent.socket)
        connection.state = ConnectionState.FIN_ACK_SENT
        print_debug("Sent FIN-ACK packet to {0}:{1}".format(connection.ip, connection.port))
        return fin_ack_packet

    def send_ack_packet(self, connection, seq: int = 0):
        ack_packet = Segment(seq=seq)
        ack_packet.flags.ack = True
        ack_packet.send_to(connection.ip, connection.port, self.parent.socket)
        print_debug("Sent ACK packet to {0}:{1}".format(connection.ip, connection.port))
        return ack_packet

    def send_nack_packet(self, connection):
        nack_packet = Segment()
        nack_packet.flags.nack = True
        nack_packet.send_to(connection.ip, connection.port, self.parent.socket)
        print_debug("Sent NACK packet to {0}:{1}".format(connection.ip, connection.port))
        return nack_packet

    def send_rst_packet(self, connection):
        rst_packet = Segment()
        rst_packet.flags.rst = True
        rst_packet.send_to(connection.ip, connection.port, self.parent.socket)
        print_debug("Sent RST packet to {0}:{1}".format(connection.ip, connection.port))
        return rst_packet

    def send_data_packet(self, connection,  packet: Segment):
        if connection is None or connection.state != ConnectionState.ACTIVE:
            return None

        bad_packets_seq = self.parent.settings.bad_packets_seq
        for attempt in range(self.parent.settings.packet_resend_attempts):

            if packet.seq in bad_packets_seq and attempt < self.parent.settings.bad_packets_attempts-1:
                packet.send_to_with_error(connection.ip, connection.port, self.parent.socket)

            elif packet.seq in bad_packets_seq:
                bad_packets_seq.remove(packet.seq)
                packet.send_to(connection.ip, connection.port, self.parent.socket)

            else:
                packet.send_to(connection.ip, connection.port, self.parent.socket)

            print_debug("Sent packet SEQ {0} to {1}:{2} server (attempt {3})".format(packet.seq, connection.ip, connection.port, attempt+1))
            ip, port, response = self.await_packet(connection, kill_on_fail=False)  # Awaiting ACK

            if ip != connection.ip or port != connection.port:
                break

            if response.flags.ack:
                return True  # If we received ACK, success
            elif response.flags.nack:
                continue  # If we received NACK, retry
            else:
                break  # If we received something else stop.

        self.kill_connection(connection)
        return None

    ###############################################
    # Await packets
    ###############################################
    def await_packet(self, connection: Connection = None, kill_on_fail: bool = True):
        try:
            data, addr = self.parent.socket.recvfrom(MTU)
        except OSError:
            # If socket froze while waiting for packet kill connection
            if connection is not None and kill_on_fail:
                self.kill_connection(connection)
            return None, None, None

        ip = addr[0]
        port = addr[1]
        packet = Segment().decode(data)

        if packet is None or (connection is not None and connection.ip != ip and connection.port != port):
            # If packet is broken, return ip and port and None
            return ip, port, None
        return ip, port, packet

    def await_syn_ack(self, connection: Connection, kill_on_fail: bool = True, return_packet: bool = False):
        ip, port, packet = self.await_packet(connection, kill_on_fail)

        if (
            packet is not None and
            connection.state == ConnectionState.SYN_SENT
            and packet.flags.syn and packet.flags.ack
            and connection.ip == ip and connection.port == port
        ):
            print_debug("Received SYN-ACK packet from {0}:{1}".format(connection.ip, connection.port))
            self.send_ack_packet(connection)
            connection.state = ConnectionState.ACTIVE
            return True if not return_packet else (True, packet)
        elif kill_on_fail:
            self.kill_connection(connection)  # Is technically a duplicate call in case await packet times out
        return False if not return_packet else (False, None)

    def await_fin_ack(self, connection: Connection, kill_on_fail: bool = True):
        ip, port, packet = self.await_packet(connection, kill_on_fail)

        if (
            packet is not None and
            connection.state == ConnectionState.FIN_SENT
            and packet.flags.fin and packet.flags.ack
            and connection.ip == ip and connection.port == port
        ):
            print_debug("Received FIN-ACK packet from {0}:{1}".format(connection.ip, connection.port))
            self.send_ack_packet(connection)
            return True
        elif kill_on_fail:
            self.kill_connection(connection)  # Is technically a duplicate call in case await packet times out
        return False

    ###############################################
    # Swap
    ###############################################
    def initiate_swap(self, connection: Connection = None, already_started: bool = False, switch_ip: bool = False):
        if connection is None:
            return

        swp_packet = Segment()
        swp_packet.flags.swp = True
        client_info_packet = Segment(data=self.parent.settings.encode())
        client_info_packet.flags.info = True

        # Sending SWP Received ACK
        if already_started or self.send_data_packet(connection, swp_packet) is True:
            # Sending settings Received ACK
            if self.send_data_packet(connection, client_info_packet) is True:
                # Receive server settings
                _, _, packet = self.await_packet()

                # Send ACK for server settings
                self.send_ack_packet(connection)

                # Decode server settings and swap roles
                if packet is not None and packet.flags.info:
                    settings = Settings().decode(packet.data)

                    if switch_ip:
                        settings.ip = connection.ip  # We want to connect to the other end

                    self._toggle_role(connection, settings)

            self.kill_connection(connection)

    def received_swap(self, connection: Connection, already_started: bool = False, switch_ip: bool = True):
        if connection is None:
            return

        if not already_started:
            # Ack for SWP packet
            self.send_ack_packet(connection)

        # Receiving client info packet
        _, _, client_info_packet = self.await_packet(connection)
        if client_info_packet.flags.info:
            # Sending ACK for client info packet
            self.send_ack_packet(connection)
        else:
            self.kill_connection(connection)
            return

        # Preparing server info packet
        info_packet = Segment(data=self.parent.settings.encode())
        info_packet.flags.info = True

        # Sending server info packet receiving ACK
        if self.send_data_packet(connection, info_packet) is False:
            self.kill_connection(connection)
            return

        settings = Settings().decode(client_info_packet.data)

        if switch_ip:
            settings.ip = connection.ip  # We want to connect to the other end

        self._toggle_role(connection, settings)

    # Helper method that toggles between Sender and Receiver
    def _toggle_role(self, connection: Connection, settings: Settings):
        self.kill_connection(connection)
        self.parent.close()

        from cli.MenuSystem import show_main_menu
        if self.__class__.__name__ == "SenderConnectionManager":
            from cli.MenuSystem import run_receiver_mode, show_receiver_menu
            run_receiver_mode(settings)  # Start server mode
            show_receiver_menu()
            print_debug("Exiting from SWP (Sender) to main menu...")
        elif self.__class__.__name__ == "ReceiverConnectionManager":
            from cli.MenuSystem import run_sender_mode, show_sender_menu
            run_sender_mode(settings)
            show_sender_menu()
            print_debug("Exiting from SWP (Receiver) to main menu...")
        show_main_menu()
        os.kill(os.getpid(), signal.SIGTERM)

    def __str__(self):
        _str = "Connection Manger:\n"

        _str += "Active connections:\n"
        for active_connection in self.active_connections:
            _str += str(active_connection) + "\n"

        _str += "Inactive connections:\n"
        for inactive_connection in self.inactive_connections:
            _str += str(inactive_connection) + "\n"

        return _str
