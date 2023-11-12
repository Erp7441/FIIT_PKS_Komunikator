import socket as s

from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
from data.File import File
from utils.Constants import DEFAULT_PORT, MTU
from connection.ConnectionManager import ConnectionManager


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.connections = ConnectionManager(self)
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))

        print("Waiting for connection...")

        while True:
            data, addr = self.socket.recvfrom(MTU)
            ip = addr[0]
            port = addr[1]

            packet = Packet().decode(data)
            connection = self.connections.get_connection(ip, port)

            # Begin establishing connection
            if packet.flags.syn and connection is None:
                self.connections.start_establish_connection(packet, ip, port)

            # Finish establishing / closing connection
            if packet.flags.ack and connection is not None:
                if connection.state == ConnectionState.SYN_ACK_SENT:
                    self.connections.finish_establish_connection(packet, connection)
                elif connection.state == ConnectionState.FIN_ACK_SENT:
                    self.connections.finish_closing_connection(packet, connection)

            # Received data packet
            if (
                packet.flags.info or packet.flags.file or packet.flags.msg
                and connection is not None and connection.state == ConnectionState.ACTIVE
            ):
                connection.communication.receive(packet)

            # Closing connection
            if packet.flags.fin and connection is not None and connection.state == ConnectionState.ACTIVE:
                self.connections.start_closing_connection(connection)

            # Pseudo idea
            # 1. Create communication object
            # 2. Handle opening of communication
                # if successfull add it ot connection manager
            # 3. Receive INFO
            # 4. Setup communication according to the info
            # 5. Receive DATA packets
            # 6. Handle DATA packets in communication
            # 7. Receive FIN
            # 8. Close connection

            # TODO:: Wait for SYN packet to start transmitting data. If SYN is received. Send ACK, etc...
