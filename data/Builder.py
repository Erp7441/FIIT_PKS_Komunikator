from json import dumps, loads

from data.Data import Data
from data.File import File
from packet.Flags import Flags
from packet.Segment import Segment
from utils.Constants import MAX_FILE_SIZE, MAX_SEGMENT_SIZE, FLAGS_SIZE, CRC_SIZE, SEQ_SIZE
from utils.Utils import print_color


def disassemble(data: Data, segment_size: int = MAX_SEGMENT_SIZE) -> list[Segment]:
    is_file = isinstance(data, File)
    payload_size = segment_size - SEQ_SIZE - CRC_SIZE - FLAGS_SIZE

    if len(data.value) > MAX_FILE_SIZE:
        print_color("Data is too large! Max size is " + str(MAX_FILE_SIZE / 1024**2) + " MB", color="red")
        return []

    # Encode the data
    encoded_data = data.encode()

    # Split encoded data into groups of size
    split = [encoded_data[i:i + payload_size] for i in range(0, len(encoded_data), payload_size)]

    packets = []
    for seq, bytes_data in enumerate(split):
        # Create packets and append them to the list
        flags = Flags(file=is_file, msg=(not is_file))
        packet = Segment(flags=flags, seq=seq + 1, data=bytes_data)
        packets.append(packet)

    info_dict = {
        "type": 'File' if is_file else 'Data',
        "name": data.name if is_file else None,
        "number_of_packets": len(packets),
        "total_encoded_size": len(encoded_data),
        "total_size": len(data.value) if data.value is not None else 0,
        "fragment_size": segment_size
    }

    encoded_dict = dumps(info_dict)

    info_packet = Segment(Flags(info=True), data=encoded_dict)
    packets.insert(0, info_packet)

    return packets


def assemble(packets: list[Segment]):
    seen_seq = set()
    filtered_packets = []
    for packet in packets:
        if packet.seq not in seen_seq:
            filtered_packets.append(packet)
            seen_seq.add(packet.seq)
    packets = filtered_packets

    # Get info about the data we'll be dealing with
    info_packet = packets.pop(0)

    info = loads(info_packet.data)

    is_file = info.get('type') == 'File'
    name = info.get('name')

    # Join together the packet data values
    data = b"".join([packet.data for packet in packets])

    print_color("Reassembled {0} fragments of size {1}".format(len(packets), info.get('fragment_size')), color="green")
    # Decode the data
    if is_file:
        return File(name=name).decode(data)
    else:
        return Data().decode(data)
