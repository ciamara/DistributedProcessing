from enum import Enum
import math
from itertools import count
import random

from status import Status


class FermatWorker:

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

    def power(self, a, n, p):

        res = 1 
        
        a = a % p  
        
        while n > 0:
            
            if n % 2:
                res = (res * a) % p
                n = n - 1
            else:
                a = (a ** 2) % p
                n = n // 2
                
        return res % p

    def findPrime(self, stop):

        for num in range(2, stop):
            if num == 4:
                continue
            elif num == 2 or num == 3:
                if num > self.current_biggest:
                    print("Fermat worker found prime number: " + str(num))
                    self.propose(num)
            else:
                is_probably_prime = True
                for _ in range(10):  # 10 iterations for better confidence
                    a = random.randint(2, num - 2)
                    if self.power(a, num - 1, num) != 1:
                        is_probably_prime = False
                        break
                if is_probably_prime:
                    if num > self.current_biggest:
                        print("Fermat worker found prime number: " + str(num))  
                        self.propose(num)  
        