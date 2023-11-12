class ConnectionManager:
    def __init__(self):
        pass

    # Pseudo idea
    # Hold list of active connections
    # Each connection has its own thread manager???
    # When new connection is created, it is added to the list
    # When connection is closed, it is removed from the list
    # Manage keepalive of connections (reciving SYN's every 5s) (its own thread)
