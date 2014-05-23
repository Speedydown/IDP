__author__ = 'Matthé Jacobs'

from MotionInterface import MotionInterface
from Adafruit_PWM_Servo_Driver import PWM
import serial

class FingerControl(self, MotionInterface):    
    def __init__(self):
        MotionInterface.__init__(self)
        run()

    def run(self):
        while(True):
            incoming = ser.readLine()

            try:
                if incoming[0] == 'a':
                    incomingInt = int(incoming.strip('a'))
                    MotionInterface.Leg1.moveAnkle(incomingInt)
            except ValueError:
                pass
            try:
                if incoming[0] == 'b':
                    incomingInt = int(incoming.strip('b'))
                    MotionInterface.Leg1.moveKnee(incomingInt)
            except ValueError:
                pass
            
