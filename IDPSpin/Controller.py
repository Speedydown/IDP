import NetworkBuffer
import NetworkInterface
import time
import thread
import threading
from threading import Thread

class Controller(object):

    CommandSize = 4
    
    def __init__(self):
        self._networkInputBuffer = NetworkBuffer.NetworkBuffer()
        self._networkOutputBuffer = NetworkBuffer.NetworkBuffer()
        self._NetworkInterface = NetworkInterface.NetworkInterface(self._networkInputBuffer, self._networkOutputBuffer)
        self._Exit = False;
                
        self._NetworkInterfaceThread = threading.Thread(target=self._NetworkInterface.run)
        self._NetworkInterfaceThread.start()
        self._CommandHandlerThread = threading.Thread(target=self.CommandHandler)
        self._CommandHandlerThread.start()
    
    def CommandHandler(self):
        while self._Exit == False:
            data = self._networkInputBuffer.Pop()    

            if len(str(data)) > 0:
                Command = data[:4]

                if Command == "prin":
                    #roep print methode aan
                    try:
                        print(data[5:]) #Temp
                    except:
                        pass
                elif Command == "glog":
                    #roep log aan en verstuur
                    self._networkOutputBuffer.Append("hier komt een log!")
                elif Command == "exit":
                    self.Exit()
                    self._Exit = True
            time.sleep(1)

    def Exit(self):
        self._NetworkInterface.Exit()

        print "Goodbye"
        #linux commandos
        
                
            

