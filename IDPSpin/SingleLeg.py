#The class to control only one leg
__author__ = 'Matthe Jacobs'


from MotionInterface import MotionInterface

class SingleLeg(self, MotionInterface):
    def __init__(self, ):
        MotionInterface.__init__(self)

    def ControlLeg1(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(1, pulseHip, pusleKnee, pulseAnkle)

    def ControlLeg2(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(2, pulseHip, pusleKnee, pulseAnkle)

    def ControlLeg3(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(3, pulseHip, pusleKnee, pulseAnkle)

    def ControlLeg4(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(4, pulseHip, pusleKnee, pulseAnkle)

    def ControlLeg5(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(5, pulseHip, pusleKnee, pulseAnkle)

    def ControlLeg6(self, pulseHip, pusleKnee, pulseAnkle):
        moveLeg(6, pulseHip, pusleKnee, pulseAnkle)

    #Function to move the leg
    def moveLeg(self, legNum, pulseHip, pusleKnee, pulseAnkle):    
        if legNum == 1:
            self.Leg1.moveHip(pulseHip)
            self.Leg1.moveKnee(pulseKnee)
            self.Leg1.moveAnkle(pulseAnkle)
        elif legNum == 2:
            self.Leg2.moveHip(pulseHip)
            self.Leg2.moveKnee(pulseKnee)
            self.Leg2.moveAnkle(pulseAnkle)
        elif legNum == 3:
            self.Leg3.moveHip(pulseHip)
            self.Leg3.moveKnee(pulseKnee)
            self.Leg3.moveAnkle(pulseAnkle)
        elif legNum == 4:
            self.Leg4.moveHip(pulseHip)
            self.Leg4.moveKnee(pulseKnee)
            self.Leg4.moveAnkle(pulseAnkle)
        elif legNum == 5:
            self.Leg5.moveHip(pulseHip)
            self.Leg5.moveKnee(pulseKnee)
            self.Leg5.moveAnkle(pulseAnkle)
        elif legNum == 6:
            self.Leg6.moveHip(pulseHip)
            self.Leg6.moveKnee(pulseKnee)
            self.Leg6.moveAnkle(pulseAnkle)
