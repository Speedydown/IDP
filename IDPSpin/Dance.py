__author__ = 'Matthe Jacobs'

import time
import threading
import math
from threading import Thread

from MotionInterface import MotionInterface

class Dance(self, MotionInterface):
    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self._LastCommand = 9
        self._MaxAngle = 20
        self._MinAngle = 6
        self._DefaultMaxAngle = 20
        self._DefaultMinAngle = 6
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[3], self._MInterface._Legs[4]]
        self.group2 = [self._MInterface._Legs[1], self._MInterface._Legs[2], self._MInterface._Legs[5]]

    def executeCommand(self, Command):
            Command = int(Command)

            if Command == 9:
                self._LastCommand = 9;
                self._MInterface.set_CurrentCommand(10)
                self.StopLegs()
                self._LastCommand = 10;
            elif Command == 10:
                self.StopLegs()
                self._LastCommand = 10;
            elif Command == 11:
                self.DoMoveLower()
                self._LastCommand = 11
            elif Command == 12:
                self.DoMoveHigher()
                self._LastCommand = 12
            elif Command == 13:
                self.DoMoveLower()
                self._LastCommand = 13
            elif Command == 14:
                self.MoveBackwardAndRotate(True)
                self._LastCommand = 14
            elif Command == 15:
                self.MoveBackward()
                self._LastCommand = 15
            elif Command == 16:
                self.MoveBackwardAndRotate(False)
                self._LastCommand = 16
            elif Command == 17:
                self.Rotate(True)
                self._LastCommand = 17
            elif Command == 18:
                self.MoveForwardAndRotate(False)
                self._LastCommand = 18
            
    def exit(self):
        pass #exit methode

    def startPos(self):        

    def doMoveHigher(self, Legs):
        steps = 30
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        startpulseAnkle = Legs[0].getAnkle()
        startpulseKnee = Legs[0].getKnee()
        for step in range(1, steps):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[1] - 95, step, steps)) #was 312
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[0] - 95, step, steps)) #was 329
            time.sleep(self._MInterface.SleepTime)

            self.startPos()

    def doMoveLower(self, Legs):
        steps = 30
        startpulseAnkle = Legs[0].getAnkle() #klopt die array? twee keer 0 voor ankle en knee.
        startpulseKnee = Legs[0].getKnee()
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)

        for step in range(1, steps):
           #lower leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[1], step, steps))
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[0], step, steps)) #startpulseKnee in plaats van Ankle
            time.sleep(self._MInterface.SleepTime)

            self.startPos()


    def doMoveRotateLeft(self):
            group1 = [self._MInterface._Legs[4], self._MInterface._Legs[2], self._MInterface._Legs[0]]
            group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]

    def doMoveRotateRight(self):
        

    def doMoveThreeLegsUp1(self, Legs):
        self.doMoveHigher(self.group1)
        
    def doMoveThreeLegsUp2(self):
        self.DoMoveHigher(self.group2)
