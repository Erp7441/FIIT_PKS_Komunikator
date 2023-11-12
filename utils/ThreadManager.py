import threading


class ThreadManager:
    # TODO:: Next implement threading for keep alive
    def __init__(self):
        self.keepalive_thread = threading.Thread()
        self.data_thread = threading.Thread()

    # Pseudo idea
    # Manages threads
    # One thread for keep alive
    # One thread for data transmitting
