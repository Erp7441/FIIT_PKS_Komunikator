from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager


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
            print("Connection with", str(connection), "established")
        return connection

    ###############################################
    # Closing connection (sender)
    ###############################################
    def close_connection(self, ip: str, port: int):
        connection = self.get_connection(ip, port)
        self.send_fin_packet(connection)

        if self.await_fin_ack(connection):
            self.active_connections.remove(connection)
            print("Connection with", str(connection), "closed")

    ###############################################
    # Keep alive sequence
    ###############################################
    def refresh_keepalive(self, connection: Connection):
        connection.keepalive_event.set()
        self.send_syn_packet(connection)
        if self.await_syn_ack(connection):
            connection.current_keepalive_time = connection.keepalive_time
            self.send_ack_packet(connection)
            print_debug("Refreshed keepalive state!")
            connection.keepalive_event.clear()
            return True
        print_debug("Failed to refresh keepalive state!")
        connection.keepalive_event.clear()
        return False