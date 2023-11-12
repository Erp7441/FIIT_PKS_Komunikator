from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
from utils.Constants import MTU


class SenderConnectionManager(ConnectionManager):
    def __init__(self, sender):
        super().__init__(sender)

    # Establishing connection
    def establish_connection(self, ip: str, port: int):
        connection = Connection(ip, port, None)
        self.send_syn_packet(connection)

        if self.await_syn_ack(connection):
            self.active_connections.append(connection)
            print("Connection with", str(connection), "established")
        return connection

    def await_syn_ack(self, connection):
        # TODO:: Handle not reciving syn ack (Kill connection)?
        ip, port, packet = self.await_packet()

        if (
            connection.state == ConnectionState.SYN_SENT
            and packet.flags.syn and packet.flags.ack
            and connection.ip == ip and connection.port == port
        ):
            ack_packet = Packet()
            ack_packet.flags.ack = True
            ack_packet.send_to((connection.ip, connection.port), self.parent.socket)
            connection.state = ConnectionState.ACTIVE
            return True
        return False

    def close_connection(self, ip: str, port: int):
        connection = self.get_connection(ip, port)
        self.send_fin_packet(connection)

        if self.await_fin_ack(connection):
            self.active_connections.remove(connection)
            print("Connection with", str(connection), "closed")

    def await_fin_ack(self, connection):
        # TODO:: Handle not reciving syn ack (Kill connection)?
        ip, port, packet = self.await_packet()

        if (
                connection.state == ConnectionState.FIN_SENT
                and packet.flags.fin and packet.flags.ack
                and connection.ip == ip and connection.port == port
        ):
            ack_packet = Packet()
            ack_packet.flags.ack = True
            ack_packet.send_to((connection.ip, connection.port), self.parent.socket)
            connection.state = ConnectionState.CLOSED
            return True
        return False

    def await_packet(self):
        data, addr = self.parent.socket.recvfrom(MTU)
        ip = addr[0]
        port = addr[1]
        packet = Packet().decode(data)
        return ip, port, packet