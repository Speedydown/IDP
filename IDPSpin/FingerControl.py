__author__ = 'Matthe Jacobs'
#Class that gets the finger control pulses and controls a leg with it

from MotionInterface import MotionInterface
import serial

class FingerControl(self, MotionInterface):    
    def __init__(self):
        MotionInterface.__init__(self)
        run()

    def run(self):
        while(True):
            #Read incoming data
            incoming = ser.readLine()
            try:
                if incoming[0] == 'a':
                    incomingInt = int(incoming.strip('a'))
                    #Move the leg
                    MotionInterface.Leg1.moveAnkle(incomingInt)
            except ValueError:
                pass
            try:
                if incoming[0] == 'b':
                    incomingInt = int(incoming.strip('b'))
                    #Move the leg
                    MotionInterface.Leg1.moveKnee(incomingInt)
            except ValueError:
                pass
            
