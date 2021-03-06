from Servo import Servo
from threading import Semaphore

class Leg(object):

    def __init__(self, AddressArray, ChannelArray):
        self._AddressArray = AddressArray
        self._ChannelArray = ChannelArray
        self._LegSemaphore = threading.Semaphore(1)
            
        if len(_AddressArray) == 3:
            self._Hip = Servo(_AddressArray[0], _ChannelArray[0])
            self._Knee = Servo(_AddressArray[1], _ChannelArray[1])
            self._Ankle = Servo(_AddressArray[2], _ChannelArray[2])
        else:
            print "-----------Error Creating less-----------"
            "Could not create leg:", sys.exc_info()[0]
            
    def moveHip(self, Angle):
        return self.MoveServo(_Hip, Angle)
    
    def moveKnee(self, Angle):
        return self.MoveServo(_Knee, Angle)
    
    def moveAnkle(self, Angle):
        return self.MoveServo(_Ankle, Angle)

    def MoveServo(self, Servo, Angle):

        if Servo.getAngle() != Angle:
            Servo.SetAngle(Angle)

            #voor TestDoeleiden
            return "Moved servo to: " + Angle
        
       

