import NetworkBuffer
import NetworkInterface
import SpinLog
import time
import thread
import threading
import subprocess
#from MotionInterface import MotionInterface
from threading import Thread
from subprocess import call
from Camera import Camera

class Controller(object):

    CommandSize = 4
    
    def __init__(self):
        print "spInOS active"
        self._networkInputBuffer = NetworkBuffer.NetworkBuffer()
        self._NetworkInterface = NetworkInterface.NetworkInterface(self._networkInputBuffer)
        #self._MotionInterface = MotionInterface()
        self._Log = SpinLog.SpinLog()
        self._Camera = Camera()
        self._Exit = False;
                
        self._NetworkInterfaceThread = threading.Thread(target=self._NetworkInterface.run)
        self._NetworkInterfaceThread.start()
        self._CommandHandlerThread = threading.Thread(target=self.CommandHandler)
        self._CommandHandlerThread.start()
    
    def CommandHandler(self):
        while self._Exit == False:
            data = self._networkInputBuffer.Pop()    

            if len(str(data)) > 0:
                ID = data[:6]
                Command = data[6:10]
                self._Log.append(str(data))
                
                if Command == "prin":
                    print(data[10:])
                    self._NetworkInterface.Send("Printed: " + data[11:], ID)
                elif Command == "cocl":
                    self._NetworkInterface.Send(len(self._NetworkInterface._NetworkClients), ID)
                elif Command == "glog":
                    self._NetworkInterface.Send(self._Log.get(), ID)
                elif Command  == "cllg":
                    self._NetworkInterface.Send("Cleared log!", ID)
                    self._Log.clear()
                elif Command == "gcpu":
                    self.gcpu(ID)
                elif Command == "tsen":
                   self._NetworkInterface.Send(self._MotionInterface.test(data[11:]), ID)
                elif Command == "move":
                    self._NetworkInterface.Send(self._MotionInterface.test(data[11:]), ID)
                elif Command == "gimg":
                    self._NetworkInterface.Send(self._Camera.takeImage(), ID)
                elif Command == "gcim":
                    self._NetworkInterface.Send(self._Camera.getImageFromMemory(), ID)
                elif Command == "exit":
                    self._NetworkInterface.Send("Exited", ID)
                    self.Exit()
                    self._Exit = True
                    exit()
                elif Command == "rebt":
                    self._NetworkInterface.Send("Reboot!", ID)
                    self.Exit()
                    self._Exit = True
                    self.Reboot()
                elif Command == "shtd":
                    self._NetworkInterface.Send("Shutting down!", ID)
                    self.Exit()
                    self._Exit = True
                    self.Shutdown()
                    
            time.sleep(0.001)
        print "CommandHandler says goodbye"

    def Exit(self):
        self._NetworkInterface.Exit()
        self._Camera.Exit()

        print "Goodbye"
        
    def Reboot(self):
        self._NetworkInterface.Exit()
        self._Camera.Exit()
        try:
            call(["reboot"])
            print "Goodbye"

            print "BRB"
        except:
            print "Cannot reboot"
        
    def Shutdown(self):
        self._NetworkInterface.Exit()
        self._Camera.Exit()

        try:
            call(["poweroff"])
            print "Goodbye"
        except:
            print "Cannot shut down"

    def gcpu(self, ID):
        cmd = ["top -b -n 10 -d.2 | grep 'Cpu' |  awk 'NR==3{ print($2)}'"]
        result = subprocess.check_output(cmd,shell=True)

        self._NetworkInterface.Send("CPU usage: " + result, ID)
        
                
            

