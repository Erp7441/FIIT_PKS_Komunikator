from utils.Constants import ENCODE_DICT
from utils.Utils import convert_bytes_to_str, convert_str_to_bytes, convert_any_to_bytes, get_enc_data


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
        if ENCODE_DICT.get("encode_data", False):
            return get_enc_data(self.value, ENCODE_DICT.get("step", 3), ENCODE_DICT.get("right", True))[0]
        return self.value

    def decode(self, encoded_data: bytes):
        if ENCODE_DICT.get("encode_data", False):
            self.value = get_enc_data(encoded_data, -ENCODE_DICT.get("step", 3), ENCODE_DICT.get("right", True))[0]
        else:
            self.value = encoded_data
        return self

    # Convert data bytes into string
    def __str__(self):
        return convert_bytes_to_str(self.value)

    def __bytes__(self):
        return self.value
