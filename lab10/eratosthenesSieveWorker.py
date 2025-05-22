from enum import Enum
import math
from itertools import count
import random
import time

from status import Status


class EratosthenesSieveWorker:

    def __init__(self, status=Status.FOLLOWER, epoch=0, current_biggest=1, filePath = 'primes.txt'):
        self.status = status
        self.epoch = epoch
        self.current_biggest = current_biggest
        self.filePath = filePath


    def demandElection():
        return 0
    
    def vote():
        return 0
    
    def propose(self, num):
        if self.status == Status.LEADER:
            self.writeNum(num)
            self.current_biggest = num
            # TODO UPDATE ALL CURRENT BIGGEST
        else:
            raise Exception("Not implemented")
            # TODO TO LEADER
            # TODO UPDATE ALL CURRENT BIGGEST
        return 1
    
    def updateCurrentBiggest(self, new_biggest):
        self.current_biggest = new_biggest

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
                if num > self.current_biggest:
                    print("Eratosthenes-sieve worker found prime number: " + str(num))
                    self.propose(num)
            
        