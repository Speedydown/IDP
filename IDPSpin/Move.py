from MotionInterface import MotionInterface
import time

class Move(MotionInterface):

    def __init__(self):
        MotionInterface.__init__(self)
        self._Stop = False




    def moveForward(self):

        while self._Stop == False:
            #MotionInterface.Leg1.moveHip(375)
            #MotionInterface.Leg1.moveKnee(451);
            MotionInterface.Leg1.moveAnkle(236)





