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
            Leg([0x41, 0x41, 0x41], [0, 1, 2], [375, 375, 375], [0, 0, 0]), #leg 1
            Leg([0x40, 0x40, 0x40], [0, 1, 2], [375, 375, 375], True, [0, 0, 0]), #leg 2
            Leg([0x41, 0x41, 0x41], [4, 5, 6], [375, 375, 375], [0, 0, 0]), #leg 3
            Leg([0x40, 0x40, 0x40], [4, 5, 6], [375, 375, 375], True, [0, 0, 0]), #leg 4
            Leg([0x41, 0x41, 0x41], [8, 9, 10], [375, 375, 375], [0, 0, 0]), #leg 5
            Leg([0x40, 0x40, 0x40], [8, 9, 10], [375, 375, 375], True, [0, 0, 0]), #leg 6
        ]
        self._CurrentCommand = 10
        self._Exit = False
        self._Semaphore = threading.Semaphore(1)
        self._ExitSemaphore = threading.Semaphore(1)
        self._Height = 100
        self._Length = 160
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
        return "Command " + str(_CurrentCommand) + " has been received"

    def runThread(self):
        self._ExitSemaphore.acquire()
        while self.isExited() == False:
            self._CurrentMode.executeCommand(self.get_CurrentCommand())
            self._ExitSemaphore.release()
            time.sleep(0.001)

    def exit(self):
        self._ExitSemaphore.acquire()
        self._Exit = True
        self._CurrentMode.exit()
        self._ExitSemaphore.release()

    def getSemaphore(self):
        return self._Semaphore

    def getExitSemaphore(self):
        return self._ExitSemaphore

    def isExited(self):
        return self._Exit

    def setHeight(self, height):
        try:
            height = int(height)
        except:
            height = self._Height
        
        if height < 40:
            self._Height = 40
        elif height > 110:
            self._Height = 110
        else:
            self._Height = height

        self.set_CurrentCommand(9)

    def getHeight(self):
        return self._Height

    def setLength(self, length):
        try:
            length = int(length)
        except:
            length = self._Length
        
        if length < 50:
            self._Length = 50
        elif length > 160:
            self._Length = 160
        else:
            self._Length = length

        self.set_CurrentCommand(9)

    def getLength(self):
        return self._Length

    def setSpeed(self, Speed):
        try:
            Speed = int(Speed)
        except:
            Speed = self.SleepTime
        
        if Speed > 0.01:
            self.SleepTime = 0.01
        elif Speed < 0.001:
            self.SleepTime = 0.001
        else:
            self.SleepTime = Speed
    def getSpeed(self):
        return self.SleepTime

    def convertDegreesToPulse(self, pulse):
        return int(pulse * 2.8125)

    def setDefaultPulse(self, pulse):
        self._DefaultPulse = int(pulse)

    #Inverse kinematics!
    def calculatePulse(self, height, length, offsetAnkle = -1, offsetKnee = -1):
        if offsetAnkle == -1:
            offsetAnkle = self._DefaultPulse
        if offsetKnee == -1:
            offsetKnee = self._DefaultPulse

        a = float(height)
        b = float(length)
        c = math.sqrt((a * a) + (b * b))
        d = float(80)
        e = float(145)

        hoekB = math.degrees(math.atan(b/a))

        #Calculate servo angles
        hoekC = float(math.degrees((math.acos(((d * d) + (e * e) - (c * c)) / (2 * d * e)))))
        hoekE = float(math.degrees((math.acos(((c * c) + (d * d) - (e * e)) / (2 * c * d)))))

        HoekE2 = 90 - hoekB
        HoekE1 = hoekE - HoekE2

        HoekC1 = 90 - HoekE1
        HoekC2 = hoekC - HoekC1

        #Calculate difference in degrees
        differenceInDegreesC = (90 - HoekC2)
        differenceInDegreesE = (90 - HoekE1)

        
        diffrencePulseC = self.convertDegreesToPulse(differenceInDegreesC)
        diffrencePulseE = self.convertDegreesToPulse(differenceInDegreesE)

        Ankle = int(offsetAnkle - diffrencePulseC)
        Knee = int(offsetKnee - diffrencePulseE)

        if Knee < 170:
            Knee = 170




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

    def calculateVerticalPulse(self, startingPulse, EndPulse, Step, numberOfSteps=160):
        if Step > numberOfSteps or Step < 1:
            print "Step out of range - " + str(Step)
            raise Exception("")

        pulsedifference = 150 # wordt deze gebruikt?
        if EndPulse < startingPulse:
            pulsedifference = startingPulse - EndPulse
            pulse = startingPulse - int((float(pulsedifference) / float(numberOfSteps)) * Step)
            return pulse
        else:
            pulsedifference = EndPulse - startingPulse
            pulse = startingPulse + int((float(pulsedifference) / float(numberOfSteps)) * Step)
            return pulse

    def getDefaultPulse(self):
        return self._DefaultPulse

    def Calibreren(self, number, pulse):
        for Leg in self._MInterface._Legs:
            if number == 1:
                Leg.moveHip(pulse)
            if number == 2:
                Leg.moveAnkle(pulse)
            if number == 3:
                Leg.moveKnee(pulse)
        



