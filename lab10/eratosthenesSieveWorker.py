from enum import Enum
import math
from itertools import count
import random


class Status(Enum):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3


class EratosthenesSieveWorker:

    def __init__(self, status=Status.FOLLOWER, epoch=0):
        self.status = status
        self.epoch = epoch


    def demandElection():
        return 0
    
    def vote():
        return 0

    def request():
        return 0

    def sendCommand(self):
        if(self.status == Status.LEADER):
            return 1
        return 0
    

    def changeStatus(self, new):
        self.status = new


    def findPrime(self, stop):

        if stop < 2:
            return

        prime = [True] * stop
        prime[0] = prime[1] = False

        for p in range(2, int(math.sqrt(stop)) + 1):
            if prime[p]:
                for i in range(p * p, stop, p):
                    prime[i] = False

        for num in range(2, stop):
            if prime[num]:
                print("Eratosthenes-sieve worker found prime number: " + str(num))
            
        