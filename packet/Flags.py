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

    def encode_flags(self):
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
        return flags