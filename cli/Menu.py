class Menu:
    def __init__(self, title:str = ""):
        self.options = []
        self.title = title

    def add_option(self, label, function):
        self.options.append((label, function))

    def display(self):
        while True:
            print(self.title)
            for i, option in enumerate(self.options, 1):
                print(f"{i}. {option[0]}")

            # Exit option is last element of the list
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
                return
            else:
                print("Invalid choice. Please enter a valid number.")
