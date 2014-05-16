__author__ = 'Ivar'

from Leg import Leg

class MotionInterface(object):

    def __init__(self):
        self.Leg1 = Leg(["0x40", "0x40", "0x40"], [0, 1, 2])

    def test(self, Angle):
        self.Leg1.moveAnkle(Angle)
        self.Leg1.moveKnee(Angle)
        self.Leg1.moveHip(Angle)