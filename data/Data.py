from binascii import crc32

from utils.Coder import decode_bytes_from_hex, encode_bytes_to_hex, decode_str_from_bytes, encode_str_to_bytes, encode_any_to_bytes


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

    # Encodes data bytes into hex string
    def encode(self):
        return encode_bytes_to_hex(self.value)

    # Decodes hex string into data bytes
    def decode(self, encoded_data: str):
        self.value = decode_bytes_from_hex(encoded_data)
        return self.value

    # Convert data bytes into string
    def __str__(self):
        return decode_str_from_bytes(self.value)

    def __bytes__(self):
        return self.value
