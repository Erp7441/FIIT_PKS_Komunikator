from utils.Constants import FLAGS_SIZE
from utils.Utils import convert_int_to_bytes, convert_bytes_to_int


class Flags:
    def __init__(self, syn=False, ack=False, nack=False, swp=False, info=False, file=False, msg=False, rst=False, fin=False):
        self.syn = syn
        self.ack = ack
        self.nack = nack
        self.swp = swp
        self.info = info
        self.file = file
        self.msg = msg
        self.rst = rst
        self.fin = fin

    def encode(self):
        flags = 0
        if self.syn:
            flags |= 1
        if self.ack:
            flags |= 2
        if self.nack:
            flags |= 4
        if self.swp:
            flags |= 8
        if self.info:
            flags |= 16
        if self.file:
            flags |= 32
        if self.msg:
            flags |= 64
        if self.rst:
            flags |= 128
        if self.fin:
            flags |= 256
        return convert_int_to_bytes(flags, FLAGS_SIZE)

    def decode(self, flags):
        flags = convert_bytes_to_int(flags)
        self.syn = True if flags & 1 == 1 else False
        self.ack = True if flags & 2 == 2 else False
        self.nack = True if flags & 4 == 4 else False
        self.swp = True if flags & 8 == 8 else False
        self.info = True if flags & 16 == 16 else False
        self.file = True if flags & 32 == 32 else False
        self.msg = True if flags & 64 == 64 else False
        self.rst = True if flags & 128 == 128 else False
        self.fin = True if flags & 256 == 256 else False
        return self

    def __str__(self):
        _str = ""
        _str += " SYN " if self.syn else ""
        _str += " ACK " if self.ack else ""
        _str += " NACK " if self.nack else ""
        _str += " SWP " if self.swp else ""
        _str += " INFO " if self.info else ""
        _str += " FILE " if self.file else ""
        _str += " MSG " if self.msg else ""
        _str += " RST " if self.rst else ""
        _str += " FIN " if self.fin else ""
        return _str.strip()
