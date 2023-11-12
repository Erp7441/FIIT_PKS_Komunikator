ENCODING = 'utf-8'
DEFAULT_PORT = 33333

NAME_HEX_HEADER = "__NAME__"


SEQ_SIZE = 3  # Bytes
CRC_SIZE = 8  # Bytes
FLAGS_SIZE = 2  # Bytes

# MTU is 1500
MTU = 1500


###############################################
# Calculated constants
###############################################

MAX_PAYLOAD_SIZE = MTU - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE - len(NAME_HEX_HEADER)  # Bytes

# Sizes for ranges in bytes array
SEQ_B_SIZE = SEQ_SIZE * 2
CRC_B_SIZE = CRC_SIZE * 2
FLAGS_B_SIZE = FLAGS_SIZE * 2
