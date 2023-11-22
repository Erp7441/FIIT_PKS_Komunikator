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
# Prints
###############################################
def print_color(*args, color="white", **kwargs):
    color_code = None

    if isinstance(color, int):
        if color < 0 or color > 255:
            raise ValueError(f"Invalid color code: {color}")
        color_code = f"38;5;{color}"
    elif isinstance(color, str):
        color_codes = {
            'black': '30',
            'red': '31',
            'green': '32',
            'yellow': '33',
            'blue': '34',
            'purple': '35',
            'cyan': '36',
            'white': '37',
            'orange': '38;5;208',
            'navy': '38;5;4',
            'teal': '38;5;6',
            'lime': '38;5;10',
            'fuchsia': '38;5;13',
            'aqua': '38;5;14',
            'gray': '38;5;16',
        }

        if color not in color_codes:
            raise ValueError(f"Invalid color: {color}")

        color_code = color_codes[color]

    if color_code is not None:
        message = " ".join(str(arg) for arg in args)
        print(f"\033[{color_code}m{message}\033[0m", **kwargs)


def print_debug(*args, color="yellow", **kwargs):
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"DEBUG [{timestamp}]: "
        message = " ".join(str(arg) for arg in args)
        print_color(prefix + message, color=color, **kwargs)


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


###############################################
# Object creation
###############################################
def create_settings():
    # TODO:: Implement settings dictionary creation
    # Settings
    # Pseudo idea
    # Provides variables with settings like
    # Port number
    # IP address
    # Segment size
    # Could be aggregated inside Sender or Receiver???
    pass

