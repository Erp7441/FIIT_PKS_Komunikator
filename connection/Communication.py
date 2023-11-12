class Communication:
    def __init__(self):
        pass

    # Pseudo idea
    # Gets splited data in packets
    # Evaluate packets order and crc32
    # Two things will be required in here
    # Get next packet - gets next packet in communication for sending
    # Get last packet - gets last packet in communication for resending in case of error
