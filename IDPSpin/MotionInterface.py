__author__ = 'Ivar'

from Leg import Leg
import threading
from FingerControl import FingerControl
from threading import Semaphore
from Move import Move
import time
import math

class MotionInterface(object):
    def __init__(self, mode=1):
        self._Height = 75
        self._Length = 65
        self._DefaultPulse = 375
        self._Multiplier = 1
        self._currentModeInt = mode
        pulses = self.calculatePulse(self._Height, self._Length)
        
        self._Legs = [
            Leg([0x41, 0x41, 0x41], [0, 1, 2], [375, pulses[0], pulses[1]], [0, 0, 0]), #leg 1
            Leg([0x40, 0x40, 0x40], [0, 1, 2], [375, pulses[0], pulses[1]], True, [0, 0, 0]), #leg 2
            Leg([0x41, 0x41, 0x41], [4, 5, 6], [375, pulses[0], pulses[1]], [0, 0, 0]), #leg 3
            Leg([0x40, 0x40, 0x40], [4, 5, 6], [375, pulses[0], pulses[1]], True, [0, 0, 0]), #leg 4
            Leg([0x41, 0x41, 0x41], [8, 9, 10], [375, pulses[0], pulses[1]], [0, 0, 0]), #leg 5
            Leg([0x40, 0x40, 0x40], [8, 9, 10], [375, pulses[0], pulses[1]], True, [0, 0, 0]), #leg 6
        ]
        self._CurrentCommand = 10
        self._Exit = False
        self._Semaphore = threading.Semaphore(1)
        self._ExitSemaphore = threading.Semaphore(1)

        self.SleepTime = 0.0005
        
        if mode == 1:
            self._CurrentMode = Move(self)
        if mode == 2:
            self._CurrentMode = FingerControl(self)

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
        elif height > 150:
            self._Height = 150
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
        elif length > 200:
            self._Length = 200
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

    def convertPulseToDegrees(self, pulse):
        return int(pulse / 2.8125)

    def setDefaultPulse(self, pulse):
        self._DefaultPulse = int(pulse)

    #Inverse kinematics!
    def calculatePulse(self, height, length):

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

        HoekD = 90 - HoekC1

        #Calculate difference in degrees
        if hoekC <= HoekC1:
            differenceInDegreesC = (90 - hoekC - HoekD)
        else:
            differenceInDegreesC = ((HoekC2 - 90)* -1)

        if hoekE <= HoekE2:
            differenceInDegreesE = (HoekE2 * -1)
        else:
            differenceInDegreesE = (HoekE1)

        diffrencePulseE = self.convertDegreesToPulse(differenceInDegreesE)
        diffrencePulseC = self.convertDegreesToPulse(differenceInDegreesC)


        Ankle = int(self._DefaultPulse - diffrencePulseC)
        Knee = int(self._DefaultPulse - diffrencePulseE)

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
        for Leg in self._Legs:
            if number == 1:
                Leg.moveHip(pulse)
            if number == 2:
                Leg.moveAnkle(pulse)
            if number == 3:
                Leg.moveKnee(pulse)


    def raiseLegs(self, Legs):
        steps = 30
        pulses = self.calculatePulse(self._Height, self._Length)
        startpulseAnkle = Legs[0].getAnkle()
        startpulseKnee = Legs[0].getKnee()
        for step in range(1, steps, 1 * self._Multiplier):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self.calculateVerticalPulse(startpulseAnkle, pulses[1] - 95, step, steps)) #was 312
                Leg.moveKnee(self.calculateVerticalPulse(startpulseKnee, pulses[0] - 95, step, steps)) #was 329
            time.sleep(self.SleepTime)

    def LowerLegs(self, Legs):
        steps = 30
        startpulseAnkle = Legs[0].getAnkle() #klopt die array? twee keer 0 voor ankle en knee.
        startpulseKnee = Legs[0].getKnee()
        pulses = self.calculatePulse(self._Height, self._Length)

        for step in range(1, steps, 1 * self._Multiplier):
           #lower leg
            for Leg in Legs:
                Leg.moveAnkle(self.calculateVerticalPulse(startpulseAnkle, pulses[1], step, steps))
                Leg.moveKnee(self.calculateVerticalPulse(startpulseKnee, pulses[0], step, steps)) #startpulseKnee in plaats van Ankle
            time.sleep(self.SleepTime)

    def MoveLegsForward(self, Legs, Raised, Turn):
        if Turn[0] > Turn[1]:
            self.MoveLegsBackward(Legs, Raised, Turn)
            return

        startpoint = Turn[0]
        steps = Turn[1]
        pulses = self.calculatePulse(self._Height, self._Length)
        if Raised:
            pulses[0] -= 90
            pulses[1] -= 90
        for step in range(startpoint, steps, 1 * self._Multiplier):
            #move leg forward
            #pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface.calculateLengthLeg(self._MInterface._Length, step))

            #if Raised:
                #pulses[0] -= 90
                #pulses[1] -= 90

            for Leg in Legs:
                Leg.moveHip(self.calculateHipPulse(step))
            time.sleep(self.SleepTime)


    def MoveLegsBackward(self, Legs, Raised, Turn):
        if Turn[0] < Turn[1]:
            self.MoveLegsForward(Legs, Raised, Turn)
            return

        startpoint = Turn[0]
        steps = Turn[1]
        pulses = self.calculatePulse(self._Height, self._Length)
        if Raised:
            pulses[0] -= 90
            pulses[1] -= 90
        for step in range(startpoint, steps, -1 * self._Multiplier):

            for Leg in Legs:
                Leg.moveHip(self.calculateHipPulse(step))

            time.sleep(self.SleepTime)


    def setDegrees(self, degrees):
        if (degrees < 30 or degrees > 8) and self._currentModeInt == 1:
            try:
                self._CurrentMode._MaxAngle = int(degrees)
                return "Degrees has been set to " + degrees
            except:
                return "invalid input"
        else:
            return "invalid input"

    def getDegrees(self):
        if self._currentModeInt == 1:
            return self._CurrentMode._MaxAngle

    def setMultiplier(self, multiplier):
        if multiplier >= 1 or multiplier <= 3:
            self._Multiplier = int(multiplier)
            return "multiplier has been set to: " + str(multiplier)
        else:
            return "invalid input"

    def getMultiplier(self):
        return self._Multiplier
