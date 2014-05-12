import threading
from threading import Semaphore

class NetworkBuffer(object):

    def __init__(self):
        self.Input = []
        self.Output = []
        self.InputSemaphore = threading.Semaphore(1)
        self.OutputSemaphore = threading.Semaphore(1)
        
    def Append(self, var):       
        self.InputSemaphore.acquire()
        self.Input.append(var)
        self.InputSemaphore.release()

    def Pop(self):
        self.InputSemaphore.acquire()
        
        output = ""
        try:
            output = self.Input.pop()
        except:
            output = ""
        self.InputSemaphore.release()
        return output

    
