from os.path import basename

from data.Data import Data
from utils.Utils import select_file, get_file_content, print_color


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
    def save(self, folder_path: str = "."):
        if folder_path is None:
            folder_path = "."
        try:
            file_path = folder_path + "/" + self.name
            print_color("Saving " + self.name + " to " + file_path, color="green")
            with open(file_path, 'wb') as f:
                f.write(self.value)
        except Exception as e:
            print_color("Error saving file: " + str(e), color="red")

    def __str__(self):
        return "NAME: " + self.name + "\n" + "DATA: " + super().__str__()
