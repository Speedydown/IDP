__author__ = 'Ivar'

from Leg import Leg
from threading import Semaphore
import time

class MotionInterface(object):
    def __init__(self):
        self._Legs = [
            Leg(["0x40", "0x40", "0x40"], [0, 1, 3], [375, 375, 375])
        ]
        self._currentCommand = 0
        self._Exit = False
        self.Semaphore = threading.Semaphore(1)
        self.ExitSemaphore = threading.Semaphore(1)

    def get_CurrentCommand(self):
        self.Semaphore.aquire()
        if self._currentCommand is None:
            self.Semaphore.release()
            return 10
        else:
            temp = self._CurrentCommand
            self.Semaphore.release()
            return self._currentCommand

    def set_CurrentCommand(self, _CurrentCommand):
        self.Semaphore.aquire()
        self._CurrentCommand = _CurrentCommand
        self.Semaphore.release()
        return "Command " + _CurrentCommand + " has been received"

    def run(self):
        self.ExitSemaphore.aquire()
        while self._Exit == False:
            self.executeCommand(self.get_CurrentCommand())
            self.ExitSemaphore.release()
            time.sleep(0.001)


    def executeCommand(self, Command):
        pass

    def exit(self):
        self.ExitSemaphore.aquire()
        self._Exit = True
        self.ExitSemaphore.release()



