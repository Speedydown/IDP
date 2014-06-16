__author__ = 'Ivar'

import time
import threading
import math

from threading import Thread
from MotionInterface import MotionInterface

class GapMove(object):

    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self.group1 = [self._MInterface._Legs[1], self._MInterface._Legs[1]]
        self.group2 = [self._MInterface._Legs[2], self._MInterface._Legs[3]]
        self.group3 = [self._MInterface._Legs[4], self._MInterface._Legs[5]]

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 99:
            self.pullForward()

    def exit(self):
        pass #exit methode

    def PullLegsForward(self, Legs):
        


    def PullForward(self):




