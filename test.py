import tkinter as tk
from utils.Utils import print_debug, get_integer_safely

class MenuItem:
    def __init__(self, label, function=None, waiting=False, duration=5, is_submenu=False):
        self.label = label
        self.function = function
        self.waiting = waiting
        self.duration = duration
        self.is_submenu = is_submenu

class Menu:
    def __init__(self, title: str = "", parent_menu=None):
        self.items = []  # List of MenuItem instances
        self.title = title
        self.parent_menu = parent_menu

    def add_option(self, label, function, waiting=False, duration=5):
        option = MenuItem(label, function, waiting, duration)
        self.items.append(option)

    def add_submenu(self, submenu):
        submenu.is_submenu = True
        self.items.append(submenu)

    def add_back_option(self):
        back_option = MenuItem("Back", function=self.display)
        self.items.append(back_option)

    def display(self, run_functions: list[callable] = None, on_close_functions: list[callable] = None):
        menu_window = MenuWindow(self, window_size=(400, 300))  # Adjust window size here
        menu_window.run(run_functions=run_functions, on_close_functions=on_close_functions)

class MenuWindow:
    active_windows = []

    def __init__(self, menu, window_size=(300, 200)):
        self.menu = menu
        self.root = tk.Tk()
        self.root.title(menu.title)
        self.root.geometry(f"{window_size[0]}x{window_size[1]}")
        self.widgets = []
        MenuWindow.active_windows.append(self)

    def create_widgets(self):
        # Label to display the menu title
        title_label = tk.Label(self.root, text=self.menu.title, font=("Helvetica", 16))
        title_label.pack(pady=10)
        self.widgets.append(title_label)

        # Buttons for options and submenus
        for i, item in enumerate(self.menu.items, 1):
            if isinstance(item, MenuItem):
                button_text = f"{i}. {item.label}"
                if item.waiting:
                    button_text += " (Waiting)"
                button = tk.Button(self.root, text=button_text, command=lambda o=item: self.execute_selected_option(o))
                button.pack(pady=5)
                self.widgets.append(button)

        # Exit button
        exit_button = tk.Button(self.root, text=f"{len(self.menu.items) + 1}. Exit", command=self.close_window)
        exit_button.pack(pady=5)
        self.widgets.append(exit_button)

    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def execute_selected_option(self, selected_option):
        try:
            if isinstance(selected_option, MenuItem):
                if selected_option.is_submenu:
                    self.display_submenu(selected_option)
                else:
                    if selected_option.waiting:
                        self.hide_window()
                        self.root.after(0, lambda: self.run_waiting_function(selected_option.function, selected_option.duration))
                    else:
                        selected_option.function()
        except Exception as e:
            print_debug(f"Error in function: {e}", color="red")

    def run_waiting_function(self, function, duration):
        function()
        self.show_window()

    def display_submenu(self, submenu):
        self.menu = submenu
        self.clear_widgets()
        self.create_widgets()

    def close_window(self):
        self.root.destroy()

    def hide_window(self):
        self.root.withdraw()

    def show_window(self):
        self.root.update()
        self.root.deiconify()

    def run(self, run_functions=None, on_close_functions=None):
        self.create_widgets()
        self._execute_functions(run_functions)
        self.root.mainloop()
        self._execute_functions(on_close_functions)

    def _execute_functions(self, functions):
        if functions is not None:
            try:
                for function in functions:
                    function()
            except Exception as e:
                print_debug(f"Error in function: {e}", color="red")

    @staticmethod
    def close_all_windows():
        for window in MenuWindow.active_windows:
            window.root.destroy()


# Example Usage:

def run_function1():
    print("Running function 1")

def run_function2():
    print("Running function 2")

def waiting_function():
    print("Waiting function")

def on_close_function():
    print("Executing on close function")

main_menu = Menu("Main Menu")

submenu = Menu("SubMenu", parent_menu=main_menu)
submenu.add_option("SubOption 1", lambda: print("SubOption 1 selected"))
submenu.add_option("SubOption 2", lambda: print("SubOption 2 selected"))
submenu.add_back_option()

main_menu.add_option("Option 1", lambda: print("Option 1 selected"))
main_menu.add_option("Option 2", lambda: print("Option 2 selected"))
main_menu.add_option("Waiting Option", waiting_function, waiting=True, duration=5)
main_menu.add_submenu(submenu)

menu_window = MenuWindow(main_menu, window_size=(400, 300))
MenuWindow.active_windows.append(menu_window)
menu_window.run(run_functions=[run_function1, run_function2], on_close_functions=[on_close_function])

# Close all active windows
MenuWindow.close_all_windows()
