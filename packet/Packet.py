from packet.Flags import Flags


class Packet:
    def __init__(self):
        self.flags = Flags()
        self.crc = None
        self.data = None
