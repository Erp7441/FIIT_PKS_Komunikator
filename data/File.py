from os.path import basename

from data.Data import Data
from utils.Utils import select_file, get_file_content


class File(Data):
    def __init__(self, path: str = None, select: bool = False, name: str = ""):
        if select is True:
            path = select_file()

        if path is not None:
            super(File, self).__init__(get_file_content(path))
            self.name = basename(path)
        else:
            super(File, self).__init__()
            self.name = name

    def encode(self):
        return super(File, self).encode()

    def decode(self, encoded_data):
        return super(File, self).decode(encoded_data)

    # Saves current file object to a folder
    def save(self, folder_path):
        with open(folder_path + "/" + self.name, 'wb') as f:
            f.write(self.value)

    def __str__(self):
        return "NAME: " + self.name + "\n" + "DATA: " + super().__str__()
