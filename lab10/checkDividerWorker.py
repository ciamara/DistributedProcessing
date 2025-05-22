from enum import Enum
import math
from itertools import count
import random

from status import Status


class CheckDividerWorker:

    def __init__(self, status=Status.FOLLOWER, epoch=0, current_biggest=1, filePath = 'primes.txt'):
        self.status = status
        self.epoch = epoch
        self.current_biggest = current_biggest
        self.filePath = filePath


    def demandElection():
        return 0
    
    def vote():
        return 0
    
    def writeNum(self, num):
        with open("primes.txt", "a") as f:
            f.write(str(num) + "\n")
        return
    
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
  
    def changeStatus(self, new):
        self.status = new

    def findPrime(self, stop):

        for num in range(2, stop):
            for div in range(2, math.floor(math.sqrt(num)) + 1):
                if num % div == 0:
                    break
            else:
                if num > self.current_biggest:
                    print("Check divider worker found prime number: " + str(num))
                    self.propose(num)
            
        