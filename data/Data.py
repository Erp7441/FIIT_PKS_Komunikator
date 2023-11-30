from utils.Utils import convert_bytes_to_str, convert_str_to_bytes, convert_any_to_bytes


class Data:
    def __init__(self, value=None):
        # Value is type of bytes to represent many data structures
        if value is None:
            self.value = b''
        elif isinstance(value, bytes):
            self.value = value
        elif isinstance(value, str):
            self.value = convert_str_to_bytes(value)
        else:
            self.value = convert_any_to_bytes(value)

    def encode(self):
        return self.value

    def decode(self, encoded_data: bytes):
        self.value = encoded_data
        return self

    # Convert data bytes into string
    def __str__(self):
        return convert_bytes_to_str(self.value)

    def __bytes__(self):
        return self.value
