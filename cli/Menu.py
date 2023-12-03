from utils.Utils import print_debug, get_integer_safely


class Menu:
    def __init__(self, title: str = ""):
        self.options = []  # List of tuples (label, function)
        self.title = title

    def add_option(self, label, function):
        self.options.append((label, function))

    def display(self, run_functions: list[callable] = None, on_close_functions: list[callable] = None):
        while True:
            print(self.title)
            # Execute all run functions before printing options
            Menu._execute_functions(run_functions)

            # Print options
            for i, option in enumerate(self.options, 1):
                print(f"{i}. {option[0]}")

            # Exit option is last element of the menu (static creation)
            print(f"{len(self.options) + 1}. Exit")

            # Get int from user
            choice = get_integer_safely(
                "Enter your choice: ",
                error_msg="Please enter a valid number.",
                condition=lambda x: 1 <= x <= len(self.options) + 1,
                verbose=False
            )

            # If an option from the list was selected
            if 1 <= choice <= len(self.options):
                selected_option = self.options[choice - 1]
                Menu._execute_functions([selected_option[1]])

            # Last option
            elif choice == len(self.options) + 1:
                # Execute all exit functions before quitting
                Menu._execute_functions(on_close_functions)
                return  # Exit option was selected

    @staticmethod
    def _execute_functions(functions):
        if functions is not None:
            try:
                for function in functions:
                    function()
            except Exception as e:
                print_debug(f"Error in function: {e}", color="red")
