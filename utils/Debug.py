from utils.Constants import DEBUG

from datetime import datetime


def print_debug(*args, **kwargs):
    if DEBUG:
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = f"DEBUG [{timestamp}]: "
        message = " ".join(str(arg) for arg in args)
        print(prefix + message, **kwargs)