from utils.Constants import DEFAULT_PORT, MAX_SEGMENT_SIZE, SENDER_BAD_PACKETS_SEQ, SENDER_BAD_PACKETS_ATTEMPTS, \
    RESEND_ATTEMPTS, NACK_RESPONSE_MULTIPLIER
from cli.Menu import Menu
from utils.Utils import is_valid_ipv4, print_color, get_integer_safely, get_list_safely, get_string_safely, \
    get_downloads_folder


class Settings:

    def __init__(self):
        self.ip = None
        self.port = DEFAULT_PORT
        self.packet_resend_attempts = RESEND_ATTEMPTS
        self.bad_packets_seq = SENDER_BAD_PACKETS_SEQ
        self.bad_packets_attempts = SENDER_BAD_PACKETS_ATTEMPTS
        self.segment_size = MAX_SEGMENT_SIZE
        self.nack_response_multiplier = NACK_RESPONSE_MULTIPLIER
        self.downloads_dir = get_downloads_folder()
        self._initialized = False

    def get_all(self):
        self.get_ip()
        self.get_port()
        self.get_segment_size()
        self._initialized = True

    def get_ip(self):
        self.ip = get_string_safely("Please enter IP address: ", DEFAULT_PORT, lambda x: is_valid_ipv4(x), "Invalid IP address")

    def get_port(self):
        self.port = get_integer_safely(
            "Please enter port number: ", DEFAULT_PORT,
                    lambda x: x <= DEFAULT_PORT, "Port number must be less or equal to " + str(65535)
        )

    def get_segment_size(self):
        self.segment_size = get_integer_safely(
            "Please enter segment size: ", MAX_SEGMENT_SIZE,
                    lambda x: x <= MAX_SEGMENT_SIZE, "Segment size must be less than " + str(MAX_SEGMENT_SIZE)
        )

    def get_bad_packets_seq(self):
        self.bad_packets_seq = get_list_safely("Please enter comma separated list of SEQ numbers: ", SENDER_BAD_PACKETS_SEQ, unique=True)

    def get_bad_packets_attempts(self):
        self.bad_packets_attempts = get_integer_safely("Please enter bad packets resend attempts: ", SENDER_BAD_PACKETS_ATTEMPTS)

    def get_packet_resend_attempts(self):
        self.packet_resend_attempts = get_integer_safely("Please enter packet resend attempts: ", RESEND_ATTEMPTS)

    def get_nack_response_multiplier(self):
        while True:
            try:
                print_color("Please enter bad packets resend attempts: ", color="yellow", end="")
                nack_response_multiplier = input()

                if nack_response_multiplier is not None and nack_response_multiplier != "":
                    nack_response_multiplier = nack_response_multiplier.strip()
                    nack_response_multiplier = int(nack_response_multiplier)
                else:
                    print_color(f"Using default bad packets resend attempts: {NACK_RESPONSE_MULTIPLIER}", color="yellow")
                    nack_response_multiplier = NACK_RESPONSE_MULTIPLIER

                self.nack_response_multiplier = nack_response_multiplier
                break
            except ValueError as e:
                print_color(f"Invalid input: {e}... Please try again.", color="red")

    def modify_settings(self):
        if self._initialized is False:
            self.get_all()
            return

        modify_menu = Menu(title="Modify settings")

        modify_menu.add_option("IP", lambda: self.get_ip())
        modify_menu.add_option("Port", lambda: self.get_port())
        modify_menu.add_option("Segment size", lambda: self.get_segment_size())
        modify_menu.add_option("Bad packets SEQ numbers", lambda: self.get_bad_packets_seq())
        modify_menu.add_option("Bad packets resend attempts", lambda: self.get_bad_packets_attempts())
        modify_menu.add_option("Packet resend attempts", lambda: self.get_packet_resend_attempts())
        modify_menu.add_option("NACK response multiplier", lambda: self.get_nack_response_multiplier())
        modify_menu.display()

    def __str__(self):
        return  f"IP: {self.ip}\n" \
                f"Port: {self.port}\n" \
                f"Segment size: {self.segment_size}\n" \
                f"Bad packets seq: {self.bad_packets_seq}\n" \
                f"Bad packets send attempts: {self.bad_packets_attempts}\n" \
                f"Packet resend attempts: {self.packet_resend_attempts}\n" \
                f"NACK response multiplier: {self.nack_response_multiplier}\n"
