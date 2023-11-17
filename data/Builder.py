from json import dumps, loads

from data.Data import Data
from data.File import File
from packet.Flags import Flags
from packet.Packet import Packet
from utils.Constants import MAX_PAYLOAD_SIZE


# TODO:: Add max size of 2MB limit before disassembly


def disassemble(data: Data):
    is_file = isinstance(data, File)

    # Encode the data
    encoded_data = data.encode()

    # Split encoded data into groups of size
    split = [encoded_data[i:i + MAX_PAYLOAD_SIZE] for i in range(0, len(encoded_data), MAX_PAYLOAD_SIZE)]

    packets = []
    for seq, bytes_data in enumerate(split):
        # Create packets and append them to the list
        flags = Flags(file=is_file, msg=(not is_file))
        packet = Packet(flags=flags, seq=seq+1, data=bytes_data)
        packets.append(packet)

    # TODO:: Split this packet in case the name is too long
    # TODO:: Add name to this info and remove it from where its not needed.
    info_dict = {
        "type": 'File' if is_file else 'Data',
        "name": data.name if is_file else None,
        "number_of_packets": len(packets),
        "total_size": len(encoded_data)  # TODO:: Fix value
    }

    # TODO:: Add encoding of info packet?
    encoded_dict = dumps(info_dict)

    info_packet = Packet(Flags(info=True), data=encoded_dict)
    packets.insert(0, info_packet)

    # TODO:: Append info packet at the begining
    # TODO:: Append fin packet at the end (or find better way by "closing" communicaiton after send is done)

    return packets


def assemble(packets: list[Packet]):
    # Get info about the data we'll be dealing with
    info_packet = packets.pop(0)

    # TODO:: Add decoding of info packet?
    info = loads(info_packet.data)
    
    is_file = info.get('type') == 'File'
    name = info.get('name')


    # Join together the packet data values
    data = ''.join([packet.data for packet in packets])

    # Decode the data
    if is_file:
        return File(name=name).decode(data)
    else:
        return Data().decode(data)
