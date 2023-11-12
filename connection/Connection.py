from connection.Communication import Communication
from connection.ConnectionState import ConnectionState
from utils.ThreadManager import ThreadManager


class Connection:
    def __init__(self, ip: str, port: int, syn_packet=None):
        self.ip = ip
        self.port = port
        self.state = None if syn_packet is None else ConnectionState.SYN_SENT
        self.communication = Communication()
        self.thread_manager = ThreadManager()

        if syn_packet is not None:
            self.communication.packets.append(syn_packet)

        # Run timer for keep alive

    def __str__(self):
        return self.ip + ":" + str(self.port)

    # Pseudo idea
    # Holds information about connection state
    # Holds information about last packet sent/received???
    # Thread manager for the connection
        # One thread for keep alive
        # Second thread for communication
