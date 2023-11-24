from utils.Utils import print_debug


class Menu:
    def __init__(self, title: str = ""):
        self.options = []  # List of tuples (label, function)
        self.title = title

    def add_option(self, label, function):
        self.options.append((label, function))

    def display(self, on_close_function=None):
        while True:
            print(self.title)

            # Print options
            for i, option in enumerate(self.options, 1):
                print(f"{i}. {option[0]}")

            # Exit option is last element of the menu (static creation)
            print(f"{len(self.options) + 1}. Exit")

            choice = input("Enter your choice: ")

            try:
                choice = int(choice)
            except ValueError:
                print("Invalid choice. Please enter a number.")
                continue

            if 1 <= choice <= len(self.options):
                selected_option = self.options[choice - 1]
                selected_option[1]()
            elif choice == len(self.options) + 1:
                if on_close_function is not None:
                    try:
                        on_close_function()
                    except Exception as e:
                        print_debug(f"Error in on_close_function: {e}", color="red")
                return  # Exit option was selected
            else:
                print("Invalid choice. Please enter a valid number.")
