from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState
from utils.Utils import print_debug


class ReceiverConnectionManager(ConnectionManager):
    def __init__(self, receiver):
        super().__init__(receiver)

    ###############################################
    # Establishing connection (receiver)
    ###############################################
    def start_establish_connection(self, packet, ip: str, port: int):
        existing_connection = self.get_connection(ip, port)

        if packet.flags.syn and existing_connection is None:
            print_debug("Received SYN packet from {0}:{1}. Establishing connection...".format(ip, port))
            connection = Connection(ip, port, syn_packet=packet, parent=self)
            self.inactive_connections.append(connection)
            self.send_syn_ack_packet(connection)

    def finish_establish_connection(self, packet, connection: Connection):
        if packet.flags.ack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            print_debug("Received ACK packet from {0}:{1}. Connection established!".format(connection.ip, connection.port))
            # If we received ack after syn ack. Move communication to active list
            connection.state = ConnectionState.ACTIVE
            self.move_connection_to_active(connection)
        elif packet.flags.nack and connection and connection.state == ConnectionState.SYN_ACK_SENT:
            # If we received nack after syn ack. Resend syn ack
            self.send_syn_ack_packet(connection)

        # TODO:: ACK wont be received within 5 seconds, kill connection?

    ###############################################
    # Closing connection (receiver)
    ###############################################
    def start_closing_connection(self, packet, connection: Connection):
        with self.lock:
            if packet.flags.fin and connection is not None:
                print_debug("Received FIN packet from {0}:{1}".format(connection.ip, connection.port))
                connection.state = ConnectionState.FIN_RECEIVED
                self.move_connection_to_inactive(connection)
                self.send_fin_ack_packet(connection)

    def finish_closing_connection(self, packet, connection: Connection):
        with self.lock:
            if packet.flags.ack and connection and connection.state == ConnectionState.FIN_ACK_SENT:
                print_debug("Received ACK packet from {0}:{1}. Closing connection...".format(connection.ip, connection.port))
                # If we received ack after syn ack. Move communication to active list
                self.remove_connection(connection)
            elif packet.flags.nack and connection and connection.state == ConnectionState.FIN_ACK_SENT:
                # If we received nack after syn ack. Resend syn ack
                self.send_fin_ack_packet(connection)

        # TODO:: ACK wont be received within 5 seconds, kill connection?

    #############################################################
    # Received SYN for refreshing the connection keepalive state
    #############################################################
    def refresh_keepalive(self, connection: Connection):
        with (self.lock):
            if connection.state == ConnectionState.CLOSED or connection.state == ConnectionState.RESET:
                print_debug("Failed to refresh keepalive state! Connection is already closed", color="red")
                return False

            self.send_syn_ack_packet(connection)
            ip, port, packet = self.await_packet(connection)
            if (
                packet is not None and
                (connection.ip == ip and connection.port == port and packet.flags.ack)
            ):
                # Reset current keepalive time
                connection.current_keepalive_time = connection.keepalive_time
                connection.state = ConnectionState.ACTIVE
                print_debug("Refreshed keepalive state of client!", color="green")
                return True
            print_debug("Failed to refresh keepalive state!", color="red")
            return False

    def __str__(self):
        return "Receiver " + super().__str__()