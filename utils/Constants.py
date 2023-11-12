ENCODING = 'utf-8'
DEFAULT_PORT = 33333

NAME_HEX_HEADER = "__NAME__"


SEQ_SIZE = 3  # Bytes
CRC_SIZE = 4  # Bytes
FLAGS_SIZE = 2  # Bytes

MTU = 1500  # MTU is 1500 by default
ETHERNET_HEADER_LENGTH = 14
MIN_IP_HEADER_LENGTH = 20
MAX_IP_HEADER_LENGTH = 60
UDP_HEADER_LENGTH = 8
UNUSED_BYTES = 6  # FLAGS is only 2 bytes which leaves 2 bytes free, SEQ is only 3 bytes which leaves 1 byte free.
IP_HEADER_LENGTH = MIN_IP_HEADER_LENGTH  # We'll count with minimum IP header length

###############################################
# Calculated constants
###############################################

MAX_PACKET_SIZE = MTU - ETHERNET_HEADER_LENGTH - IP_HEADER_LENGTH + UNUSED_BYTES  # Bytes
MAX_PAYLOAD_SIZE = MAX_PACKET_SIZE - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE  # Bytes
MAX_FILE_SIZE = MAX_PAYLOAD_SIZE - len(NAME_HEX_HEADER)

# Sizes for ranges in bytes array
SEQ_B_SIZE = SEQ_SIZE * 2
CRC_B_SIZE = CRC_SIZE * 2
FLAGS_B_SIZE = FLAGS_SIZE * 2
