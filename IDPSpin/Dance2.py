__author__ = 'Speedy'

import time
import math
import threading
from threading import Thread

class Dance2(object):

 def __init__(self, _MotionInterface):
    self._MotionInterface = _MotionInterface
    self.SleepTime = 0.02

    self.WaveLegs = [self._MotionInterface._Legs[0], self._MotionInterface._Legs[2], self._MotionInterface._Legs[4], self._MotionInterface._Legs[5], self._MotionInterface._Legs[3], self._MotionInterface._Legs[1]]
    self.Legs = self._MotionInterface._Legs

    leg1Thread = threading.Thread(target=self.Dance)
    leg1Thread.start()

 def executeCommand(self, Command):
    pass

 def Dance(self):
     #wave
     self._MotionInterface.setHeight(55)
     self._MotionInterface.LowerLegs(self.Legs)

     steps = 50

     for Leg in self.WaveLegs:
         startposAnkle = Leg.getAnkle()

         for step in range(1, steps):
            Leg.moveAnkle(self._MotionInterface.calculateVerticalPulse(startposAnkle, startposAnkle + 450, step, steps))
            time.sleep(self.SleepTime)

     for i in range(0, 3):
         self._MotionInterface.MoveLegsForward(self.WaveLegs, False, [ 0, 60])
         self._MotionInterface.MoveLegsBackward(self.WaveLegs, False, [ 60, 0])




     for Leg in reversed(self.WaveLegs):
         startposAnkle = Leg.getAnkle()

         for step in range(1, steps):
            Leg.moveAnkle(self._MotionInterface.calculateVerticalPulse(startposAnkle, startposAnkle - 450, step, steps))
            time.sleep(self.SleepTime)

     self._MotionInterface.setHeight(75)
     self._MotionInterface.LowerLegs(self.Legs)


     self.shake()

     self.forwardLegs()
     #self._MotionInterface.LowerLegs(self.Legs)


 def forwardLegs(self):
     group1 = [self._MotionInterface._Legs[0], self._MotionInterface._Legs[2], self._MotionInterface._Legs[4]]
     group2 = [self._MotionInterface._Legs[1], self._MotionInterface._Legs[3], self._MotionInterface._Legs[5]]

     steps = 50

     self._MotionInterface.raiseLegs([group1[1], group2[1]])
     self._MotionInterface.MoveLegsForward([group1[1], group2[1]], True, [0,30])
     self._MotionInterface.LowerLegs([group1[1], group2[1]])

     self._MotionInterface.raiseLegs([group1[2], group2[2]], [-450, 90])
     self._MotionInterface.MoveLegsForward([group1[2], group2[2]], True, [0, 90])

     self._MotionInterface.raiseLegs([group1[0], group2[0]], [-300, 0])


 def shake(self):
    group = self._MotionInterface._Legs
    angle = 20

    self._MotionInterface.setMultiplier(2)

    self._MotionInterface.MoveLegsForward(group, False, [0, angle])
    self._MotionInterface.MoveLegsBackward(group, False, [angle, -angle])
    self._MotionInterface.MoveLegsForward(group, False, [-angle, angle])
    self._MotionInterface.MoveLegsBackward(group, False, [angle, -angle])
    self._MotionInterface.MoveLegsForward(group, False, [-angle, angle])
    self._MotionInterface.MoveLegsBackward(group, False, [angle, -angle])
    self._MotionInterface.MoveLegsForward(group, False, [-angle, angle])
    self._MotionInterface.MoveLegsBackward(group, False, [angle, -angle])
    self._MotionInterface.MoveLegsForward(group, False, [-angle, angle])
    self._MotionInterface.MoveLegsBackward(group, False, [angle, 0])


 def exit(self):
     self._MotionInterface.setHeight(75)
     self._MotionInterface.LowerLegs(self.Legs)

