from cli.Menu import Menu
from utils.Constants import DEFAULT_PORT, MAX_SEGMENT_SIZE, SENDER_BAD_PACKETS_SEQ, SENDER_BAD_PACKETS_ATTEMPTS, \
    RESEND_ATTEMPTS, NACK_RESPONSE_MULTIPLIER
from utils.Utils import is_valid_ipv4, get_integer_safely, get_list_safely, get_string_safely, \
    get_downloads_folder, select_folder, convert_bytes_to_str, convert_str_to_bytes


class Settings:

    def __init__(
        self,
        ip: str = None,
        port: int = DEFAULT_PORT,
        packet_resend_attempts: int = RESEND_ATTEMPTS,
        bad_packets_seq: list = SENDER_BAD_PACKETS_SEQ,
        bad_packets_attempts: int = SENDER_BAD_PACKETS_ATTEMPTS,
        segment_size: int = MAX_SEGMENT_SIZE,
        nack_response_multiplier: int = NACK_RESPONSE_MULTIPLIER,
        downloads_dir: str = None
    ):
        self.ip = ip
        self.port = port
        self.packet_resend_attempts = packet_resend_attempts
        self.bad_packets_seq = bad_packets_seq
        self.bad_packets_attempts = bad_packets_attempts
        self.segment_size = segment_size
        self.nack_response_multiplier = nack_response_multiplier
        self.downloads_dir = get_downloads_folder() if downloads_dir is None else downloads_dir
        self._initialized = False if ip is None else True

    # Initialize all needed settings
    def get_all(self):
        self.get_ip()
        self.get_port()
        self.get_segment_size()

    def get_ip(self):
        self.ip = get_string_safely("Please enter IP address: ", DEFAULT_PORT, lambda x: is_valid_ipv4(x),
                                    "Invalid IP address")
        self._initialized = True

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
        self.bad_packets_seq = get_list_safely("Please enter comma separated list of SEQ numbers: ",
                                               SENDER_BAD_PACKETS_SEQ, unique=True)

    def get_bad_packets_attempts(self):
        self.bad_packets_attempts = get_integer_safely("Please enter bad packets resend attempts: ",
                                                       SENDER_BAD_PACKETS_ATTEMPTS)

    def get_packet_resend_attempts(self):
        self.packet_resend_attempts = get_integer_safely("Please enter packet resend attempts: ", RESEND_ATTEMPTS)

    def get_nack_response_multiplier(self):
        self.nack_response_multiplier = get_integer_safely("Please enter nack response multiplier: ",
                                                           NACK_RESPONSE_MULTIPLIER)

    def get_downloads_folder(self):
        self.downloads_dir = select_folder("Please select downloads folder")

    def modify_settings(self):
        if self._initialized is False:
            self.get_all()
            return

        modify_menu = Menu(title="Modify settings")

        # Each attribute has an option
        modify_menu.add_option("IP", lambda: self.get_ip())
        modify_menu.add_option("Port", lambda: self.get_port())
        modify_menu.add_option("Segment size", lambda: self.get_segment_size())
        modify_menu.add_option("Bad packets SEQ numbers", lambda: self.get_bad_packets_seq())
        modify_menu.add_option("Bad packets resend attempts", lambda: self.get_bad_packets_attempts())
        modify_menu.add_option("Packet resend attempts", lambda: self.get_packet_resend_attempts())
        modify_menu.add_option("NACK response multiplier", lambda: self.get_nack_response_multiplier())
        modify_menu.add_option("Download folder", lambda: self.get_downloads_folder())

        modify_menu.display()

    def __str__(self):
        return f"IP: {self.ip}\n" \
               f"Port: {self.port}\n" \
               f"Segment size: {self.segment_size}\n" \
               f"Bad packets seq: {self.bad_packets_seq}\n" \
               f"Bad packets send attempts: {self.bad_packets_attempts}\n" \
               f"Packet resend attempts: {self.packet_resend_attempts}\n" \
               f"NACK response multiplier: {self.nack_response_multiplier}\n" \
               f"Downloads folder: {self.downloads_dir}"

    def encode(self):
        _str = (
            str(self.ip) + ';'
            + str(self.port) + ';'
            + str(self.segment_size) + ';'
            + str(self.bad_packets_seq) + ';'
            + str(self.bad_packets_attempts) + ';'
            + str(self.packet_resend_attempts) + ';'
            + str(self.nack_response_multiplier) + ';'
        )
        return convert_str_to_bytes(_str)

    def decode(self, data):
        data = convert_bytes_to_str(data).split(';')
        self.ip = data[0]
        self.port = data[1]
        self.segment_size = data[2]
        self.bad_packets_seq = data[3]
        self.bad_packets_attempts = data[4]
        self.packet_resend_attempts = data[5]
        self.nack_response_multiplier = data[6]
