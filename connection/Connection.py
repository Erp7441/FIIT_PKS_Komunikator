from connection.Communication import Communication
from utils.ThreadManager import ThreadManager
from connection.ConnectionState import ConnectionState


class Connection:
    def __init__(self, ip, port, syn_packet):
        self.ip = ip
        self.port = port
        self.state = ConnectionState.SYN_RECEIVED
        self.communication = Communication([syn_packet])
        self.thread_manager = ThreadManager()

        # Run timer for keep alive

    # Pseudo idea
    # Holds information about connection state
    # Holds information about last packet sent/received???
    # Thread manager for the connection
        # One thread for keep alive
        # Second thread for communication
