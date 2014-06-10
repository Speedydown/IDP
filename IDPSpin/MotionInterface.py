__author__ = 'Ivar'

from Leg import Leg
import threading
from threading import Semaphore
import time

class MotionInterface(object):
    def __init__(self):
        self._Legs = [
            Leg([0x41, 0x41, 0x41], [0, 1, 2], [375, 375, 375]), #leg 1
            Leg([0x40, 0x40, 0x40], [0, 1, 2], [375, 375, 375]), #leg 2
            Leg([0x41, 0x41, 0x41], [4, 5, 6], [375, 375, 375]), #leg 3
            Leg([0x40, 0x40, 0x40], [4, 5, 6], [375, 375, 375]), #leg 4
            Leg([0x41, 0x41, 0x41], [8, 9, 10], [375, 375, 375]), #leg 5
            Leg([0x40, 0x40, 0x40], [8, 9, 10], [375, 375, 375]), #leg 6
        ]
        self._CurrentCommand = 10
        self._Exit = False
        self._Semaphore = threading.Semaphore(1)
        self._ExitSemaphore = threading.Semaphore(1)

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



    def exit(self):
        self._ExitSemaphore.acquire()
        self._Exit = True
        self._ExitSemaphore.release()

    def getSemaphore(self):
        return self._Semaphore

    def getExitSemaphore(self):
        return self._ExitSemaphore

    def isExited(self):
        return self._Exit



