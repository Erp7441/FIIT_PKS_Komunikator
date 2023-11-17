from binascii import crc32

from utils.Utils import decode_str_from_bytes, encode_str_to_bytes, encode_any_to_bytes


# TODO:: Add info packet, with dict about data to be transmitted


class Data:
    def __init__(self, value=None):
        # Value is type of bytes to represent many data structures
        if value is None:
            self.value = b''
        elif isinstance(value, bytes):
            self.value = value
        elif isinstance(value, str):
            self.value = encode_str_to_bytes(value)
        else:
            self.value = encode_any_to_bytes(value)

    # Calculates CRC32 of the data
    def crc32(self):
        return crc32(self.value)

    # TODO:: Add encoding?
    def encode(self):
        return self.value

    # TODO:: Add decoding?
    def decode(self, encoded_data: str):
        self.value = encoded_data
        return self

    # Convert data bytes into string
    def __str__(self):
        return decode_str_from_bytes(self.value)

    def __bytes__(self):
        return self.value
