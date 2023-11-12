def encoding_tests():
    # from packet.Flags import Flags
    #
    # test = Flags(syn=True, ack=True, fin=True, info=True)
    # encoded_flags = test.encode_flags()
    # print("{0:b}".format(encoded_flags))
    # test.decode_flags(3)
    # pass

    # from data.File import File
    # file = File()
    # encoded_file = file.encode()
    # file2 = File(select=False)
    # decoded_file = file2.decode(encoded_file)
    # file2.save("C:/Users/Martin/Desktop")

    # from data.Message import Message
    # message = Message("Test sprava")
    # encoded_message = message.encode()
    # decoded_message = message.decode(encoded_message)
    pass


def packet_tests():
    from packet.Packet import Packet
    from packet.Flags import Flags
    from data.File import File

    packet = Packet(Flags())
    packet2 = Packet(Flags(file=True), data=File())
    pass