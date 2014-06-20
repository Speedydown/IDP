import NetworkBuffer
import NetworkInterface
import SpinLog
import time
import thread
import threading
import subprocess
from MotionInterface import MotionInterface
from GyroData import GyroData
from GetSpiData import GetSpiData
from Move import Move
from threading import Thread
from subprocess import call
from Camera import Camera
from IOPIN import IOPIN

class Controller(object):

    CommandSize = 4
    
    def __init__(self):
        print "spInOS active"
        self._networkInputBuffer = NetworkBuffer.NetworkBuffer()
        self._NetworkInterface = NetworkInterface.NetworkInterface(self._networkInputBuffer)
        self._MotionInterface = MotionInterface(1)
        self._SPIData = GetSpiData()
        self._GyroData = GyroData()
        self._Log = SpinLog.SpinLog()
        self._IOPIN = IOPIN()
        self._Camera = Camera()
        self._Exit = False;
        self._Mode = 1
                
        self._NetworkInterfaceThread = threading.Thread(target=self._NetworkInterface.run)
        self._NetworkInterfaceThread.start()
        self._CommandHandlerThread = threading.Thread(target=self.CommandHandler)
        self._CommandHandlerThread.start()
        self._MotionInterfaceThread = threading.Thread(target=self._MotionInterface.runThread)
        self._MotionInterfaceThread.start()
    
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
                elif Command == "gspi":
                    self._NetworkInterface.Send(self._SPIData.getSpi(), ID)
                elif Command == "smde":
                    self._Mode = data[11:12]
                    self._MotionInterface.exit()
                    if int(self._Mode) == 1:
                        self._MotionInterface = MotionInterface(1)
                    if int(self._Mode) == 2:
                        self._MotionInterface = MotionInterface(2)
                    if int(self._Mode) == 3:
                        self._MotionInterface = MotionInterface(3)
                    if int(self._Mode) == 4:
                        self._MotionInterface = MotionInterface(4)
                    print threading.currentThread()
                    self._NetworkInterface.Send("Mode set to:" + self._Mode, ID)
                    self._MotionInterfaceThread = threading.Thread(target=self._MotionInterface.runThread)
                    self._MotionInterfaceThread.start()
                elif Command == "gmde":
                    self._NetworkInterface.Send(self._Mode, ID)
                elif Command == "move":
                    self._NetworkInterface.Send(self._MotionInterface.set_CurrentCommand(data[11:13]), ID)
                elif Command == "slen":
                    self._MotionInterface.setLength(data[11:14])
                    self._NetworkInterface.Send("length has been set", ID)
                elif Command == "shgt":
                    self._MotionInterface.setHeight(data[11:14])
                    self._NetworkInterface.Send("height has been set to:" + data[11:14], ID)
                elif Command == "sspd":
                    self._MotionInterface.setSpeed(data[11:17])
                    self._NetworkInterface.Send("Speed has been set to:" + data[11:14], ID)
                elif Command == "spul":
                    self._MotionInterface.setDefaultPulse(data[11:17])
                    self._NetworkInterface.Send("Defaultpulse has been updated", ID)
                elif Command == "cali":
                    self._MotionInterface.Calibreren(data[11:12], data[14:17])
                    self._NetworkInterface.Send("Defaultpulse has been updated", ID)
                elif Command == "gimg":
                    self._NetworkInterface.Send(self._Camera.takeImage(), ID)
                elif Command == "gifm":
                    self._NetworkInterface.Send(self._Camera.getImageFromMemory(), ID)
                elif Command == "ping":
                    self._NetworkInterface.Send("ping", ID)
                elif Command == "sdeg":
                    self._NetworkInterface.Send(self._MotionInterface.setDegrees(data[11:13]), ID)
                elif Command == "gdeg":
                    self._NetworkInterface.Send(self._MotionInterface.getDegrees(), ID)
                elif Command == "ggyr":
                    self._NetworkInterface.Send(self._GyroData.getDegrees(), ID)
                elif Command == "smul":
                    self._NetworkInterface.Send(self._MotionInterface.setMultiplier(data[11:12]), ID)
                elif Command == "gmul":
                    self._NetworkInterface.Send(self._MotionInterface.getMultiplier(), ID)
                elif Command == "horn":
                    self._IOPIN.Horn()
                    self._NetworkInterface.Send("toot toot!", ID)
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
                else:
                    self._NetworkInterface.Send("Could not execute command", ID)

                    
            time.sleep(0.001)
        print "CommandHandler says goodbye"

    def Exit(self):
        self._NetworkInterface.Exit()
        self._Camera.Exit()
        self._MotionInterface.exit()

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
        
                
            

