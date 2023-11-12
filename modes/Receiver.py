import socket as s
from packet.Packet import Packet
from data.File import File
from utils.Constants import DEFAULT_PORT, MTU
from connection.ConnectionManager import ConnectionManager


class Receiver:
    def __init__(self, port: int = DEFAULT_PORT, ip: str = "0.0.0.0"):
        self.connections = ConnectionManager()
        self.socket = s.socket(s.AF_INET, s.SOCK_DGRAM)
        self.socket.bind((ip, port))

        print("Waiting for connection...")

        while True:
            data, addr = self.socket.recvfrom(MTU)
            print("Connected from", addr)
            print("Received data", data)

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

            # TODO REMOVE THIS TEST
            packet = Packet().decode(data)
            file = File().decode(packet.data)
            file.save("C:/Users/Martin/Downloads")
            pass
            # TODO:: Wait for SYN packet to start transmitting data. If SYN is received. Send ACK, etc...
