from enum import Enum


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

    def findPrime(self, method):

        if method == Method.CHECK_DIVIDER:
            #TODO check divider primality test method
            return 1
        elif method == Method.MILLER_RABIN:
            #TODO miller-rabin primality test method
            return 2
        elif method == Method.FERMAT:
            #TODO fermat primality test method
            return 3
        elif method == Method.ERATOSTHENES_SIEVE:
            #TODO eratosthenes primality test method
            return 4
        else:
            raise Exception("Unavailable/non-existent method for checking primality")