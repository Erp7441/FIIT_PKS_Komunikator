from data.Data import Data
from packet.Flags import Flags
from utils.Coder import encode_int_to_hex, decode_int_from_hex, decode_str_from_bytes
from utils.Constants import SEQ_B_SIZE, CRC_B_SIZE, FLAGS_B_SIZE, SEQ_SIZE, CRC_SIZE


class Packet:
    def __init__(self, flags: Flags = None, seq=0, data: Data = None):
        self.flags = Flags() if flags is None else flags
        self.seq = seq
        self.crc = 0 if data is None else data.crc32()
        self.data = None if data is None else data.encode()

    def encode(self):
        encoded_seq = encode_int_to_hex(self.seq, SEQ_SIZE)
        encoded_crc = encode_int_to_hex(self.crc, CRC_SIZE)
        encoded_data = "" if self.data is None else self.data
        return self.flags.encode() + encoded_seq + encoded_crc + encoded_data

    def decode(self, data):
        if isinstance(data, bytes):
            data = decode_str_from_bytes(data)

        flags_header = data[0:FLAGS_B_SIZE]
        seq_header = data[FLAGS_B_SIZE:FLAGS_B_SIZE + SEQ_B_SIZE]
        crc_header = data[FLAGS_B_SIZE + SEQ_B_SIZE:FLAGS_B_SIZE + SEQ_B_SIZE + CRC_B_SIZE]
        data_header = data[FLAGS_B_SIZE + SEQ_B_SIZE + CRC_B_SIZE:]

        self.flags = Flags().decode(flags_header)
        self.seq = decode_int_from_hex(seq_header)
        self.crc = decode_int_from_hex(crc_header)
        self.data = data_header
        return self
