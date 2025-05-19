from worker import Worker
from worker import Status
from worker import Method


def main():

    checkDividerWorker = Worker()
    millerRabinWorker = Worker()
    fermatWorker = Worker()
    eratosthenesSieveWorker = Worker()

    for num in range(2, 200):
        if eratosthenesSieveWorker.findPrime(num, Method.ERATOSTHENES_SIEVE):
            print("Number " + str(num) + " is prime")
        else:
            print("Number " + str(num) + " is not prime")
        

    return 0









if __name__=="__main__":
    main()