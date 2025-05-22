from enum import Enum
import math
from itertools import count
import random


class Status(Enum):
    FOLLOWER = 1
    LEADER = 2
    CANDIDATE = 3

class Method(Enum):
    CHECK_DIVIDER = 1
    MILLER_RABIN= 2
    FERMAT = 3 
    ERATOSTHENES_SIEVE = 4


class Worker:

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

    def findPrime(self, num, method):

        if method == Method.CHECK_DIVIDER:

            for div in range(2, math.floor(math.sqrt(num)) + 1):
                if  num % div == 0:
                    return False
            print("Check divider worker found prime number: " + str(num))
            return True
        
        elif method == Method.MILLER_RABIN:

            if num in (2, 3):
                print("Miller-Rabin worker found prime number: " + str(num))
                return True
            if num <= 1 or num % 2 == 0:
                return False

            d = num - 1
            r = 0
            while d % 2 == 0:
                d //= 2
                r += 1

            for _ in range(10):
                if not self.millerTest(num, d, r):
                    return False
            print("Miller-Rabin worker found prime number: " + str(num))
            return True
        
        elif method == Method.FERMAT:
            if num == 4:
                return False
            elif num == 2 or num == 3:
                print("Fermat worker found prime number: " + str(num))
                return True
            
            else:
                for i in range(10):
                    
                    a = random.randint(2, num - 2)
                    if self.power(a, num - 1, num) != 1:
                        return False
            print("Fermat worker found prime number: " + str(num))            
            return True

        elif method == Method.ERATOSTHENES_SIEVE:

            if num < 2:
                return False

            prime = [True for _ in range(num + 1)]
            prime[0] = prime[1] = False

            p = 2
            while p * p <= num:
                if prime[p]:
                    for i in range(p * p, num + 1, p):
                        prime[i] = False
                p += 1
            if (prime[num] == True):
                print("Eratosthenes-sieve worker found prime number: " + str(num))
            return prime[num]
            
        else:
            raise Exception("Unavailable/non-existent method for checking primality")