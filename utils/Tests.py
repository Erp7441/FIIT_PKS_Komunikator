def encoding_tests():
    from packet.Flags import Flags

    flags = Flags(syn=True, ack=True, fin=True, info=True)
    encoded_flags = flags.encode_flags()
    print("{0:b}".format(encoded_flags))
    flags.decode_flags(3)
    pass

    from data.File import File
    file = File(select=True)
    encoded_file = file.encode()
    file2 = File()
    decoded_file = file2.decode(encoded_file)
    file2.save("C:/Users/Martin/Desktop")
    pass

    from data.Message import Message
    message = Message("Test sprava")
    encoded_message = message.encode()
    received_message = Message()
    decoded_message = received_message.decode(encoded_message)
    pass


def packet_tests():
    from packet.Packet import Packet
    from packet.Flags import Flags
    from data.File import File

    packet = Packet(Flags(file=True), data=File())
    encoded_packet = packet.encode()
    packet2 = Packet()

    decoded_packet = packet2.decode(encoded_packet)
    pass


def packet_length_tests():
    from packet.Packet import Packet
    from packet.Flags import Flags
    from data.File import File
    from utils.Constants import MAX_PACKET_SIZE

    packet = Packet(Flags(file=True), data=File())
    encoded_packet = packet.encode()

    while len(encoded_packet) != MAX_PACKET_SIZE:
        encoded_packet += '0'

    packet2 = Packet().decode(encoded_packet)

    from modes.Sender import Sender

    sender = Sender("192.168.48.128")
    sender.send_packet(packet2)


def connection_tests_client():
    from modes.Sender import Sender
    from packet.Packet import Packet
    from data.File import File
    from packet.Flags import Flags

    sender = Sender("192.168.48.128")
    packet = Packet(Flags(file=True), data=File())
    sender.send_packet(packet)


def connection_tests_establishment():
    from modes.Sender import Sender

    sender = Sender("192.168.48.128")
    sender.close_connection()


def connection_tests_server():
    from modes.Receiver import Receiver
    receiver = Receiver()