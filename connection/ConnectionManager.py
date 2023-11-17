import threading

from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
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
        for connection in self.inactive_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        for connection in self.active_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        return None

    def remove_connection(self, connection: Connection):
        print_debug(connection.ip+":"+str(connection.port), "was removed!")
        if connection in self.inactive_connections:
            self.inactive_connections.remove(connection)
        elif connection in self.active_connections:
            self.active_connections.remove(connection)
        connection.keepalive_thread.stop()

    def kill_connection(self, connection: Connection):
        print_debug(connection.ip+":"+str(connection.port), "was killed!")
        rst_packet = Packet()
        rst_packet.flags.rst = True
        rst_packet.send_to((connection.ip, connection.port), self.parent.socket)
        self.remove_connection(connection)
        connection.keepalive_thread.stop()
        connection.state = ConnectionState.RESET

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
        syn_packet = Packet()
        syn_packet.flags.syn = True
        syn_packet.send_to((connection.ip, connection.port), self.parent.socket)
        connection.state = ConnectionState.SYN_SENT

    def send_fin_packet(self, connection: Connection):
        fin_packet = Packet()
        fin_packet.flags.fin = True
        fin_packet.send_to((connection.ip, connection.port), self.parent.socket)
        connection.state = ConnectionState.FIN_SENT

    def send_syn_ack_packet(self, connection: Connection):
        syn_ack_packet = Packet()
        syn_ack_packet.flags.syn = True
        syn_ack_packet.flags.ack = True
        syn_ack_packet.send_to((connection.ip, connection.port), self.parent.socket)
        connection.state = ConnectionState.SYN_ACK_SENT

    def send_fin_ack_packet(self, connection: Connection):
        fin_ack_packet = Packet()
        fin_ack_packet.flags.fin = True
        fin_ack_packet.flags.ack = True
        fin_ack_packet.send_to((connection.ip, connection.port), self.parent.socket)
        connection.state = ConnectionState.FIN_ACK_SENT

    def send_ack_packet(self, connection):
        ack_packet = Packet()
        ack_packet.flags.ack = True
        ack_packet.send_to((connection.ip, connection.port), self.parent.socket)

    ###############################################
    # Await packets
    ###############################################
    def await_packet(self):
        data, addr = self.parent.socket.recvfrom(MTU)
        ip = addr[0]
        port = addr[1]
        packet = Packet().decode(data)
        return ip, port, packet

    def await_syn_ack(self, connection: Connection):
        # TODO:: Handle not receiving syn ack (Kill connection)?
        ip, port, packet = self.await_packet()

        if (
            connection.state == ConnectionState.SYN_SENT
            and packet.flags.syn and packet.flags.ack
            and connection.ip == ip and connection.port == port
        ):
            self.send_ack_packet(connection)
            connection.state = ConnectionState.ACTIVE
            return True
        return False

    def await_fin_ack(self, connection: Connection):
        # TODO:: Handle not receiving fin ack (Kill connection)?
        ip, port, packet = self.await_packet()

        if (
            connection.state == ConnectionState.FIN_SENT
            and packet.flags.fin and packet.flags.ack
            and connection.ip == ip and connection.port == port
        ):
            self.send_ack_packet(connection)
            connection.state = ConnectionState.CLOSED
            return True
        return False

    def __str__(self):
        _str = "Connection Manger:\n"

        _str += "Active connections:\n"
        for active_connection in self.active_connections:
            _str += str(active_connection) + "\n"

        _str += "Inactive connections:\n"
        for inactive_connection in self.inactive_connections:
            _str += str(inactive_connection) + "\n"

        return _str


    # Pseudo idea
    # Hold list of active connections
    # Each connection has its own thread manager???
    # When new connection is created, it is added to the list
    # When connection is closed, it is removed from the list
    # Manage keepalive of connections (receiving SYN's every 5s) (its own thread)
