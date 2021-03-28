from protocol import Protocol, Message, Package
from utils import rand_is_corrupted

class GoBackNProtocol(Protocol):
    def __init__(self):
        super().__init__()

    def receive(self, packSize):
        self.total_received = 0
        self.total_sent_ack = 0
        while True:
            if self.receiver_queue.empty():
                continue
            frame = self.receiver_queue.get()
            if frame.sequence != self.total_received:
                continue
            if not frame.is_corrupted:
                self.total_received += 1

                self.sender_queue.put(Package(frame.sequence, Message.ACK, False))
                self.total_sent_ack += 1
                if self.total_sent_ack == packSize:
                    return
            else:
                self.sender_queue.put(Package(frame.sequence, Message.NAK, False))

    def send(self, winSize, packSize, p):
        self.total_sent = 0
        self.total_received_ack = 0
        window = []
        while True:
            if len(window) < winSize and self.total_sent < packSize:
                package = Package(self.total_sent, None, rand_is_corrupted(p))
                self.receiver_queue.put(package)
                window.append(package)
                self.total_sent += 1

            if not self.sender_queue.empty():
                ack = self.sender_queue.get()
                if ack.message == Message.ACK:
                    self.total_received_ack += 1
                    del window[0]
                    if self.total_received_ack == packSize:
                        return
                elif ack.message == Message.NAK:
                    for entry in window:
                        entry.is_corrupted = rand_is_corrupted(p)
                        self.receiver_queue.put(entry)