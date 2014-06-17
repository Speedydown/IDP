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

        if Command == 99:
            self.pullForward()

    def exit(self):
        pass #exit methode

    def PullLegsForward(self):
        group1.moveAnkle(150), group1.moveKnee(150), group1.moveHip(150)
        group2.moveAnkle(550), group2.moveKnee(550), group2.moveHip(375)
        group3.moveAnkle(600), group3.moveKnee(600), group3.moveHip(600)

    def PullForward(self):







