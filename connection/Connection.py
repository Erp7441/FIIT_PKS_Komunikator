from threading import Thread
from time import sleep

from connection.Communication import Communication
from connection.ConnectionState import ConnectionState

from utils.Constants import DEFAULT_KEEPALIVE_TIME


# TODO:: Next implement threading for keep alive
# First find out how to create thread and start it.
# From client:
# Then create function to refresh keep alive state
# Create new thread that calls the function every 5 seconds
# From server:
# Create timer thread that counts down to 5 seconds
# If the server receives refresh sequence while counting to 5 then refresh the counter
# If the counter reaches 0 then kill the connection

class Connection:
    def __init__(self, ip: str, port: int, syn_packet=None, parent=None, keepalive_time=DEFAULT_KEEPALIVE_TIME):
        self.ip = ip
        self.port = port
        self.state = None if syn_packet is None else ConnectionState.SYN_SENT
        self.communication = Communication()
        self.parent = parent
        self.keepalive_time = keepalive_time
        self.current_keepalive_time = keepalive_time

        if syn_packet is not None:
            self.communication.packets.append(syn_packet)

        # Initializing keep alive thread
        if parent.__class__.__name__ == "ReceiverConnectionManager":
            self.keepalive_thread = Thread(target=self.await_keep_alive)
            self.keepalive_thread.start()
        elif parent.__class__.__name__ == "SenderConnectionManager":
            self.keepalive_thread = Thread(target=self.keep_alive)
            self.keepalive_thread.start()
        else:
            self.keepalive_thread = None

    # Run timer for keep alive
    # Client side method
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

    # Server side method
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

    def __str__(self):
        return self.ip + ":" + str(self.port)

    # Pseudo idea
    # Holds information about connection state
    # Holds information about last packet sent/received???
    # Thread manager for the connection
    # One thread for keep alive
    # Second thread for communication
