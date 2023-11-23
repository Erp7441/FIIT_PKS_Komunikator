from connection.Connection import Connection
from connection.ConnectionManager import ConnectionManager
from connection.ConnectionState import ConnectionState
from utils.Constants import RESEND_ATTEMPTS, WINDOW_SIZE
from utils.Utils import print_color, print_debug, print_debug_data


class SenderConnectionManager(ConnectionManager):
    def __init__(self, sender):
        super().__init__(sender)

    ###############################################
    # SECTION: Establishing connection (Sender)
    ###############################################
    def establish_connection(self, ip: str, port: int):
        connection = Connection(ip, port, None, parent=self, batch_size=WINDOW_SIZE)
        self.send_syn_packet(connection)

        if self.await_syn_ack(connection):
            self.active_connections.append(connection)
            print_color("Connection with", connection.ip+":"+str(connection.port), "established", color='green')
        return connection

    ###############################################
    # SECTION: Closing connection (Sender)
    ###############################################
    def close_connection(self, ip: str, port: int):
        with self.lock:
            connection = self.get_connection(ip, port)
            if connection is None:
                print_debug("Connection with {0}:{1} does not exist!".format(ip, port))
                return
            elif connection.state is ConnectionState.CLOSED or connection.state is ConnectionState.RESET:
                print_debug("Connection with {0}:{1} is already closed!".format(ip, port))
                return

            self.send_fin_packet(connection)

            if self.await_fin_ack(connection):
                self.remove_connection(connection)
                print_color("Connection with", connection.ip+":"+str(connection.port), "closed", color='green')

    ###############################################
    # SECTION: Keep alive sequence (Sender)
    ###############################################
    def refresh_keepalive(self, connection: Connection):
        with self.lock:
            if connection.state == ConnectionState.CLOSED or connection.state == ConnectionState.RESET:
                print_debug("Failed to refresh keepalive state! Connection is already closed", color="red")
                return False

            self.send_syn_packet(connection)
            if self.await_syn_ack(connection):
                connection.current_keepalive_time = connection.keepalive_time
                self.send_ack_packet(connection)
                connection.state = ConnectionState.ACTIVE
                print_debug("Refreshed keepalive state!")
                return True
            print_debug("Failed to refresh keepalive state!", color='orange')
            return False

    ###############################################
    # SECTION: Batch sending data packets (Client)
    ###############################################
    # Send a single packet (with check)
    def send_data_packet(self, packet, connection: Connection):
        if connection is None or connection.state != ConnectionState.ACTIVE:
            return False

        packet.send_to(connection.ip, connection.port, self.parent.socket, with_error=self.parent.generate_bad_packet)

        print_debug_data("Sent packet to {0}:{1} server with data: {2}".format(connection.ip, connection.port, packet.data))
        return True

    def _await_ack_for_data(self, data_packet, connection: Connection):
        # TODO:: Implement receiving of multiple ACKs here (client)
        # TODO:: How to handle faulty ACK?
        ip, port, packet = self.await_packet(connection)

        # If we got an ACK from wrong connection. Kill it the connection.
        if ip != connection.ip or port != connection.port or packet is None:
            # BIG TODO:: packet is None currently

            # TODO:: Add ACK and NACK flag check?
            self.kill_connection(connection)
            return None

        if packet.flags.nack:
            # TODO:: Handle incorrect NACK seq? Probably not needed.
            print_debug("Received NACK packet from {0}:{1}".format(connection.ip, connection.port))
            connection.add_bad_packet(data_packet)
        elif packet.flags.ack:
            print_debug("ACK with SEQ value {0} received".format(packet.seq))

            # Compare SEQ number of ACK packet with SEQ number of sent packet
            if packet is None or packet.seq != data_packet.seq:
                print_debug("Broken or incorrect ACK packet received!", color="orange")

        return packet

    def batch_send(self, packets: list, connection: Connection):
        packet_count = len(packets)  # Number of packets
        packet_index = 0  # Index of current packet

        # Sending multiple packets in a batch
        for _ in range(0, len(packets), connection.batch_size):
            sent_packets_this_batch = 0

            # For each packet in the batch
            for _ in range(connection.batch_size):
                # If we reached the end of the list, break (case where there are fewer packets than the batch size)
                if packet_index >= packet_count:
                    break

                # Send single packet from batch
                if not self.send_data_packet(packets[packet_index], connection):
                    return  # Connection is dead
                print_debug("Sending packet {0}/{1}".format(packet_index+1, packet_count))
                packet_index += 1
                sent_packets_this_batch += 1

            # For each packet sent this batch
            for j in range(sent_packets_this_batch):
                # Get the packet from the batch
                data_packet = packets[packet_index - sent_packets_this_batch + j]
                self._await_ack_for_data(data_packet, connection)  # Await ACK

        self._resend_bad_packets(connection)

    # Resending failed packets
    def _resend_bad_packets(self, connection: Connection):
        if self.parent.generate_bad_packet is True:
            self.parent.generate_bad_packet = False  # TODO:: Move to settings

        count = 0  # Attempt counter
        # While list of bad packets is not empty
        while len(connection.bad_packets) != 0:
            print_debug("Resending {0} bad packets".format(len(connection.bad_packets)))
            if count >= RESEND_ATTEMPTS:
                break  # Too many attempts
            bad_packets = connection.bad_packets  # Get list of bad packets
            connection.bad_packets = []  # Clear the original list, so you have space to re-add new bad packets
            self.batch_send(bad_packets, connection)    # Resend bad packets
            count += 1  # Increment attempt counter

    def __str__(self):
        return "Sender " + super().__str__()

