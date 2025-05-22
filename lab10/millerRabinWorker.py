from enum import Enum
import math
from itertools import count
import random

from status import Status


class MillerRabinWorker:

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

    def sendCommand(self):
        if(self.status == Status.LEADER):
            return 1
        return 0
    
    def updateCurrentBiggest(self, new_biggest):
        self.current_biggest = new_biggest
    

    def changeStatus(self, new):
        self.status = new

    def millerTest(self, num, d, r):

        a = random.randrange(2, num - 2)
        x = pow(a, d, num)

        if x == 1 or x == num - 1:
            return True

        for _ in range(r - 1):
            x = pow(x, 2, num)
            if x == num - 1:
                return True
            if x == 1:
                return False

        return False


    def findPrime(self, stop):

        for num in range(2, stop):

            if num in (2, 3):
                if num > self.current_biggest:
                    print("Miller-Rabin worker found prime number: " + str(num))
                    self.propose(num)
                continue
            if num <= 1 or num % 2 == 0:
                continue

            # Write num-1 as d * 2^r
            d = num - 1
            r = 0
            while d % 2 == 0:
                d //= 2
                r += 1

            is_probably_prime = True
            for _ in range(10):  # 10 rounds of testing
                if not self.millerTest(num, d, r):
                    is_probably_prime = False
                    break

            if is_probably_prime:
                if num > self.current_biggest:
                    print("Miller-Rabin worker found prime number: " + str(num))
                    self.propose(num)
        