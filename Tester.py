import time
from multiprocessing import Process, Queue
from enum import Enum

class Tester:
    def __init__(self, protocol):
        self.protocol = protocol
        print("Init Base")

    def singleTest(self, winSize, packSize, pLoss):
        sender_proc = Process(target=self.protocol.send, args=(winSize, packSize, pLoss))
        receiver_proc = Process(target=self.protocol.receive, args=(packSize,))

        startTime = time.time()
        sender_proc.start()
        receiver_proc.start()
        receiver_proc.join()
        sender_proc.join()
        endTime = time.time()

        print("time.................... %f" % (endTime - startTime) )

        return endTime - startTime

    def testRun(self, winSize, packSize, pLoss, nTests):
        times = []
        for n in range(nTests):
            times.append(self.singleTest(winSize, packSize, pLoss))

        print("avg time................ %f" % (sum(times) / len(times)))
        return sum(times) / len(times)