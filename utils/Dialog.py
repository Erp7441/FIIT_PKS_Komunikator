from tkinter import Tk
from tkinter.filedialog import askopenfilename, askdirectory


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