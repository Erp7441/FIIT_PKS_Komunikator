from cli.Menu import Menu
from cli.Settings import Settings
from modes.Receiver import Receiver
from modes.Sender import Sender
from utils.Constants import DEFAULT_SERVER_IP
from utils.Utils import print_color, toggle_debug_mode, get_debug_mode, print_debug


def run_receiver_mode(settings: Settings):
    print_debug("Starting receiver mode...")
    if settings.ip is None:
        settings.get_ip()
    if settings.downloads_dir is None:
        settings.get_downloads_folder()
    receiver = Receiver(settings=settings)
    try:
        receiver.close()
    except Exception:
        pass


def run_sender_mode(settings: Settings):
    print_debug("Starting sender mode...")
    if settings.ip is None:
        settings.get_ip()
    sender = Sender(settings=settings)

    sender_sub_menu = Menu("Sender sub menu")
    sender_sub_menu.add_option("Send file", lambda: sender.send_file())
    sender_sub_menu.add_option("Send message", lambda: sender.send_message())
    sender_sub_menu.add_option("Swap roles", lambda: sender.connection_manager.initiate_swap(sender.get_current_connection()))
    sender_sub_menu.display(
        run_functions=[
            lambda: print_color(sender.get_current_connection().stats(), color="blue")
        ],
        on_close_functions=[
            lambda: sender.close()
        ]
    )

    try:
        sender.close()
    except Exception:
        pass

def show_sender_menu():
    sender_menu = Menu("Sender menu")
    settings = Settings()

    sender_menu.add_option("Connect", lambda: run_sender_mode(settings))
    sender_menu.add_option("Show settings", lambda: print("Current settings:\n" + str(settings)))
    sender_menu.add_option("Modify settings", lambda: settings.modify_settings())
    sender_menu.display()


def show_receiver_menu():
    receiver_menu = Menu("Receiver menu")
    settings = Settings(ip=DEFAULT_SERVER_IP)

    receiver_menu.add_option("Start", lambda: run_receiver_mode(settings))
    receiver_menu.add_option("Show settings", lambda: print("Current settings:\n" + str(settings)))
    receiver_menu.add_option("Modify settings", lambda: settings.modify_settings())
    receiver_menu.display()


def show_main_menu():
    get_debug_mode()
    main_menu = Menu("Main menu")
    main_menu.add_option("Run Receiver Mode", show_receiver_menu)
    main_menu.add_option("Run Sender Mode", show_sender_menu)
    main_menu.add_option("Toggle Debug Output", toggle_debug_mode)
    main_menu.display()
    # TODO:: Resolve hanging on main menu when swapped roles trying to exit the program
