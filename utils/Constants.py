###############################################
# Communication
###############################################
ENCODING = 'utf-8'
DEFAULT_PORT = 33333
DEFAULT_SERVER_IP = "0.0.0.0"
RESEND_ATTEMPTS = 3  # Tries

# Keepalive
DEFAULT_KEEPALIVE_TIME = 5  # Seconds
DEFAULT_KEEPALIVE_REFRESH_ATTEMPTS = 3  # TODO:: Implement or remove?

# Sender
SENDER_SOCKET_TIMEOUT = 5  # Seconds
SENDER_BAD_PACKETS_SEQ = [3, 8, 6, 7]  # SEQ numbers
SENDER_BAD_PACKETS_ATTEMPTS = 3  # Tries
NACK_RESPONSE_MULTIPLIER = 5  # Packets

# File
MAX_FILE_SIZE = 2097152  # Bytes

###############################################
# DEBUG
###############################################
DEBUG = True  # Debug mode
DEBUG_SHOW_DATA = False  # Show sent data in debug mode

###############################################
# Segment
###############################################
SEQ_SIZE = 3  # Bytes
CRC_SIZE = 4  # Bytes
FLAGS_SIZE = 2  # Bytes

MTU = 1500  # MTU is 1500 bytes by default
ETHERNET_HEADER_LENGTH = 14  # Bytes
MIN_IP_HEADER_LENGTH = 20  # Bytes
MAX_IP_HEADER_LENGTH = 60  # Bytes
UDP_HEADER_LENGTH = 8  # Bytes
IP_HEADER_LENGTH = MIN_IP_HEADER_LENGTH  # We'll count with minimum IP header length
OFFSET = 9  # Bytes

###############################################
# Calculated constants
###############################################
MAX_SEGMENT_SIZE = MTU - ETHERNET_HEADER_LENGTH - IP_HEADER_LENGTH - UDP_HEADER_LENGTH - OFFSET  # Bytes
MAX_PAYLOAD_SIZE = MAX_SEGMENT_SIZE - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE  # Bytes

RECEIVER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME + 1  # Seconds (Integer)
SENDER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME  # Seconds (Integer)
