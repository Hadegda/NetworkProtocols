from protocol import Protocol, Message, Package
from utils import rand_is_corrupted

class SelectiveRepeatProtocol (Protocol):
    def __init__(self):
        super().__init__()

    def receive(self, packSize):
        total_received = 0
        total_sent_ack = 0
        buffer = []
        while True:
            if self.receiver_queue.empty():
                continue
            package = self.receiver_queue.get()
            if total_received == package.sequence:
                if package.is_corrupted:
                    self.sender_queue.put(Package(package.sequence, Message.NAK, False))
                    continue

                total_received += 1

                self.sender_queue.put(Package(package.sequence, Message.ACK, False))
                total_sent_ack += 1

                while len(buffer):
                    if buffer[0].is_corrupted:
                        self.sender_queue.put(Package(buffer[0].sequence, Message.NAK, False))
                        del buffer[0]
                        break
                    total_received += 1
                    self.sender_queue.put(Package(buffer[0].sequence, Message.ACK, False))
                    total_sent_ack += 1
                    del buffer[0]

                if total_sent_ack == packSize:
                    return
            else:
                buffer.append(package)

    def send(self, winSize, packSize, p):
        total_sent = 0
        total_received_ack = 0
        window = []
        while True:
            if len(window) < winSize and total_sent < packSize:
                package = Package(total_sent, None, rand_is_corrupted(p))
                self.receiver_queue.put(package)
                window.append(package)
                total_sent += 1

            if not self.sender_queue.empty():
                ack = self.sender_queue.get()
                if ack.message == Message.ACK:
                    total_received_ack += 1
                    del window[0]
                    if total_received_ack == packSize:
                        return
                elif ack.message == Message.NAK:
                    result = window[ack.sequence - total_received_ack]
                    result.is_corrupted = rand_is_corrupted(p)
                    self.receiver_queue.put(result)