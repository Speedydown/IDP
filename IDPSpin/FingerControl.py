__author__ = 'Matthe Jacobs'
#Class that gets the finger control pulses and controls a leg with it

from MotionInterface import MotionInterface
import serial

class FingerControl(self, MotionInterface):    
    def __init__(self):
        MotionInterface.__init__(self)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        run()

    def run(self):
        while(True):
            #Read incoming data
            incoming = self.ser.readLine()
            try:
                if incoming[0] == 'a':                    
                    #Move the leg
                    MotionInterface.Legs[0].moveAnkle(int(incoming.strip('a')))
            except ValueError:
                pass
            try:
                if incoming[0] == 'b':
                    #Move the leg
                    MotionInterface.Legs[0].moveKnee(int(incoming.strip('b')))
            except ValueError:
                pass
            
