from binascii import crc32

from packet.Flags import Flags
from utils.Constants import FLAGS_SIZE, SEQ_SIZE, CRC_SIZE
from utils.Utils import convert_int_to_bytes, convert_bytes_to_str, convert_str_to_bytes, \
    convert_bytes_to_int


class Packet:
    def __init__(self, flags: Flags = None, seq=0, data = None):
        self.flags = Flags() if flags is None else flags
        self.seq = seq

        if isinstance(data, bytes):
            self.data = None if data is None else data
            self.crc = 0 if data is None else crc32(data)
        elif isinstance(data, str):
            self.data = None if data is None else data
            self.crc = 0 if data is None else crc32(convert_str_to_bytes(data))
        else:
            self.crc = 0 if data is None else data.crc32()
            self.data = None if data is None else data.encode()

    def encode(self):
        encoded_seq = convert_int_to_bytes(self.seq, SEQ_SIZE)
        encoded_crc = convert_int_to_bytes(self.crc, CRC_SIZE)
        encoded_data = b"" if self.data is None else self.data
        return self.flags.encode() + encoded_seq + encoded_crc + encoded_data

    def decode(self, data):
        flags_header = data[0:FLAGS_SIZE]
        seq_header = data[FLAGS_SIZE:FLAGS_SIZE + SEQ_SIZE]
        crc_header = data[FLAGS_SIZE + SEQ_SIZE:FLAGS_SIZE + SEQ_SIZE + CRC_SIZE]
        data_header = data[FLAGS_SIZE + SEQ_SIZE + CRC_SIZE:]

        self.flags = Flags().decode(flags_header)
        self.seq = convert_bytes_to_int(seq_header)
        self.crc = convert_bytes_to_int(crc_header)
        self.data = data_header
        return self

    # TODO:: Should this class be responsible for this?
    # TODO:: Get rid of tuples?
    def send_to(self, destination: tuple, socket):
        encoded_data_bytes = self.encode()
        socket.sendto(encoded_data_bytes, destination)

    def __str__(self):
        _str = "Packet:\n"
        if self.flags is not None:
            _str += "Flags: " + str(self.flags) + "\n"
        if self.seq is not None:
            _str += "SEQ: " + str(self.seq) + "\n"
        if self.crc is not None:
            _str += "CRC: " + str(self.crc) + "\n"
        if self.data is not None:
            _str += "Data: " + str(self.data) + "\n"
        return _str
