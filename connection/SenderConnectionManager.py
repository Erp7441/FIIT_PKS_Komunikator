from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState
from utils.Utils import print_debug, print_color


class SenderConnectionManager(ConnectionManager):
    def __init__(self, sender):
        super().__init__(sender)

    ###############################################
    # Establishing connection (sender)
    ###############################################
    def establish_connection(self, ip: str, port: int):
        connection = Connection(ip, port, None, parent=self)
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
            self.send_fin_packet(connection)

            if self.await_fin_ack(connection):
                self.remove_connection(connection)
                print_color("Connection with", connection.ip+":"+str(connection.port), "closed", color='green')

    ###############################################
    # Keep alive sequence
    ###############################################
    def refresh_keepalive(self, connection: Connection):
        with self.lock:
            self.send_syn_packet(connection)
            if self.await_syn_ack(connection):
                connection.current_keepalive_time = connection.keepalive_time
                self.send_ack_packet(connection)
                print_debug("Refreshed keepalive state!")
                connection.state = ConnectionState.ACTIVE
                return True
            print_debug("Failed to refresh keepalive state!", color='orange')
            return False

    def __str__(self):
        return "Sender " + super().__str__()

