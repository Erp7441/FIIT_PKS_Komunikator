from data.Data import Data
from data.File import File
from packet.Flags import Flags
from packet.Packet import Packet
from utils.Constants import MAX_PACKET_SIZE


class Tests:

    @staticmethod
    def encoding_tests():
        flags = Flags(syn=True, ack=True, fin=True, info=True)
        encoded_flags = flags.encode_flags()
        print("{0:b}".format(encoded_flags))
        flags.decode_flags(3)
        pass

        file = File(select=True)
        encoded_file = file.encode()
        file2 = File()
        decoded_file = file2.decode(encoded_file)
        file2.save("C:/Users/Martin/Desktop")
        pass

        message = Data("Test sprava")
        encoded_message = message.encode()
        received_message = Data()
        decoded_message = received_message.decode(encoded_message)
        pass

    @staticmethod
    def packet_tests():
        packet = Packet(Flags(file=True), data=File())
        encoded_packet = packet.encode()
        packet2 = Packet()

        decoded_packet = packet2.decode(encoded_packet)
        pass

    @staticmethod
    def packet_length_tests():
        packet = Packet(Flags(file=True), data=File())
        encoded_packet = packet.encode()

        while len(encoded_packet) != MAX_PACKET_SIZE:
            encoded_packet += '0'

        packet2 = Packet().decode(encoded_packet)

        from modes.Sender import Sender

        sender = Sender("192.168.48.128")
        sender._send_packet_(packet2)

    @staticmethod
    def connection_tests_client():
        from modes.Sender import Sender
        from packet.Packet import Packet
        from data.File import File
        from packet.Flags import Flags

        sender = Sender("192.168.48.128")
        packet = Packet(Flags(file=True), data=File(select=True))
        sender._send_packet_(packet)

    @staticmethod
    def connection_tests_establishment():
        from modes.Sender import Sender

        sender = Sender("192.168.48.128")
        # sender.close_connection()

    @staticmethod
    def connection_tests_establishment_data():
        from modes.Sender import Sender

        sender = Sender("192.168.48.128")
        while True:
            packet = Packet(Flags(file=True), data=File(select=True))
            sender._send_packet_(packet)
        # sender.close_connection()


    @staticmethod
    def data_resassembly_test():
        # from data.Builder import disassemble, assemble
        # data = File(select=True)
        # packets = disassemble(data)
        # data2 = assemble(packets)
        # print(data.value == data2.value)
        # pass
        #
        # data = Data("Hello There!")
        # packets = disassemble(data)
        # data2 = assemble(packets)
        # print(data.value == data2.value)
        # pass

        from modes.Sender import Sender
        data = File(select=True)
        sender = Sender("192.168.48.128")
        sender.send(data)

    @staticmethod
    def connection_tests_server():
        from modes.Receiver import Receiver
        receiver = Receiver()

    @classmethod
    def test_string_conversion(cls):
        # from modes.Sender import Sender
        from modes.Receiver import Receiver
        # sender = Sender("192.168.48.128")
        receiver = Receiver()
        pass
