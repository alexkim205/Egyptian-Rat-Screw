from multiprocessing import Process, Condition, Lock  
from multiprocessing.managers import BaseManager  
import time, os  

lock = Lock()  
waitC = Condition(lock)  
waitP = Condition(lock)  

class numeri(object):  
    def __init__(self):  
        self.nl = []  

    def getLen(self):  
        print("Address of list inside class: " + str(id(self))) 
        return len(self.nl)  
    
    def getData(self):  
        print("Address of list inside class: " + str(id(self))) 
        return self.nl

    def stampa(self):  
        print("Address of list inside class: " + str(id(self))) 
        print(self.nl)  

    def appendi(self, x):  
        print("Address of list inside class: " + str(id(self))) 
        self.nl.append(x)  

    def svuota(self):  
        print("Address of list inside class: " + str(id(self))) 
        for i in range(len(self.nl)):  
            del self.nl[0]  

class numManager(BaseManager):  
    pass  

numManager.register('numeri', numeri, exposed = ['getLen', 'appendi', 'svuota', 'stampa', 'getData'])  

def consume(waitC, waitP, listaNumeri):  
    lock.acquire()  
    print("Consume:")
    print("Address of list inside consume: " + str(id(listaNumeri))) 
    if (listaNumeri.getLen() == 0):  
        waitC.wait()  
    listaNumeri.stampa()  
    print(listaNumeri.getData())
    listaNumeri.svuota()  
    print(listaNumeri.getData())
    waitP.notify()  
    lock.release()  

def produce(waitC, waitP, listaNumeri):  
    lock.acquire()  
    print("Produce:")
    print(listaNumeri.getData())
    print("Address of list inside produce: " + str(id(listaNumeri))) 
    if (listaNumeri.getLen() > 0):  
        waitP.wait()  
    for i in range(10):  
        listaNumeri.appendi(i)  
    waitC.notify()  
    lock.release()  


def main():  
    mymanager = numManager()  
    mymanager.start()  
    listaNumeri = mymanager.numeri() 
    producer = Process(target = produce, args =(waitC, waitP, listaNumeri,))  
    producer.start()  
    time.sleep(2)  
    consumer = Process(target = consume, args =(waitC, waitP, listaNumeri,))  
    consumer.start()  

    consumer.join()
    producer.join()    

main() 
