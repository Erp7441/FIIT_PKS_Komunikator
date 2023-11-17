from modes.Receiver import Receiver
from modes.Sender import Sender

# LAB IPs
# 192.168.48.128 - Server
# 192.168.48.129 - Client

# TODO:: Should I encode bytes to hex? Would it be better to do some other kind of encoding?


if __name__ == "__main__":
    mode = input("Mode? [r/s/t]: ")
    if mode == "r":
        Receiver()
    elif mode == "s":
        Sender("192.168.48.128")
    elif mode == "t":
        from utils.Tests import Tests
        #Tests.connection_tests_establishment_data()
        Tests.data_resassembly_test()
        # Tests.test_string_conversion()
