from utils.Constants import ENCODING


###############################################
# Decoding
###############################################
def decode_str_from_bytes(bytes_data: bytes):
    return str(bytes_data.decode(ENCODING))


def decode_bytes_from_hex(hex_data: str):
    return bytes.fromhex(hex_data)


def decode_str_from_hex(hex_data: str):
    bytes_data = decode_bytes_from_hex(hex_data)
    return decode_str_from_bytes(bytes_data)


def decode_int_from_hex(hex_data: str):
    return int.from_bytes(decode_bytes_from_hex(hex_data))


# Decodes part of hex data string
def decode_part(part_name: str, data):
    if data is None:
        return
    encoded_part = data[:data.index(part_name)]
    data = data[len(encoded_part+part_name):]  # Removes data header from the hex data string
    return decode_str_from_hex(encoded_part), data  # Return extracted data along with modified hex string


###############################################
# Encoding
###############################################
def encode_str_to_bytes(str_data: str):
    return bytes(str_data, ENCODING)


def encode_bytes_to_hex(bytes_data: bytes):
    return bytes_data.hex()


def encode_str_to_hex(str_data: str):
    bytes_data = encode_str_to_bytes(str_data)
    return encode_bytes_to_hex(bytes_data)


def encode_any_to_bytes(value):
    try:
        if isinstance(value, bytes):
            return value
        else:
            return encode_str_to_bytes(str(value))
    except (TypeError, ValueError):
        return None


def encode_int_to_hex(value: int, length: int = 4):
    return encode_bytes_to_hex(value.to_bytes(length, "big"))