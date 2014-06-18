__author__ = 'Ivar'

import time
import threading
import math

from threading import Thread
from MotionInterface import MotionInterface

class GapMove(object):

    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[1]]#achterpoten
        self.group2 = [self._MInterface._Legs[2], self._MInterface._Legs[3]]
        self.group3 = [self._MInterface._Legs[4], self._MInterface._Legs[5]]#voorpoten

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 3:
            self.pullForward()

    def exit(self):
        pass #exit methode

    def PullLegsForward(self):
        group1.moveHip(550), group1.moveKnee(200), group1.moveAnkle(550)
        group2.moveHip(375), group2.moveKnee(400), group2.moveAnkle(550)
        group3.moveHip(200), group3.moveKnee(550), group3.moveAnkle(550)

        group1.moveHip(550), group1.moveKnee(250), group1.moveAnkle(550)
        group2.moveHip(375), group2.moveKnee(400), group2.moveAnkle(550)
        group3.moveHip(550), group3.moveKnee(200), group3.moveAnkle(550)


    def PullForward(self, Step, numberSteps=160):
        if Step > numberSteps or Step < 1:
            print "Step out of range - " + str(Step)
            raise Exception("")

        leg1Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = (self.group1))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = (self.group2))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = (self.group3))
        leg3Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()











