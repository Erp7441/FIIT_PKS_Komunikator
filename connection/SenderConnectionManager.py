from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState
from utils.Constants import WINDOW_SIZE
from utils.Utils import print_debug, print_color


class SenderConnectionManager(ConnectionManager):
    def __init__(self, sender):
        super().__init__(sender)

    ###############################################
    # Establishing connection (sender)
    ###############################################
    def establish_connection(self, ip: str, port: int):
        connection = Connection(ip, port, None, parent=self, batch_size=WINDOW_SIZE)
        self.send_syn_packet(connection)

        if self.await_syn_ack(connection):
            self.active_connections.append(connection)
            print_color("Connection with", connection.ip+":"+str(connection.port), "established", color='green')
        return connection

    ###############################################
    # Closing connection (sender)
    ###############################################
    def close_connection(self, ip: str, port: int):
        with self.lock:
            connection = self.get_connection(ip, port)
            if connection is None:
                print_debug("Connection with {0}:{1} does not exist!".format(ip, port))
                return
            elif connection.state is ConnectionState.CLOSED or connection.state is ConnectionState.RESET:
                print_debug("Connection with {0}:{1} is already closed!".format(ip, port))
                return

            self.send_fin_packet(connection)

            if self.await_fin_ack(connection):
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

            self.send_syn_packet(connection)
            if self.await_syn_ack(connection):
                connection.current_keepalive_time = connection.keepalive_time
                self.send_ack_packet(connection)
                connection.state = ConnectionState.ACTIVE
                print_debug("Refreshed keepalive state!")
                return True
            print_debug("Failed to refresh keepalive state!", color='orange')
            return False

    def __str__(self):
        return "Sender " + super().__str__()

