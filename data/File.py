import os.path

from data.Data import Data
from tkinter import Tk
from tkinter.filedialog import askopenfilename

from utils.Constants import ENCODING


def select_file():
    root = Tk()
    root.withdraw()  # Hides the root window
    file = askopenfilename(title="Select file")  # Opens a file dialog
    return None if len(file) == 0 else file


# Decodes part of hex data string
def decode_part(part_name: str, data):
    if data is None:
        return
    encoded_part = data[:data.index(part_name)]
    data = data[len(encoded_part+part_name):]  # Removes data header from the hex data string
    return bytes.fromhex(encoded_part).decode(ENCODING), data  # Return extracted data along with modified hex string


class File(Data):
    def __init__(self, path=None, select=True):
        if select is True:
            path = select_file()

        if path is not None and isinstance(path, str):
            file = open(path, 'rb')
            super(File, self).__init__(file.read())
            file.close()

            self.name = os.path.basename(path)
        else:
            super(File, self).__init__()
            self.name = ""

    # Encodes file into hexadecimal string
    def encode(self):
        encoded_name = self.name.encode(ENCODING).hex() + "NAME"  # Encodes name within the hex string
        encoded_data = encoded_name + super(File, self).encode()
        return encoded_data

    # Decodes hexadecimal string to data bytes (including name)
    def decode(self, encoded_data):
        self.name, data = decode_part("NAME", encoded_data)  # Decodes name and removes its header from data
        return super(File, self).decode(data)  # Decode rest of the data

    # Saves current file object to a folder
    def save(self, folder_path):
        with open(folder_path + "/" + self.name, 'wb') as f:
            f.write(self.value)
