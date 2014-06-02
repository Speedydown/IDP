__author__ = 'Ivar'

from Servo import Servo

class Leg(object):
    """
    All 6 legs will be added to an array. All the address and channels of the specific leg will be added
    into an array. The starting position of the spider is put into an array.
    The leg is defined in 3 groups: Hip, Knee and Ankle.
    """


    def __init__(self, AddressArray, ChannelArray, DefaultPulseArray):
        self._AddressArray = AddressArray
        self._ChannelArray = ChannelArray
        self._DefaultPulseArray = DefaultPulseArray

    # Make address on for 3 servos. First Hip then Knee and last Ankle
        if len(self._AddressArray) == 3:
            self._Hip = Servo(self._AddressArray[0], self._ChannelArray[0], self._DefaultPulseArray[0])
            self._Knee = Servo(self._AddressArray[1], self._ChannelArray[1], self._DefaultPulseArray[1])
            self._Ankle = Servo(self._AddressArray[2], self._ChannelArray[2],self._DefaultPulseArray[2])
        else:
            print "-----------Error Creating leg-----------"

    # Moving the Hip of the Leg
    def moveHip(self, Pulse):
        self._Hip.setPulse(Pulse)

    # Moving the Knee of the Leg
    def moveKnee(self, Pulse):
        self._Knee.setPulse(Pulse)

    # Moving the Ankle of the Leg
    def moveAnkle(self, Pulse):
        self._Ankle.setPulse(Pulse)

    # Moving the full leg to starting position. Pulse will be set on 375
    def defaultPos(self):
        self.moveHip(self._Hip, self._DefaultPulseArray[0])
        self.moveKnee(self._Knee, self._DefaultPulseArray[1])
        self.moveAnkle(self._Ankle, self._DefaultPulseArray[2])

        
       

