ENCODING = 'utf-8'
DEFAULT_PORT = 33333
DEFAULT_KEEPALIVE_TIME = 5  # Seconds
DEFAULT_KEEPALIVE_REFRESH_ATTEMPTS = 3
DEBUG = True  # Debug mode


SEQ_SIZE = 3  # Bytes
CRC_SIZE = 4  # Bytes
FLAGS_SIZE = 2  # Bytes

MTU = 1500  # MTU is 1500 by default
ETHERNET_HEADER_LENGTH = 14
MIN_IP_HEADER_LENGTH = 20
MAX_IP_HEADER_LENGTH = 60
UDP_HEADER_LENGTH = 8
IP_HEADER_LENGTH = MIN_IP_HEADER_LENGTH  # We'll count with minimum IP header length

# TODO:: Find out why this changed from 6 to 5 (Due to the INFO packet?)
UNUSED_BYTES = 5  # FLAGS is only 2 bytes which leaves 2 bytes free, SEQ is only 3 bytes which leaves 1 byte free.

###############################################
# Calculated constants
###############################################

MAX_PACKET_SIZE = MTU - ETHERNET_HEADER_LENGTH - IP_HEADER_LENGTH - UDP_HEADER_LENGTH + UNUSED_BYTES  # Bytes
MAX_PAYLOAD_SIZE = MAX_PACKET_SIZE - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE  # Bytes

# Sizes for ranges in bytes array
SEQ_B_SIZE = SEQ_SIZE * 2
CRC_B_SIZE = CRC_SIZE * 2
FLAGS_B_SIZE = FLAGS_SIZE * 2

RECEIVER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME + 1  # Seconds (Integer)
SENDER_KEEPALIVE_TIME = DEFAULT_KEEPALIVE_TIME  # Seconds (Integer)
