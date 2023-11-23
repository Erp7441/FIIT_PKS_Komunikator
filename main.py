from modes.Receiver import Receiver
from modes.Sender import Sender

# LAB IPs
# 192.168.48.128 - Server
# 192.168.48.129 - Client

# TODO:: Fix bug there one good and one bad receives 2 acks (Two points of failure, Client is batch awaiting only acks, or server is sending only acks)
# TODO:: Check if connection reset from server side works. (Case where client connection dies suddenly)

if __name__ == "__main__":
    mode = input("Mode? [r/s/t]: ")
    if mode == "r":
        Receiver()
    elif mode == "s":
        Sender("192.168.48.129")
    elif mode == "t":
        from utils.Tests import Tests
        #Tests.connection_tests_establishment_data()
        Tests.data_resassembly_test()
        #Tests.packet_tests()
        #Tests.test_string_conversion()
