from connection.Connection import Connection
from connection.ConnectionState import ConnectionState
from connection.manager.ConnectionManager import ConnectionManager
from utils.Utils import print_debug, print_color


class SenderConnectionManager(ConnectionManager):
    def __init__(self, sender):
        super().__init__(sender)

    ###############################################
    # Establishing connection (sender)
    ###############################################
    def establish_connection(self, ip: str, port: int):
        connection = Connection(ip, port, None, parent=self)
        self.send_syn_packet(connection)  # SYN
        if self.await_syn_ack(connection):  # Awaiting SYN-ACK and sending ACK
            self.active_connections.append(connection)
            print_color("Connection with", connection.ip+":"+str(connection.port), "established", color='green')
        return connection

    ###############################################
    # Closing connection (sender)
    ###############################################
    def close_connection(self, ip: str, port: int):
        with self.lock:
            connection = self.get_connection(ip, port)

            # Check if connection is valid
            if connection is None:
                print_debug("Connection with {0}:{1} does not exist!".format(ip, port))
                return
            elif connection.state is ConnectionState.CLOSED or connection.state is ConnectionState.RESET:
                print_debug("Connection with {0}:{1} is already closed!".format(ip, port))
                return

            self.send_fin_packet(connection)  # FIN
            if self.await_fin_ack(connection):  # Awaiting SYN-ACK and sending ACK
                self.remove_connection(connection)
                print_color("Connection with", connection.ip+":"+str(connection.port), "closed", color='green')

    ###############################################
    # Keep alive sequence
    ###############################################
    def refresh_keepalive(self, connection: Connection):
        with self.lock:
            if connection.state == ConnectionState.CLOSED or connection.state == ConnectionState.RESET:
                print_debug("Failed to refresh keepalive state! Connection is already closed", color="red")
                return False

            self.send_syn_packet(connection)  # SYN
            if self.await_syn_ack(connection):  # Awaiting SYN-ACK and sending ACK
                connection.current_keepalive_time = connection.keepalive_time  # Refresh keepalive timer
                connection.state = ConnectionState.ACTIVE
                print_debug("Refreshed keepalive state!", color='green')
                return True
            print_debug("Failed to refresh keepalive state!", color='red')
            return False

    def __str__(self):
        return "Sender " + super().__str__()

