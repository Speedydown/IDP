from Servo import Servo
#from threading import Semaphore

class Leg(object):

    def __init__(self, AddressArray, ChannelArray, DefaultPulseArray):
        self._AddressArray = AddressArray
        self._ChannelArray = ChannelArray
        self._DefaultPulseArray = DefaultPulseArray
        #self._LegSemaphore = threading.Semaphore(1)
            
        if len(self._AddressArray) == 3:
            self._Hip = Servo(self._AddressArray[0], self._ChannelArray[0], self._DefaultPulseArray[0])
            self._Knee = Servo(self._AddressArray[1], self._ChannelArray[1], self._DefaultPulseArray[1])
            self._Ankle = Servo(self._AddressArray[2], self._ChannelArray[2],self._DefaultPulseArray[2])
        else:
            print "-----------Error Creating leg-----------"
            #"Could not create leg:", sys.exc_info()[0]
            
    def moveHip(self, Pulse):
        self.MoveServo(self._Hip, Pulse)
    
    def moveKnee(self, Pulse):
        self.MoveServo(self._Knee, Pulse)
    
    def moveAnkle(self, Pulse):
        self.MoveServo(self._Ankle, Pulse)

    def MoveServo(self, Servo, Pulse):
        #print "Leg Received: " + Pulse
        if Servo.getPulse() != Pulse:
            Servo.setPulse(Pulse)

        
       

