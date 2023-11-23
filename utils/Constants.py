ENCODING = 'utf-8'
DEFAULT_PORT = 33333
DEFAULT_KEEPALIVE_TIME = 5  # Seconds
DEFAULT_KEEPALIVE_REFRESH_ATTEMPTS = 3  # TODO:: Implement or remove?

DEBUG = True  # Debug mode
DEBUG_SHOW_DATA = False  # Show sent data in debug mode

RESEND_ATTEMPTS = 3  # Tries
SENDER_SOCKET_TIMEOUT = 5  # Seconds
SENDER_BAD_PACKETS_SEQ = [3, 8, 6, 7]  # SEQ numbers
SENDER_BAD_PACKETS_ATTEMPTS = 3  # Tries

NACK_RESPONSE_MULTIPLIER = 5  # Packets

SEQ_SIZE = 3  # Bytes
CRC_SIZE = 4  # Bytes
FLAGS_SIZE = 2  # Bytes

MTU = 1500  # MTU is 1500 by default
ETHERNET_HEADER_LENGTH = 14
MIN_IP_HEADER_LENGTH = 20
MAX_IP_HEADER_LENGTH = 60
UDP_HEADER_LENGTH = 8
IP_HEADER_LENGTH = MIN_IP_HEADER_LENGTH  # We'll count with minimum IP header length
OFFSET = 9

###############################################
# Calculated constants
###############################################

MAX_SEGMENT_SIZE = MTU - ETHERNET_HEADER_LENGTH - IP_HEADER_LENGTH - UDP_HEADER_LENGTH - OFFSET  # Bytes
MAX_PAYLOAD_SIZE = MAX_SEGMENT_SIZE - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE  # Bytes

RECEIVER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME + 1  # Seconds (Integer)
SENDER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME  # Seconds (Integer)
