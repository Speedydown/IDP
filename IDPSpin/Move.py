from MotionInterface import MotionInterface
import time
class Move(MotionInterface):

    def __init__(self):
        MotionInterface.__init__(self)
        self._Stop = False

    def moveForward(self):

        while self._Stop == False:
            #MotionInterface.Leg1.moveHip(375)
            MotionInterface.Leg1.moveKnee(347)
            MotionInterface.Leg1.moveAnkle(339)
            time.sleep(1)
            MotionInterface.Leg1.moveKnee(355)
            MotionInterface.Leg1.moveAnkle(360)





