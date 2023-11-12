def main():
    from packet.Flags import Flags

    test = Flags(syn=True, ack=True, fin=True, info=True)
    encoded_flags = test.encode_flags()
    print("{0:b}".format(encoded_flags))


if __name__ == "__main__":
    main()