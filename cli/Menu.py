import tkinter as tk
import time
from utils.Utils import print_debug, get_integer_safely

class Menu:
    def __init__(self, title: str = ""):
        self.options = []  # List of Option instances
        self.submenus = []  # List of Menu instances for submenus
        self.title = title

    def add_option(self, label, function, waiting=False, duration=0):
        option = Option(label, function, waiting, duration)
        self.options.append(option)

    def add_submenu(self, submenu):
        submenu.parent_menu = self
        self.submenus.append(submenu)

    def display(self, run_functions: list[callable] = None, on_close_functions: list[callable] = None):
        menu_window = MenuWindow(self, window_size=(400, 300))  # Adjust window size here
        menu_window.run(run_functions=run_functions, on_close_functions=on_close_functions)

class Option:
    def __init__(self, label, function, waiting=False, duration=0):
        self.label = label
        self.function = function
        self.waiting = waiting
        self.duration = duration

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

        # Buttons for menu options
        for i, option in enumerate(self.menu.options, 1):
            button_text = f"{i}. {option.label}"
            if option.waiting:
                button_text += " (Waiting)"
            button = tk.Button(self.root, text=button_text, command=lambda o=option: self.execute_selected_option(o))
            button.pack(pady=5)
            self.widgets.append(button)

        # Buttons for submenu options
        for i, submenu in enumerate(self.menu.submenus, len(self.menu.options) + 1):
            button = tk.Button(self.root, text=f"{i}. {submenu.title}", command=lambda s=submenu: self.display_submenu(s))
            button.pack(pady=5)
            self.widgets.append(button)

        # Exit button
        exit_button = tk.Button(self.root, text=f"{len(self.menu.options) + len(self.menu.submenus) + 1}. Exit", command=self.close_window)
        exit_button.pack(pady=5)
        self.widgets.append(exit_button)

        # Back button for submenus
        if isinstance(self.menu, SubMenu):
            back_button = tk.Button(self.root, text=f"{len(self.menu.options) + len(self.menu.submenus) + 2}. Back", command=self.display_parent_menu)
            back_button.pack(pady=5)
            self.widgets.append(back_button)

    def clear_widgets(self):
        for widget in self.widgets:
            widget.destroy()

    def execute_selected_option(self, selected_option):
        try:
            if selected_option.waiting:
                self.hide_window()
                self.root.after(int(selected_option.duration * 1000), lambda: self.run_waiting_function(selected_option.function))
            else:
                selected_option.function()
        except Exception as e:
            print_debug(f"Error in function: {e}", color="red")

    def run_waiting_function(self, function):
        function()
        self.show_window()

    def display_submenu(self, submenu):
        self.menu = submenu
        self.clear_widgets()
        self.create_widgets()

    def display_parent_menu(self):
        if isinstance(self.menu, SubMenu):
            parent_menu = self.menu.parent_menu
            self.menu = parent_menu
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
        # Execute all run functions before displaying the window
        self.create_widgets()
        self._execute_functions(run_functions)

        # Start the Tkinter event loop
        self.root.mainloop()

        # Execute all exit functions before quitting
        self._execute_functions(on_close_functions)

    def _execute_functions(self, functions):
        if functions is not None:
            try:
                for function in functions:
                    function()
            except Exception as e:
                print_debug(f"Error in function: {e}", color="red")
    def close_all_windows():
        for window in MenuWindow.active_windows:
            window.root.destroy()


# SubMenu class to represent a submenu
class SubMenu(Menu):
    def __init__(self, title: str = "", parent_menu=None):
        super().__init__(title)
        self.parent_menu = parent_menu  # Reference to the parent menu

