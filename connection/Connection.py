from time import sleep
from typing import Callable

from connection.ConnectionState import ConnectionState
from connection.KeepaliveThread import KeepaliveThread
from packet.Segment import Segment
from utils.Constants import RECEIVER_KEEPALIVE_TIME, SENDER_KEEPALIVE_TIME, DEFAULT_KEEPALIVE_TIME


class Connection:
    def __init__(self, ip: str, port: int, syn_packet=None, parent=None, keepalive_time=None):
        self.ip = ip
        self.port = port
        self.state = None if syn_packet is None else ConnectionState.SYN_SENT
        self.packets = []
        self.parent = parent

        # Selecting keepalive method based on parent class
        if parent.__class__.__name__ == "ReceiverConnectionManager":
            self._init_keep_alive_(keepalive_time, RECEIVER_KEEPALIVE_TIME, self.await_keep_alive)
        elif parent.__class__.__name__ == "SenderConnectionManager":
            self._init_keep_alive_(keepalive_time, SENDER_KEEPALIVE_TIME, self.keep_alive)
        else:
            self._init_keep_alive_(keepalive_time, DEFAULT_KEEPALIVE_TIME)

    # Add packet and sort the list
    def add_packet(self, packet: Segment):
        self.packets.append(packet)
        self.packets.sort(key=lambda seq: seq.seq)

    # Wait for "keepalive_time" seconds
    def _count_down(self):
        for _ in range(self.keepalive_time, 0, -1):
            if self.keepalive_thread.is_stopped():
                return False  # Exit the loop when thread stop is detected
            self.current_keepalive_time -= 1
            sleep(1)
        return True  # Count down finished

    ###############################################
    # Client (sender) keep alive
    ###############################################
    def keep_alive(self):
        if not self._count_down():
            return  # Exit when thread stop is detected
        # If refreshing connection was not successful. Kill it
        if not self.keepalive_thread.is_stopped() and not self.parent.refresh_keepalive(self):
            self.parent.kill_connection(self)

    ###############################################
    # Server (receiver) keep alive
    ###############################################
    def await_keep_alive(self):
        if not self._count_down():
            return  # Exit when thread stop is detected
        # If connection keep alive time is 0. Kill it.
        if not self.keepalive_thread.is_stopped() and self.current_keepalive_time <= 0:
            self.parent.kill_connection(self)

    ###############################################
    # Keep alive init
    ###############################################
    def _init_keep_alive_(self, keepalive_time=None, default_keepalive_time=DEFAULT_KEEPALIVE_TIME, keep_alive_method: Callable = None):
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

    ###############################################
    # Output
    ###############################################
    def stats(self):
        _str = ""
        if self.ip is not None:
            _str += "IP: " + str(self.ip) + "\n"
        if self.port is not None:
            _str += "Port: " + str(self.port) + "\n"

        if self.state is not None:
            _str += "State: " + str(self.state) + "\n"
        return _str

    def __str__(self):
        _str = "Connection:\n"
        _str += self.stats()

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
