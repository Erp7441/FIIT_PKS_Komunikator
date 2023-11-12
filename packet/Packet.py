from data.Data import Data
from packet.Flags import Flags
from utils.Coder import encode_int_to_hex, decode_int_from_hex, decode_str_from_bytes
from utils.Constants import SEQ_SIZE, CRC_SIZE


class Packet:
    def __init__(self, flags: Flags = None, seq=0, data: Data = None):
        self.flags = flags
        self.seq = seq
        self.crc = 0 if data is None else data.crc32()
        self.data = None if data is None else data.encode()

    def encode(self):
        encoded_seq = encode_int_to_hex(self.seq, SEQ_SIZE)
        encoded_crc = encode_int_to_hex(self.crc, CRC_SIZE)
        return self.flags.encode() + encoded_seq + encoded_crc + self.data

    def decode(self, data):
        if isinstance(data, bytes):
            data = decode_str_from_bytes(data)

        self.flags = Flags()
        self.flags.decode(data[0:4])
        self.seq = decode_int_from_hex(data[4:12])
        self.crc = decode_int_from_hex(data[12:20])
        self.data = data[20:]
        return self
