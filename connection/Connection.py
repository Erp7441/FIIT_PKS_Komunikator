from time import sleep
from typing import Callable

from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
from utils.Constants import RECEIVER_KEEPALIVE_TIME, SENDER_KEEPALIVE_TIME, DEFAULT_KEEPALIVE_TIME
from utils.KeepaliveThread import KeepaliveThread


# Comm
# Pseudo idea
# Gets splited data in packets
# Evaluate packets order and crc32
# Two things will be required in here
# Get next packet - gets next packet in communication for sending
# Get last packet - gets last packet in communication for resending in case of error


class Connection:
    def __init__(self, ip: str, port: int, syn_packet=None, parent=None, keepalive_time=None):
        self.ip = ip
        self.port = port
        self.state = None if syn_packet is None else ConnectionState.SYN_SENT
        self.packets = []
        self.parent = parent

        if parent.__class__.__name__ == "ReceiverConnectionManager":
            self._init_keep_alive_(keepalive_time, RECEIVER_KEEPALIVE_TIME, self.await_keep_alive)
        elif parent.__class__.__name__ == "SenderConnectionManager":
            self._init_keep_alive_(keepalive_time, SENDER_KEEPALIVE_TIME, self.keep_alive)
        else:
            self._init_keep_alive_(keepalive_time, DEFAULT_KEEPALIVE_TIME)

    def add_packet(self, packet: Packet):
        self.packets.append(packet)
        self.packets.sort(key=lambda seq: seq.seq)

    ###############################################
    # Client (sender) keep alive
    ###############################################
    def keep_alive(self):
        # Wait for 5s
        for _ in range(self.keepalive_time, 0, -1):
            self.current_keepalive_time -= 1
            sleep(1)

        # If refreshing connection was not successful. Kill it
        if not self.parent.refresh_keepalive(self):
            self.parent.kill_connection(self)


    ###############################################
    # Server (receiver) keep alive
    ###############################################
    def await_keep_alive(self):
        # Wait for 5s
        for _ in range(self.keepalive_time, 0, -1):
            self.current_keepalive_time -= 1
            sleep(1)

        # If connection keep alive time is 0. Kill it.
        if self.current_keepalive_time <= 0:
            self.parent.kill_connection(self)


    ###############################################
    # Keep alive init
    ###############################################
    def _init_keep_alive_(self, keepalive_time=None, default_keepalive_time=None, keep_alive_method: Callable = None):
        # Initialize sender keepalive time
        if keepalive_time is None:
            self.keepalive_time = default_keepalive_time
            self.current_keepalive_time = default_keepalive_time
        else:
            self.keepalive_time = keepalive_time
            self.current_keepalive_time = keepalive_time

        # Initialize sender keepalive thread
        self.keepalive_thread = KeepaliveThread(target=keep_alive_method)
        self.keepalive_thread.start()

    def __str__(self):
        _str = "Connection:\n"

        if self.ip is not None:
            _str += "IP: " + str(self.ip) + "\n"
        if self.port is not None:
            _str += "Port: " + str(self.port) + "\n"

        if self.state is not None:
            _str += "State: " + str(self.state) + "\n"

        if self.current_keepalive_time is not None:
            _str += "Current keepalive time: " + str(self.current_keepalive_time) + "\n"

        if self.packets is not None:
            _str += "Packets:\n"
            for packet in self.packets:
                _str += str(packet) + "\n"

        if self.keepalive_time is not None:
            _str += "Keepalive time: " + str(self.keepalive_time) + "\n"
        if self.keepalive_thread is not None:
            _str += "Keepalive thread: " + str(self.keepalive_thread)
        return _str
