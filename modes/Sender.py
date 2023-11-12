import socket as s
from utils.Constants import DEFAULT_PORT

class Sender:
    def __init__(self, ip: str, port: int = DEFAULT_PORT):
        # TODO:: Handle data via assembler, connect to server then start sending sequence

        self.socket = s.socket(s.AF_INET, s.SOCK_STREAM)
        self.socket.connect((ip, port))
