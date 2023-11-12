from data.Data import Data
from utils.Coder import decode_part, encode_str_to_hex
from utils.Dialog import select_file
from os.path import basename
from utils.Constants import NAME_HEX_HEADER


# Reads file into a variable then closes it.
def read_file(path, mode: str = 'rb'):
    file = open(path, mode)
    content = file.read()
    file.close()
    return content


class File(Data):
    def __init__(self, path: str = None, select: bool = False):
        if select is True:
            path = select_file()

        if path is not None:
            super(File, self).__init__(read_file(path))
            self.name = basename(path)
        else:
            super(File, self).__init__()
            self.name = ""

    # Encodes file into hexadecimal string
    def encode(self):
        encoded_name = encode_str_to_hex(self.name) + NAME_HEX_HEADER  # Encodes name within the hex string
        encoded_data = encoded_name + super(File, self).encode()
        return encoded_data

    # Decodes hexadecimal string to data bytes (including name)
    def decode(self, encoded_data):
        self.name, data = decode_part(NAME_HEX_HEADER, encoded_data)  # Decodes name and removes its header from data
        return super(File, self).decode(data)  # Decode rest of the data

    # Saves current file object to a folder
    def save(self, folder_path):
        with open(folder_path + "/" + self.name, 'wb') as f:
            f.write(self.value)
