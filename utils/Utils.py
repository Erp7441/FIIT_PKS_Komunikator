from datetime import datetime
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory

from utils.Constants import DEBUG
from utils.Constants import ENCODING


###############################################
# Dialog windows
###############################################
def select_file():
    root = Tk()
    root.withdraw()  # Hides the root window
    file = askopenfilename(title="Select file")  # Opens a file dialog
    return None if len(file) == 0 else file


def select_folder():
    root = Tk()
    root.withdraw()  # Hides the root window
    folder = askdirectory(title="Select folder")  # Opens a file dialog
    return None if len(folder) == 0 else folder


###############################################
# Debug
###############################################
def print_debug(*args, **kwargs):
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"DEBUG [{timestamp}]: "
        message = " ".join(str(arg) for arg in args)
        print(prefix + message, **kwargs)


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


# Tries to convert any data type into bytes
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
