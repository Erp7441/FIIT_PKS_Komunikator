from binascii import crc32
from utils.Constants import ENCODING


class Data:
    def __init__(self, value=None):
        # If value is type of bytes
        if value is not None and isinstance(value, bytes):
            self.value = value
        # If value is not type of bytes convert it to bytes
        elif value is not None and not isinstance(value, bytes):
            self.value = bytes(value, ENCODING)
        # If value is None
        else:
            self.value = bytes("", ENCODING)

    def crc32(self):
        return crc32(self.value)

    def encode(self):
        return self.value.hex()

    def decode(self, encoded_data):
        self.value = bytes.fromhex(encoded_data)
        return self.value

    def __str__(self):
        return str(self.value.decode(ENCODING))
