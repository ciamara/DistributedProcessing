from enum import Enum
import math
from itertools import count
import random


class Status(Enum):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3


class CheckDividerWorker:

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

        for num in range(2, stop):
            for div in range(2, math.floor(math.sqrt(num)) + 1):
                if num % div == 0:
                    break
            else:
                print("Check divider worker found prime number: " + str(num))
            
        