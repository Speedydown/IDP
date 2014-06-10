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
        self.SleepTime = 0.05
        self._PulsesPerDegree = 2.8125
        self._Height = 100
        self._Length = 100
        self._DefaultPulse = 375
        self._LastCommand = 10
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
        self.group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]


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
            self._LastCommand = 11
        elif Command == 12:
            leg1Thread = threading.Thread(target=self.TestMove1)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 12
        elif Command == 13:
            leg1Thread = threading.Thread(target=self.TestMove2)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 13
        elif Command == 14:
            leg1Thread = threading.Thread(target=self.TestMove3)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 14
        elif Command == 15:
            leg1Thread = threading.Thread(target=self.TestMove4)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 15
        elif Command == 16:
            leg1Thread = threading.Thread(target=self.TestMove5)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 16
        elif Command == 17:
            leg1Thread = threading.Thread(target=self.TestMove6)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 17

    def get_CurrentCommand(self):
        return self._MInterface.get_CurrentCommand()

    def set_CurrentCommand(self, _CurrentCommand):
        return self._MInterface.set_CurrentCommand(_CurrentCommand)

    def setHeight(self, height):
        self._Height = height

    def setLength(self, length):
        self._Length = length

    def setSpeed(self, Speed):
        self.SleepTime = Speed

    def exit(self):
        self._MInterface.exit()

    def raiseLegs(self, Legs):
        for step in range(1, 50):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self.calculateNonForwardPulse(Leg.getAnkle(), 312, step, 50))
                Leg.moveKnee(self.calculateNonForwardPulse(Leg.getKnee(), 329, step, 50))
            time.sleep(self.SleepTime)

    def LowerLegs(self, Legs):
        for step in range(1, 50):
           #lower leg
            for Leg in Legs:
                pulses = self.calculatePulse(self._Height, self._Length)
                #print(str(Leg.getAnkle()) + " " + str(pulses[0]) + " " + str(pulses[1]))
                Leg.moveAnkle(self.calculateNonForwardPulse(Leg.getAnkle(), pulses[0], step, 50))
                Leg.moveKnee(self.calculateNonForwardPulse(Leg.getKnee(), pulses[1], step, 50))
            time.sleep(self.SleepTime)

    def MoveLegsForward(self, Legs):
        for step in range(1, 80):
            #move leg forward
            for Leg in Legs:
                pulses = self.calculatePulse(self._Height, self.calculateLengthLeg(self._Length, step / 4), Leg.getAnkle(), Leg.getKnee())
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
            self.raiseLegs(self.group1)
            self.MoveLegsBackward(self.group2)
            self.LowerLegs(self.group1)
        else:
            self.LowerLegs(self.group1)
            self.LowerLegs(self.group2)

    def MoveForward(self):
        #eerste pootbeweging
        if self._LastCommand != 11:
            self.raiseLegs(self.group2)
            self.MoveLegsForward(self.group2)
            self.LowerLegs(self.group2)

        self.raiseLegs(self.group1)
        self.MoveLegsForward(self.group1)
        self.MoveLegsBackward(self.group2)
        self.LowerLegs(self.group1)
        self.raiseLegs(self.group2)
        self.MoveLegsForward(self.group2)
        self.MoveLegsBackward(self.group1)
        self.LowerLegs(self.group2)

    def TestMove1(self):
        self.raiseLegs(self.group1)
    def TestMove2(self):
        self.raiseLegs(self.group2)
    def TestMove3(self):
        self.LowerLegs(self.group1)
    def TestMove4(self):
        self.LowerLegs(self.group2)
    def TestMove5(self):
        self.MoveLegsForward(self.group1)
    def TestMove6(self):
        self.MoveLegsBackward(self.group1)

    #Inverse Kinematics
    def calculateNonForwardPulse(self, StartingPulse, EndPulse, Step, numberOfSteps=160):
        if Step > numberOfSteps or Step < 1:
            print "Step out of range - " + str(Step)
            raise Exception("")

        pulsedifference = 150
        if EndPulse < StartingPulse:
            pulsedifference = StartingPulse - EndPulse
            pulse = StartingPulse - int((float(pulsedifference) / float(numberOfSteps)) * Step)
            return pulse
        else:
            pulsedifference = EndPulse - StartingPulse
            pulse =  StartingPulse + int((float(pulsedifference) / float(numberOfSteps)) * Step)
            return pulse

    def calculatePulse(self, height, length, offsetAnkle = 375, offsetKnee = 375):

        offsetAnkle = self._DefaultPulse
        offsetKnee = self._DefaultPulse

  

        a = height
        b = length
        c = round(math.sqrt((a * a) + (b * b)))
        d = 80
        e = 145

        #Calculate servo angles
        hoekC = float((math.acos(((d * d) + (e * e) - (c * c)) / (2 * d * e))) * 180 / math.pi)
        hoekE = float((math.acos(((c * c) + (d * d) - (e * e)) / (2 * c * d))) * 180 / math.pi)

        hoekE = hoekE + self.calculateKnee(a, b)

        #Calculate difference in degrees
        differenceInDegreesC = (80 - hoekC)
        differenceInDegreesE = (80 - hoekE)

        diffrencePulseC = differenceInDegreesC * self._PulsesPerDegree * -1
        diffrencePulseE = differenceInDegreesE * self._PulsesPerDegree * -1

        print "diffrencePulseC: " + str(diffrencePulseC)
        print "diffrencePulseE: " + str(diffrencePulseE)

        Ankle = int(offsetAnkle + diffrencePulseC)
        Knee = int(offsetKnee + diffrencePulseE)

        if Knee < 170 or Knee > 500:
            Knee = 375

        if Ankle < 170 or Ankle > 500:
            Ankle = 375

        return [Knee, Ankle]

    def calculateLengthLeg(self, widthLeg, forwardDegrees):

        hoekA = float(forwardDegrees)
        b = float(widthLeg)
        a = float((math.tan(math.radians(hoekA))) * b)
        c = float(math.sqrt(a * a + b * b))

        return int(c)

    def calculateHipPulse(self, degrees):
        pulse = degrees * self._PulsesPerDegree
        return int(self._DefaultPulse + pulse)

    def calculateKnee(self, height, width):
        a = height
        b = width

        hoekA = math.atan(b / a)

        return (int(hoekA))






