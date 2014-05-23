__author__ = 'Ivar'

from Leg import Leg

class MotionInterface(object):

    def __init__(self):
        self.Leg1 = Leg(["0x40", "0x40", "0x40"], [0, 1, 2], [600, 350, 375])

    def test(self, Pulse):
        print "Pulse: " + Pulse
        self.Leg1.moveAnkle(int(Pulse[:3]))
        self.Leg1.moveKnee(int(Pulse[:3]))
        self.Leg1.moveHip(int(Pulse[:3]))

        return "moved servo: " + Pulse
