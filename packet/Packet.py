from packet.Flags import Flags


class Packet:
    def __init__(self, flags: Flags, seq=0, crc=None, data=None):
        self.flags = flags
        self.seq = seq
        self.crc = crc
        self.data = data
