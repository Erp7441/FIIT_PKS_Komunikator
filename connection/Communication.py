class Communication:
    def __init__(self, packets):
        self.packets = packets

    def receive(self, packet):
        # TODO:: Check if packet with seq number is not already present
        self.packets.append(packet)
        self.packets.sort(key=lambda seq: seq.seq)

    # Pseudo idea
    # Gets splited data in packets
    # Evaluate packets order and crc32
    # Two things will be required in here
    # Get next packet - gets next packet in communication for sending
    # Get last packet - gets last packet in communication for resending in case of error
