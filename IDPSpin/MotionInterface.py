__author__ = 'Ivar'

from Leg import Leg
import threading
from threading import Semaphore
from Move import Move
import time
import math

class MotionInterface(object):
    def __init__(self, mode=1):
        self._Legs = [
            Leg([0x41, 0x41, 0x41], [0, 1, 2], [375, 375, 375]), #leg 1
            Leg([0x40, 0x40, 0x40], [0, 1, 2], [375, 375, 375], True), #leg 2
            Leg([0x41, 0x41, 0x41], [4, 5, 6], [375, 375, 375]), #leg 3
            Leg([0x40, 0x40, 0x40], [4, 5, 6], [375, 375, 375], True), #leg 4
            Leg([0x41, 0x41, 0x41], [8, 9, 10], [375, 375, 375]), #leg 5
            Leg([0x40, 0x40, 0x40], [8, 9, 10], [375, 375, 375], True), #leg 6
        ]
        self._CurrentCommand = 10
        self._Exit = False
        self._Semaphore = threading.Semaphore(1)
        self._ExitSemaphore = threading.Semaphore(1)
        self._Height = 100
        self._Length = 100
        self.SleepTime = 0.01
        self._DefaultPulse = 375
        if mode == 1:
            self._CurrentMode = Move(self)

    def get_CurrentCommand(self):
        self._Semaphore.acquire()
        if self._CurrentCommand is None:
            self._Semaphore.release()
            return 10
        else:
            temp = self._CurrentCommand
            self._Semaphore.release()
            return temp

    def set_CurrentCommand(self, _CurrentCommand):
        self._Semaphore.acquire()
        self._CurrentCommand = _CurrentCommand
        self._Semaphore.release()
        return "Command " + _CurrentCommand + " has been received"

    def runThread(self):
        self._ExitSemaphore.acquire()
        while self.isExited() == False:
            self._CurrentMode.executeCommand(self.get_CurrentCommand())
            self._ExitSemaphore.release()
            time.sleep(0.001)

    def exit(self):
        self._ExitSemaphore.acquire()
        self._Exit = True
        slef._CurrentMode.exit()
        self._ExitSemaphore.release()

    def getSemaphore(self):
        return self._Semaphore

    def getExitSemaphore(self):
        return self._ExitSemaphore

    def isExited(self):
        return self._Exit

    def setHeight(self, height):
        if height < 40:
            self._Height = 40
        elif height > 110:
            heigth._Height = 110
        else:
            self._Height = height

    def getHeight(self):
        return self._Height

    def setLength(self, length):
        if length < 20:
            self._Length = 40
        elif length > 120:
            length._Length = 110
        else:
            self._Length = length

    def getLength(self):
        return self._Length

    def setSpeed(self, Speed):
        if Speed > 0.01:
            self.SleepTime = 0.01
        elif Speed < 0.001:
            length.SleepTime = 0.001
        else:
            self.SleepTime = Speed

    def getSpeed(self):
        return self.SleepTime

    def convertDegreesToPulse(self, pulse):
        return int(pulse * 2.8125)


    #Inverse kinematics!
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
        
        diffrencePulseC = self.convertDegreesToPulse(differenceInDegreesC) * -1
        diffrencePulseE = self.convertDegreesToPulse(differenceInDegreesE) * -1

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
        pulse = self.convertDegreesToPulse(degrees)
        return int(self._DefaultPulse + pulse)

    def calculateKnee(self, height, width):
        a = height
        b = width

        hoekA = math.atan(b / a)

        return (int(hoekA))

    def calculateVerticalPulse(self, StartingPulse, EndPulse, Step, numberOfSteps=160):
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
        



