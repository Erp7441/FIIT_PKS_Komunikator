from enum import Enum


class ConnectionState(Enum):
    SYN_RECEIVED = 0
    SYN_ACK_SENT = 1
    ACTIVE = 2
    FIN_RECEIVED = 3
    FIN_ACK_SENT = 4
    CLOSED = 5

