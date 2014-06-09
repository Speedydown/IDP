from MotionInterface import MotionInterface
from MovementAction import MovementAction
import time
import threading
import math
from threading import Thread

class Move(MotionInterface):

    def __init__(self):
        self._MInterface = MotionInterface()
        self._Stop = False
        self.SleepTime = 0.005
        self._PulsesPerDegree = 2.8125
        self._Height = 40
        self._Length = 100
        self._DefaultPulse = 375
        self._LastCommand = 10


    def runThread(self):

        self._MInterface.getExitSemaphore().acquire()
        while self._MInterface.isExited() == False:
            self.executeCommand(self._MInterface.get_CurrentCommand())
            self._MInterface.getExitSemaphore().release()
            time.sleep(0.001)

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 10:
            leg1Thread = threading.Thread(target=self.StopLegs)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 10;
        elif Command == 11:
            leg1Thread = threading.Thread(target=self.MoveForward)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 11;

    def get_CurrentCommand(self):
        return self._MInterface.get_CurrentCommand()

    def set_CurrentCommand(self, _CurrentCommand):
        return self._MInterface.set_CurrentCommand(_CurrentCommand)

    def setHeight(self, height):
        self._Height = height

    def setLength(self, length):
        self._Length = length

    def exit(self):
        self._MInterface.exit()

    def raiseLegs(self, Legs):
        for step in range(1, 50):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self.calculateNonForwardPulse(self._DefaultPulse, 312, step, 50))
                Leg.moveKnee(self.calculateNonForwardPulse(self._DefaultPulse, 329, step, 50))
            time.sleep(self.SleepTime)

    def LowerLegs(self, Legs):
        for step in range(1, 50):
           #lower leg
            for Leg in Legs:
                Leg.moveAnkle(self.calculateNonForwardPulse(312, self._DefaultPulse, step, 50))
                Leg.moveKnee(self.calculateNonForwardPulse(329, self._DefaultPulse, step, 50))
            time.sleep(self.SleepTime)

    def MoveLegsForward(self, Legs):
        for step in range(1, 80):
            #move leg forward
            for Leg in Legs:
                pulses = self.calculatePulse(self._Height, self.calculateLengthLeg(self._Length, step / 4), 312, 329)
                Leg.moveHip(self.calculateHipPulse(step / 4))
                Leg.moveKnee(pulses[0])
                Leg.moveAnkle(pulses[1])
        time.sleep(self.SleepTime)


    def MoveLegsBackward(self, Legs):
        for step in range(1, 80):
            #move leg backward
            for Leg in Legs:
                pulses = self.calculatePulse(self._Height, self.calculateLengthLeg(self._Length, (80 - step) / 4))
                Leg.moveHip(self.calculateHipPulse((80 - step) / 4))
                Leg.moveKnee(pulses[0])
                Leg.moveAnkle(pulses[1])
            time.sleep(self.SleepTime)

    def StopLegs(self):
        if self._LastCommand == 11:
            self.raiseLeg(group1)
            self.MoveLegsBackward(group2)
            self.LowerLegs(group1)


    def MoveForward(self):
        group1 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
        group2 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]

        if self._LastCommand != 11:
            self.raiseLegs(group2)
            self.MoveLegsForward(group2)
            self.LowerLegs(group2)

        self.raiseLeg(group1)
        self.MoveLegsForward(group1)
        self.MoveLegsBackward(group2)
        self.LowerLegs(group1)
        self.raiseLeg(group2)
        self.MoveLegsForward(group2)
        self.MoveLegsBackward(group1)
        self.LowerLegs(group2)

    #Inverse Kinematics
    def calculateNonForwardPulse(self, StartingPulse, EndPulse, Step, numberOfSteps=160):
        if Step > numberOfSteps or Step < 1:
            print "Step out of range - " + str(Step)
            raise Exception("")

        pulsedifference = 150
        if EndPulse < StartingPulse:
            pulsedifference = StartingPulse - EndPulse
            pulse = StartingPulse - int((float(pulsedifference) / float(numberOfSteps)) * Step)
            print pulse
            return pulse
        else:
            pulsedifference = EndPulse - StartingPulse
            pulse =  StartingPulse + int((float(pulsedifference) / float(numberOfSteps)) * Step)
            print pulse
            return pulse

    def calculatePulse(self, height, length, offsetAnkle = self._DefaultPulse, offsetKnee = self._DefaultPulse):

        a = height
        b = length
        c = round(math.sqrt((a * a) + (b * b)))
        d = 80
        e = 125

        #Calculate servo angles
        hoekC = float((math.acos(((d * d) + (e * e) - (c * c)) / (2 * d * e))) * 180 / math.pi)
        hoekE = float((math.acos(((c * c) + (d * d) - (e * e)) / (2 * c * d))) * 180 / math.pi)

        #Calculate difference in degrees
        differenceInDegreesC = (80 - hoekC)
        differenceInDegreesE = (80 - hoekE)

        diffrencePulseC = differenceInDegreesC * self._PulsesPerDegree * -1;
        diffrencePulseE = differenceInDegreesE * self._PulsesPerDegree * -1;

        Ankle = int(offsetAnkle + diffrencePulseC)
        Knee = int(offsetKnee + diffrencePulseE)

        return [Knee, Ankle]

    def calculateLengthLeg(self, widthLeg, forwardDegrees):

        hoekA = float(forwardDegrees)
        b = float(widthLeg)
        a = float((Math.Tan(hoekA * Math.PI / 180) * b))
        c = float(Math.Sqrt((a * a + b * b)))

        return c

    def calculateHipPulse(self, degrees):
        pulse = degrees * self._PulsesPerDegree
        return self._DefaultPulse + pulse







