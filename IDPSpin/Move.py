import time
import threading
import math
from threading import Thread

class Move():

    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self._LastCommand = 9
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[3], self._MInterface._Legs[4]]
        self.group2 = [self._MInterface._Legs[1], self._MInterface._Legs[2], self._MInterface._Legs[5]]

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 9:
            self._LastCommand = 9;
            self._MInterface.set_CurrentCommand(10)
            leg1Thread = threading.Thread(target=self.StopLegs)
            leg1Thread.start()

            leg1Thread.join()
            self._LastCommand = 10;
        elif Command == 10:
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

    def exit(self):
        pass #exit methode

    def raiseLegs(self, Legs):
        steps = 50
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        startpulseAnkle = Legs[0].getAnkle() #klopt die array? twee keer 0 voor ankle en knee.
        startpulseKnee = Legs[0].getKnee()
        for step in range(1, steps):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[0] - 95, step, steps)) #was 312
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[1] - 95, step, steps)) #was 329
            time.sleep(self._MInterface.SleepTime)

    def LowerLegs(self, Legs):
        steps = 50
        startpulseAnkle = Legs[0].getAnkle() #klopt die array? twee keer 0 voor ankle en knee.
        startpulseKnee = Legs[0].getKnee()
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        for step in range(1, steps):
           #lower leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[0], step, steps))
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[1], step, steps)) #startpulseKnee in plaats van Ankle
            time.sleep(self._MInterface.SleepTime)

    def MoveLegsForward(self, Legs):
        offsetAnkle = 280 #Legs[0].getAnkle()
        offsetKnee = 280#Legs[0].getKnee()
        steps = 80
        for step in range(1, steps):
            #move leg forward
            for Leg in Legs:
                pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface.calculateLengthLeg(self._MInterface._Length, step / 4), offsetAnkle, offsetKnee)
                Leg.moveHip(self._MInterface.calculateHipPulse(step / 4))
                Leg.moveKnee(pulses[0])
                Leg.moveAnkle(pulses[1])
            time.sleep(self._MInterface.SleepTime)


    def MoveLegsBackward(self, Legs):
        offsetAnkle = Legs[0].getAnkle() #Zelfde verhaal als de andere array
        offsetKnee = Legs[0].getKnee()
        steps = 80
        for step in range(1, steps):
            #move leg backward
            for Leg in Legs:
                pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface.calculateLengthLeg(self._MInterface._Length, (steps - step) / 4), offsetAnkle, offsetKnee)
                Leg.moveHip(self._MInterface.calculateHipPulse((steps - step) / 4))
                Leg.moveKnee(pulses[0])
                Leg.moveAnkle(pulses[1])
            time.sleep(self._MInterface.SleepTime)

    def StopLegs(self):
        #laatste pootbeweging
        if self._LastCommand == 11:
            self.raiseLegs(self.group1)
            self.MoveLegsBackward(self.group2)
            self.LowerLegs(self.group1)
        elif self._LastCommand == 9:
            self.LowerLegs(self._MInterface._Legs)
        else:
            pass

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
        for Leg in self._MInterface._Legs:
            Leg.moveAnkle(280)
    def TestMove3(self):
        self.LowerLegs(self.group1)
    def TestMove4(self):
        self.LowerLegs(self.group2)
    def TestMove5(self):
        self.MoveLegsForward(self.group1)
    def TestMove6(self):
        self.MoveLegsBackward(self.group1)

    

    

    






