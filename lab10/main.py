from checkDividerWorker import CheckDividerWorker
from eratosthenesSieveWorker import EratosthenesSieveWorker
from fermatWorker import FermatWorker
from millerRabinWorker import MillerRabinWorker

from status import Status

from multiprocessing import Process


def main():

    open('primes.txt', 'w').close()

    cdWorker = CheckDividerWorker()
    mrWorker = MillerRabinWorker()
    fWorker = FermatWorker()
    esWorker = EratosthenesSieveWorker()

    cdWorker.changeStatus(Status.LEADER)
        
    cdProc = Process(target=cdWorker.findPrime, args=(1000,))
    mrProc = Process(target=mrWorker.findPrime, args=(1000,))
    fProc = Process(target=fWorker.findPrime, args=(1000,))
    esProc = Process(target=esWorker.findPrime, args=(1000,))

    cdProc.start()
    mrProc.start()
    fProc.start()
    esProc.start()

    cdProc.join()
    mrProc.join()
    fProc.join()
    esProc.join()

    return 0









if __name__=="__main__":
    main()