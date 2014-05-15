import NetworkBuffer
import NetworkInterface
import SpinLog
import time
import thread
import threading
from threading import Thread
from subprocess import call

class Controller(object):

    CommandSize = 4
    
    def __init__(self):
        print "spInOS active"
        self._networkInputBuffer = NetworkBuffer.NetworkBuffer()
        self._networkOutputBuffer = NetworkBuffer.NetworkBuffer()
        self._NetworkInterface = NetworkInterface.NetworkInterface(self._networkInputBuffer, self._networkOutputBuffer)
        self._Log = SpinLog.SpinLog()
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
                self._Log.append(str(data))
                
                if Command == "prin":
                    try:
                        print(data[5:])
                        self._networkOutputBuffer.Append("Printed: " + data[5:])
                    except:
                        pass
                elif Command == "glog":
                    self._networkOutputBuffer.Append(self._Log.get())
                elif Command  == "cllg":
                    self._networkOutputBuffer.Append("Cleared log!")
                    self._Log.clear()
                elif Command == "exit":
                    self._networkOutputBuffer.Append("Exited")
                    self.Exit()
                    self._Exit = True
                elif Command == "rebt":
                    self._networkOutputBuffer.Append("Reboot!")
                    self._Exit = True
                    self.Reboot()
                elif Command == "shtd":
                    self._networkOutputBuffer.Append("Shutting down!")
                    self._Exit = True
                    self.Shutdown()
                    
            time.sleep(1)

    def Exit(self):
        self._NetworkInterface.Exit()

        print "Goodbye"
        
    def Reboot(self):
        self._NetworkInterface.Exit()
        try:
            call(["shutdown", "-r", "NOW"])
            print "BRB"
        except:
            print "Cannot reboot"
        
    def Shutdown(self):
        self._NetworkInterface.Exit()

        try:
            call(["poweroff"])
            print "Goodbye"
        except:
            print "Cannot shut down"
        
                
            

