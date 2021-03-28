import time
from multiprocessing import Process, Queue
from enum import Enum

class Message(Enum):
    ACK = 0
    NAK = 1

class Package:
    def __init__(self, sequence, message, is_corrupted):
        self.sequence = sequence
        self.message = message
        self.is_corrupted = is_corrupted

class Protocol:
    def __init__(self):
        self.sender_queue = Queue()
        self.receiver_queue = Queue()

    def receive(self, num_packages):
        print("Receive Base")

    def send(self, winSize, packSize, pLoss):
        print("Send Base")
