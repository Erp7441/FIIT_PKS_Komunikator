import socket as s


class Sender:
    def __init__(self, ip: str, port: int = 3333):
        # TODO:: Handle data via assembler, connect to server then start sending sequence

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.connect((ip, port))
