from threading import Thread, Event
from time import sleep
from typing import Callable

from connection.ConnectionState import ConnectionState
from packet.Packet import Packet
from utils.Constants import RECEIVER_KEEPALIVE_TIME, SENDER_KEEPALIVE_TIME, DEFAULT_KEEPALIVE_TIME


# TODO:: Next implement threading for keep alive
# First find out how to create thread and start it.
# From client:
# Then create function to refresh keep alive state
# Create new thread that calls the function every 5 seconds
# From server:
# Create timer thread that counts down to 5 seconds
# If the server receives refresh sequence while counting to 5 then refresh the counter
# If the counter reaches 0 then kill the connection

# Comm
# Pseudo idea
# Gets splited data in packets
# Evaluate packets order and crc32
# Two things will be required in here
# Get next packet - gets next packet in communication for sending
# Get last packet - gets last packet in communication for resending in case of error

# Pseudo idea
# Holds information about connection state
# Holds information about last packet sent/received???
# Thread manager for the connection
# One thread for keep alive
# Second thread for communication


class Connection:
    def __init__(self, ip: str, port: int, syn_packet=None, parent=None, keepalive_time=None):
        self.ip = ip
        self.port = port
        self.state = None if syn_packet is None else ConnectionState.SYN_SENT
        self.packets = []
        self.parent = parent

        if syn_packet is not None:
            self.add_packet(syn_packet)

        if parent.__class__.__name__ == "ReceiverConnectionManager":
            self._init_keep_alive_(keepalive_time, RECEIVER_KEEPALIVE_TIME, self.await_keep_alive)
        elif parent.__class__.__name__ == "SenderConnectionManager":
            self._init_keep_alive_(keepalive_time, SENDER_KEEPALIVE_TIME, self.keep_alive)
        else:
            self._init_keep_alive_(keepalive_time, DEFAULT_KEEPALIVE_TIME)

    def add_packet(self, packet: Packet):
        # TODO:: Check if packet with seq number is not already present
        self.packets.append(packet)
        self.packets.sort(key=lambda seq: seq.seq)

    # TODO:: Refactor to client and server
    ###############################################
    # Client (sender) keep alive
    ###############################################
    def keep_alive(self):
        connection_killed = False
        while not connection_killed:
            # Wait for 5s
            for _ in range(self.keepalive_time, 0, -1):
                self.current_keepalive_time -= 1
                sleep(1)

            # If refreshing connection was not successful. Kill it
            if not self.parent.refresh_keepalive(self):
                self.parent.kill_connection(self)
                connection_killed = True

    ###############################################
    # Server (receiver) keep alive
    ###############################################
    def await_keep_alive(self):
        connection_killed = False
        while not connection_killed:
            # Wait for 5s
            for _ in range(self.keepalive_time, 0, -1):
                self.current_keepalive_time -= 1
                sleep(1)

            # If connection keep alive time is 0. Kill it.
            if self.current_keepalive_time <= 0:
                self.parent.kill_connection(self)
                connection_killed = True

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
        self.keepalive_thread = Thread(target=keep_alive_method)
        self.keepalive_thread.start()

    def __str__(self):
        return self.ip + ":" + str(self.port)
