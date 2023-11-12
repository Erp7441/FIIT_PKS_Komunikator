from enum import Enum


class ConnectionState(Enum):
    SYN_SENT = 0
    SYN_RECEIVED = 1
    SYN_ACK_SENT = 2
    ACTIVE = 3
    FIN_RECEIVED = 4
    FIN_ACK_SENT = 5
    FIN_SENT = 6
    CLOSED = 7

