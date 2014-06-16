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
            elif Command == 18:
                leg1Thread = threading.Thread(target=self.Calibreren())
                leg1Thread.start()

                leg1Thread.join()
                self._LastCommand = 18

    def exit(self):
        pass #exit methode

    def doMove1(self):
        for Leg in self.MInterface._Legs:
            Leg.moveAnkle(280)
        

    def doMove2(self):
        

    def doMove3(self):
        

    def doMove4(self):
        
