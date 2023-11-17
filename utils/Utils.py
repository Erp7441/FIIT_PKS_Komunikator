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
# Conversions
###############################################
def convert_bytes_to_str(bytes_data: bytes):
    return str(bytes_data.decode(ENCODING))


def convert_str_to_bytes(str_data: str):
    return bytes(str_data, ENCODING)


def convert_bytes_to_int(value: bytes):
    return int.from_bytes(value, "big")


def convert_int_to_bytes(value: int, length: int = 4):
    return value.to_bytes(length, "big")


# Tries to convert any data type into bytes
def convert_any_to_bytes(value):
    try:
        if isinstance(value, bytes):
            return value
        elif isinstance(value, int):
            return convert_int_to_bytes(value)
        else:
            return convert_str_to_bytes(str(value))
    except (TypeError, ValueError):
        return None



