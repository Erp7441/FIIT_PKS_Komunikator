import threading


class ThreadManager:
    # TODO:: Next implement threading for keep alive
    # First find out how to create thread and start it.
    # From client:
        # Then create function to refresh keep alive state
        # Create new thread that calls the function every 5 seconds
    # From server:
        # Create timer thread that counts down to 5 seconds
        # If the server receives refresh sequence while counting to 5 then refresh the counter
        # If the counter reaches 0 then kill the connection

    def __init__(self):
        self.keepalive_thread = threading.Thread()
        self.data_thread = threading.Thread()

    # Pseudo idea
    # Manages threads
    # One thread for keep alive
    # One thread for data transmitting
