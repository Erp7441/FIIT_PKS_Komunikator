from json import dumps, loads

from data.Data import Data
from data.File import File
from packet.Flags import Flags
from packet.Packet import Packet
from utils.Constants import MAX_FILE_SIZE, MAX_PAYLOAD_SIZE
from utils.Utils import encode_str_to_hex, decode_str_from_hex

# TODO:: Add max size of 2MB limit before disassembly


def disassemble(data: Data):
    is_file = isinstance(data, File)
    size = MAX_FILE_SIZE if isinstance(data, File) else MAX_PAYLOAD_SIZE

    # Encode the data
    encoded_data = data.encode()

    # Split encoded data into groups of size
    split = [encoded_data[i:i + size] for i in range(0, len(encoded_data), size)]

    packets = []
    for seq, bytes_data in enumerate(split):
        # Create packets and append them to the list
        flags = Flags(file=is_file, msg=(not is_file))
        packet = Packet(flags=flags, seq=seq+1, data=bytes_data)
        packets.append(packet)

    # TODO:: Add name to this info and remove it from where its not needed.
    info_dict = {
        "type": 'File' if is_file else 'Data',
        "number_of_packets": len(packets),
        "total_size": len(encoded_data)  # TODO:: Fix value
    }
    encoded_dict = encode_str_to_hex(dumps(info_dict))

    info_packet = Packet(Flags(info=True), data=encoded_dict)
    packets.insert(0, info_packet)

    # TODO:: Append info packet at the begining
    # TODO:: Append fin packet at the end (or find better way by "closing" communicaiton after send is done)

    return packets


def assemble(packets: list[Packet]):
    # Get info about the data we'll be dealing with
    info_packet = packets.pop(0)
    info = loads(decode_str_from_hex(info_packet.data))
    is_file = info.get('type') == 'File'


    # Join together the packet data values
    data = ''.join([packet.data for packet in packets])

    # Decode the data
    if is_file:
        return File().decode(data)
    else:
        return Data().decode(data)
