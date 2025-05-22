from enum import Enum
import math
from itertools import count
import random


class Status(Enum):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3


class FermatWorker:

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
                print("Fermat worker found prime number: " + str(num))
            else:
                is_probably_prime = True
                for _ in range(10):  # 10 iterations for better confidence
                    a = random.randint(2, num - 2)
                    if self.power(a, num - 1, num) != 1:
                        is_probably_prime = False
                        break
                if is_probably_prime:
                    print("Fermat worker found prime number: " + str(num))    
        