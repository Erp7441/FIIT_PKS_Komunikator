from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
from utils.Coder import encode_str_to_bytes


class ConnectionManager:
    def __init__(self, receiver):
        self.active_connections = []
        self.inactive_connections = []
        self.refreshing_connections = []
        self.receiver = receiver

    # Establishing connection
    def start_establish_connection(self, packet, ip: str, port: str):
        existing_connection = self.get_connection(ip, port)

        if packet.flags.syn and existing_connection is None:

            connection = Connection(ip, port, syn_packet=packet)
            self.inactive_connections.append(connection)

            self.send_syn_ack_packet(connection)
            connection.state = ConnectionState.SYN_ACK_SENT

    def finish_establish_connection(self, packet, connection: Connection):
        if packet.flags.ack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received ack after syn ack. Move communication to active list
            connection.state = ConnectionState.ACTIVE
            self.move_connection_to_active(connection)
        elif packet.flags.nack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received nack after syn ack. Resend syn ack
            self.send_syn_ack_packet(connection)
        # Else we wont do anything.
        # TODO:: ACK wont be received within 5 seconds, kill connection?

    # Closing connection
    def start_closing_connection(self, packet, connection: Connection):
        if packet.flags.fin and connection is not None:
            connection.state = ConnectionState.FIN_RECEIVED
            self.move_connection_to_inactive(connection)

            self.send_fin_ack_packet(connection)
            connection.state = ConnectionState.FIN_ACK_SENT

    def finish_closing_connection(self, packet, connection: Connection):
        if packet.flags.ack and connection and connection.state == ConnectionState.FIN_ACK_SENT:
            # If we received ack after syn ack. Move communication to active list
            connection.state = ConnectionState.CLOSED
            self.remove_connection(connection)
        elif packet.flags.nack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received nack after syn ack. Resend syn ack
            self.send_fin_ack_packet(connection)
        # Else we wont do anything.
        # TODO:: ACK wont be received within 5 seconds, kill connection?

    def get_connection(self, ip: str, port: str):
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
    def send_syn_ack_packet(self, connection: Connection):
        syn_ack_packet = Packet()
        syn_ack_packet.flags.syn = True
        syn_ack_packet.flags.ack = True
        self.send_packet(syn_ack_packet, connection)

    def send_fin_ack_packet(self, connection: Connection):
        fin_ack_packet = Packet()
        fin_ack_packet.flags.fin = True
        fin_ack_packet.flags.ack = True
        self.send_packet(fin_ack_packet, connection)

    def send_packet(self, packet, connection: Connection):
        encoded_data_string = packet.encode()
        encoded_data_bytes = encode_str_to_bytes(encoded_data_string)
        self.receiver.socket.sendto(encoded_data_bytes.encode(), (connection.ip, connection.port))



    # Pseudo idea
    # Hold list of active connections
    # Each connection has its own thread manager???
    # When new connection is created, it is added to the list
    # When connection is closed, it is removed from the list
    # Manage keepalive of connections (reciving SYN's every 5s) (its own thread)
