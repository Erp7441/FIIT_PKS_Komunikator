from data.Data import Data
from packet.Flags import Flags


class Packet:
    def __init__(self, flags: Flags, seq=0, data: Data = None):
        self.flags = flags
        self.seq = seq
        self.crc = 0 if data is None else data.crc32()
        self.data = None if data is None else data.encode()
