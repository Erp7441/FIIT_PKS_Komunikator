from modes.Receiver import Receiver
from modes.Sender import Sender
from utils.Menu import Menu
from utils.Settings import Settings


# LAB IPs
# 192.168.48.128 - Server
# 192.168.48.129 - Client

# TODO:: Check if connection reset from server side works. (Case where client connection dies suddenly)


def run_receiver_mode():
    Receiver()


def run_sender_mode(settings):
    if settings.ip is None:
        settings.get_ip()
    sender = Sender(settings=settings)

    sender_sub_menu = Menu("Sender sub menu")
    sender_sub_menu.add_option("Send file", lambda: sender.send_file())
    sender_sub_menu.add_option("Send message", lambda: sender.send_message())
    sender_sub_menu.display()


def show_sender_menu():
    sender_menu = Menu("Sender menu")
    settings = Settings()

    sender_menu.add_option("Run", lambda: run_sender_mode(settings))
    sender_menu.add_option("Show settings", lambda: print("Current settings:\n" + str(settings)))
    sender_menu.add_option("Modify settings", lambda: settings.modify_settings())
    sender_menu.display()


def run_test_mode():
    #from utils.Tests import Tests
    from utils.Tests import Tests
    #Tests.connection_tests_establishment_data()
    Tests.data_resassembly_test()
    #Tests.packet_tests()
    #Tests.test_string_conversion()


if __name__ == "__main__":
    menu = Menu("Main menu")
    menu.add_option("Run Receiver Mode", run_receiver_mode)
    menu.add_option("Run Sender Mode", show_sender_menu)
    menu.add_option("Run Test Mode", run_test_mode)
    menu.display()

