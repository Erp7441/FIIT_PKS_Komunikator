from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from packet.Packet import Packet


class ConnectionManager:
    def __init__(self, parent):
        self.active_connections = []
        self.inactive_connections = []
        self.refreshing_connections = []
        self.parent = parent

    def get_connection(self, ip: str, port: int):
        for connection in self.inactive_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        for connection in self.active_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        for connection in self.refreshing_connections:
            if connection.ip == ip and connection.port == port:
                return connection
        return None

    def remove_connection(self, connection: Connection):
        if connection in self.inactive_connections:
            self.inactive_connections.remove(connection)
        elif connection in self.active_connections:
            self.active_connections.remove(connection)
        elif connection in self.refreshing_connections:
            self.refreshing_connections.remove(connection)

    # Move connections
    def move_connection_to_active(self, connection):
        if connection in self.inactive_connections:
            self.inactive_connections.remove(connection)
            self.active_connections.append(connection)
        elif connection in self.refreshing_connections:
            self.refreshing_connections.remove(connection)
            self.active_connections.append(connection)

    def move_connection_to_inactive(self, connection):
        if connection in self.active_connections:
            self.active_connections.remove(connection)
            self.inactive_connections.append(connection)
        elif connection in self.refreshing_connections:
            self.refreshing_connections.remove(connection)
            self.inactive_connections.append(connection)

    # Send packets
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



    # Pseudo idea
    # Hold list of active connections
    # Each connection has its own thread manager???
    # When new connection is created, it is added to the list
    # When connection is closed, it is removed from the list
    # Manage keepalive of connections (reciving SYN's every 5s) (its own thread)
