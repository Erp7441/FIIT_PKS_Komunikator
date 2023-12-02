import os
import re
from datetime import datetime
from pathlib import Path
from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory
from typing import Callable

from utils.Constants import ENCODING, DEBUG, DEBUG_SHOW_DATA

###############################################
# Global variables
###############################################
debug = DEBUG  # Debug mode
debug_show_data = DEBUG_SHOW_DATA  # Show sent data in debug mode


###############################################
# Dialog windows
###############################################
def select_file(title="Select file"):
    root = Tk()
    root.withdraw()  # Hides the root window
    file = askopenfilename(title=title)  # Opens a file dialog
    return None if len(file) == 0 else file


def select_folder(title="Select folder"):
    root = Tk()
    root.withdraw()  # Hides the root window
    folder = askdirectory(title=title)  # Opens a file dialog
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
    if debug:
        timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
        prefix = f"DEBUG [{timestamp}]: "
        message = " ".join(str(arg) for arg in args)
        print_color(prefix + message, color=color, **kwargs)


def print_debug_data(*args, color="yellow", **kwargs):
    if debug_show_data:
        print_debug(args, color=color, **kwargs)


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
# Checks
###############################################
def is_valid_ipv4(ip):
    if ip is None or not isinstance(ip, str):
        return False
    ipv4_pattern = re.compile(
        r"^(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)\."
        r"(25[0-5]|2[0-4][0-9]|[0-1]?[0-9][0-9]?)$"
    )
    return bool(ipv4_pattern.match(ip))


def is_valid_confirmation(string: str):
    return string.lower() == "y" or string.lower() == "yes" or string.lower() == "n" or string.lower() == "no"


def is_valid_port(port: int):
    try:
        return 1 <= port <= 65535
    except ValueError:
        return False


def is_port_in_use(port: int, ip: str = "0.0.0.0"):
    if not is_valid_port(port) or not is_valid_ipv4(ip):
        return True

    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        try:
            s.bind(("127.0.0.1", port))
        except socket.error:
            return True
    return False


###############################################
# Getters
###############################################
def get_integer_safely(prompt: str, default: int = 0, condition: Callable[[int], bool] = lambda x: True, error_msg: str = "", verbose: bool = True) -> int:
    while True:
        try:
            print_color(prompt, color="yellow", end="")
            value = input()

            if value is not None and value != "":
                value = value.strip()
                value = int(value)
            else:
                if verbose:
                    print_color(f"Using default value: {default}", color="yellow")
                value = default

            if not condition(value):
                raise ValueError(error_msg)

            return value
        except ValueError as e:
            if error_msg is not None and error_msg != "":
                print_color(f"Invalid input: \"{e}\"", color="red")
            else:
                print_color("Invalid input", color="red")


def get_string_safely(prompt: str, default: str = "", condition: Callable[[str], bool] = lambda x: True, error_msg: str = "") -> str:
    while True:
        try:
            print_color(prompt, color="yellow", end="")
            value = input()

            if value is not None and value != "":
                value = value.strip()
            else:
                print_color(f"Using default value: {default}", color="yellow")
                value = default

            if not condition(value):
                raise ValueError(error_msg)

            return value
        except ValueError as e:
            print_color(f"Invalid input: {e}... Please try again.", color="red")


def get_list_safely(prompt: str, default=None, unique=False) -> list:
    if default is None:
        default = []

    while True:
        try:
            print_color(prompt, color="yellow", end="")
            arr = input()

            if arr is not None and arr != "":
                arr = arr.strip()
                arr = [int(x.strip()) for x in arr.split(',')]
            else:
                print_color(f"Using default list: {default}", color="yellow")
                arr = default

            if unique:
                arr = list(set(arr))
            return arr
        except ValueError as e:
            print_color(f"Invalid input: {e}... Please try again.", color="red")


# Gets current system downloads folder
def get_downloads_folder():
    user_home = str(Path.home())

    # Check the operating system
    if os.name == 'posix':  # Linux, macOS
        return os.path.join(user_home, 'Downloads')
    elif os.name == 'nt':  # Windows
        return os.path.join(user_home, 'Downloads')
    elif os.name == 'os2':  # OS/2
        return os.path.join(user_home, 'Downloads')
    elif os.name == 'ce':  # Windows CE
        return os.path.join(user_home, 'Downloads')
    else:
        # Handle other operating systems
        return None


# Reads file into a variable then closes it.
def get_file_content(path: str):
    file = open(path, 'rb')
    content = file.read()
    file.close()
    return content


def get_confirmation(prompt: str):
    return get_string_safely(
        prompt,
        error_msg="Invalid input",
        condition=lambda x: is_valid_confirmation(x)
    )


def get_debug_mode(output=True):
    if output:
        if debug:
            print_color("Debug output: Enabled", color="green")
        else:
            print_color("Debug output: Disabled", color="red")
        if debug_show_data:
            print_color("Debug output with data values: Enabled", color="green")
        else:
            print_color("Debug output with data values: Disabled", color="red")
    return debug, debug_show_data


###############################################
# Setters
################################################
def toggle_debug_mode():
    global debug
    debug = not debug

    if debug:
        global debug_show_data
        debug_show_data = get_confirmation("Do you want to enable debug output with data values? (y/n): ") == "y"
    else:
        debug_show_data = False

    return get_debug_mode()

