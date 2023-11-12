from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState


class ReceiverConnectionManager(ConnectionManager):
    def __init__(self, receiver):
        super().__init__(receiver)

    # Establishing connection
    def start_establish_connection(self, packet, ip: str, port: int):
        existing_connection = self.get_connection(ip, port)

        if packet.flags.syn and existing_connection is None:

            connection = Connection(ip, port, syn_packet=packet)
            self.inactive_connections.append(connection)

            self.send_syn_ack_packet(connection)

    def finish_establish_connection(self, packet, connection: Connection):
        if packet.flags.ack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received ack after syn ack. Move communication to active list
            connection.state = ConnectionState.ACTIVE
            self.move_connection_to_active(connection)
        elif packet.flags.nack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received nack after syn ack. Resend syn ack
            self.send_syn_ack_packet(connection)

        # TODO:: ACK wont be received within 5 seconds, kill connection?

    # Closing connection
    def start_closing_connection(self, packet, connection: Connection):
        if packet.flags.fin and connection is not None:
            connection.state = ConnectionState.FIN_RECEIVED
            self.move_connection_to_inactive(connection)
            self.send_fin_ack_packet(connection)

    def finish_closing_connection(self, packet, connection: Connection):
        if packet.flags.ack and connection and connection.state == ConnectionState.FIN_ACK_SENT:
            # If we received ack after syn ack. Move communication to active list
            connection.state = ConnectionState.CLOSED
            self.remove_connection(connection)
        elif packet.flags.nack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received nack after syn ack. Resend syn ack
            self.send_fin_ack_packet(connection)

        # TODO:: ACK wont be received within 5 seconds, kill connection?
