from modes.Receiver import Receiver
from modes.Sender import Sender

if __name__ == "__main__":
    mode = input("Mode? [r/s]: ")
    if mode == "r":
        Receiver()
    elif mode == "s":
        Sender("192.168.48.128")
