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
        #groups = [self.group1, self.group2, self.group3]
        AnkleStartpoint = self.group1[0].getAnkle()
        KneeStartpoint = self.group1[0].getKnee()
        HipStartpoint = self.group1[0].getHip()

        for Leg in group1:
            steps = 50

            for step in range(1, steps):
                for Leg in group1:
                    Leg.moveAnkle(self._MInterface.calculateVerticalPulse(AnkleStartpoint, 400, step, steps))
                    Leg.moveKnee(self._MInterface.calculateVerticalPulse(KneeStartpoint, 375, step, steps))
                time.sleep(self.SleepTime)

            for step in range(1, 20):
                Leg.moveHip(self._MInterface.calculateVerticalPulse(HipStartpoint, 550, step, steps))
            time.sleep(self.SleepTime)

        for Leg in group2:
            steps = 50

            for step in range(1, steps):
                for Leg in group2:
                    Leg.moveAnkle(self._MInterface(AnkleStartpoint, 400, step, steps))
                    Leg.moveKnee(self._MInterface(KneeStartpoint, 400, step, steps))
                time.sleep(self._MInterface.SleepTime)

                for step in range(1, 20):
                    Leg.moveHip(self._MInterface(HipStartpoint, 375, step, steps))

        for Leg in group3:
            steps = 50

            for step in range(1, steps):
                for Leg in group3:
                    Leg.moveAnkle(self._MInterface(AnkleStartpoint, 400, step, steps))
                    Leg.moveKnee(self._MInterface(KneeStartpoint, 550, step, steps))
                time.sleep(self.SleepTime)

            for step in range(1, 20):
                Leg.moveHip(self._MInterface(HipStartpoint, 550, step, steps))
            time.sleep(self.SleepTime)


        for Leg in group1:
            steps = 50

            for step in range(1, steps):
                for Leg in group1:
                    Leg.moveAnkle(self._MInterface.calculateVerticalPulse(AnkleStartpoint, 550, step, steps))
                    Leg.moveKnee(self._MInterface.calculateVerticalPulse(KneeStartpoint, 200, step, steps))
                time.sleep(self.SleepTime)

            for step in range(1, 20):
                Leg.moveHip(self._MInterface(HipStartpoint, 550, step, steps))
            time.sleep(self.SleepTime)


        for Leg in group3:
            steps = 50

            for step in range(1, steps):
                for Leg in group3:
                    Leg.moveAnkle(self._MInterface(AnkleStartpoint, 550, step, steps))
                    Leg.moveKnee(self._MInterface(KneeStartpoint, 400, step, steps))
                time.sleep(self.SleepTime)

            for step in range(1, 20):
                Leg.moveHip(self._MInterface(HipStartpoint, 550, step, steps))
            time.sleep(self.SleepTime)


    def PullForward(self):
        leg1Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = ([self.group1]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = ([self.group2]))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self._MInterface.PullLegsForward, args = ([self.group3]))
        leg3Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()











