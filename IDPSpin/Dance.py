__author__ = 'Matthe Jacobs'

import time
import threading
import math
from threading import Thread

from MotionInterface import MotionInterface

class Dance(MotionInterface):
    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self._MaxAngle = 20
        self._MinAngle = 6
        self._DefaultMaxAngle = 20
        self._DefaultMinAngle = 6
        self.sleepTime = (0.001)
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[3], self._MInterface._Legs[4]]
        self.group2 = [self._MInterface._Legs[1], self._MInterface._Legs[2], self._MInterface._Legs[5]]
        self.allLegs = [self._MInterface._Legs[0], self._MInterface._Legs[1], self._MInterface._Legs[2],
                        self._MInterface._Legs[3], self._MInterface._Legs[4], self._MInterface._Legs[5]]
            
    def exit(self):
        pass #exit methode

    #Calling dance methods
    def dance(self):
        for x in range (0, 6):
            self.doMoveForwards()
        for x in range (0, 6):
            self.doMoveBackwards()

        for x in range (0, 6):
            self.doMoveRotateLeft()
            time.sleep(self.sleepTime)
            self.doMoveRotateLeft()
            time.sleep(self.sleepTime)
        
        for x in range(0, 3):
            doMoveStamp(1)
            doMoveStamp(2)
            time.sleep(self.sleepTime)
            
        #doMoveWaveLeg()
        time.sleep(self.sleepTime)
        
        for x in range(0, 3):
            self.doMoveRaiseSingle(True)
            self.doMoveRaiseSingle(False)
            time.sleep(self.sleepTime)
            
        #self.doMoveWaveLeg()
        #self.doMoveWave()
        self.fourLegs()

        for x in range (0, 6):
            self.doMoveForwards()
        for x in range (0, 6):
            self.doMoveBackwards()

        self.doMoveUpDown(self)

    #Walk a step forward
    def doMoveForwards():
        self._MInterface.raiseLegs(self.group1)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (self.group1, True, [0, self._DefaultMaxAngle]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (self.group2, False, [self._DefaultMaxAngle, 0]))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self._MInterface.LowerLegs(self.group1)
        self._MInterface.raiseLegs(self.group2)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (self.group2, True,[0, self._DefaultMaxAngle]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (self.group1, False, [self._DefaultMaxAngle, 0]))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self._MInterface.LowerLegs(self.group2)

        self._MInterface.raiseLegs(self.group1)
        self._MInterface.MoveLegsBackward(self.group2, False, [self._DefaultMaxAngle, 0])
        self._MInterface.LowerLegs(self.group1)

    #Walk a step backwards
    def doMoveBackwards():
        self._MInterface.raiseLegs(self.group1)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (self.group1, True, [0, -self._MaxAngle],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (self.group2, False, [-self._MaxAngle, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self._MInterface.LowerLegs(self.group1)
        self._MInterface.raiseLegs(self.group2)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (self.group2, True, [0, -self._MaxAngle],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (self.group1, False, [-self._MaxAngle, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self._MInterface.LowerLegs(self.group2)

        self._MInterface.raiseLegs(self.group1)
        self._MInterface.MoveLegsForward(self.group2, False, [-self._MaxAngle, 0])
        self._MInterface.LowerLegs(self.group1)
        
    #Do a wave with all 6 legs. First lower the 1st two than 2nd two etc.
    def doMoveWave(self):
        pass
        
    #Wave with 1 leg
    def doMoveWaveLeg(self):
        pass

    #Only move the hips
    def doMoveHip(self):
        steps = 30
        pulses = self._MInterface.calculateHipPulse(self._Height, self._Length)
        startPulseHip = Legs[0].getHip()
        for step in range(1, steps, 1 * self._MInterface._Multiplier):
            for x in range(0, 6):
                self._MInterface.Legs[x].moveHip(self._MInterface.calculateVerticalPulse(startPulseHip, pulses[1] , step, steps))
            time.sleep(self.sleepTime)
                

    #The whole spin moves up and down
    def doMoveUpDown(self):
        self.setHeight(50)
        time.sleep(sleepTime)
        self.setHeight(180)
        time.sleep(sleepTime)
        self.setHeight(75)
        
        
    #Spider stands on 4 legs and moves the middle 2
    def fourLegs(self):
        group = [self._MInterface._Legs[2], self._MInterface._Legs[3]]
        self._MInterface.raiseLegs(group)
        #Move the 2 legs
        
                
    #Raise and lower all 6 legs one by one
    def doMoveRaiseSingle(self, Start):        
        if(Start):
            for x in range(0, 6):
                array = [self.allLegs[x]]
                self._MInterface.raiseLegs(array)
                self._MInterface.LowerLegs(array)
        else:
            for x in range(5, -1, -1):
                array = [self.allLegs[x]]
                self._MInterface.raiseLegs(array)
                self._MInterface.LowerLegs(array)
        
    def rotateLegs(self, group1, group2, group1from, group1to, group2from, group2to):
        for i in range(0, 3):
            tempgroup = [group1[i], group2[i]]
            self._MInterface.raiseLegs(tempgroup)
            self._MInterface.MoveLegsForward([tempgroup[0]], True, [group1from, group1to])
            self._MInterface.MoveLegsBackward([tempgroup[1]], True, [group2from, group2to])
            self._MInterface.LowerLegs(tempgroup)

    #Rotate the spider to the left
    def doMoveRotateLeft(self):
        group1 = [self._MInterface._Legs[4], self._MInterface._Legs[2], self._MInterface._Legs[0]]
        group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]        
        
        self.rotateLegs(group1, group2, 0, self._MaxAngle, 0, -self._MaxAngle)
            
        #move legs backward
        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, -self._MaxAngle],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, self._MaxAngle],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        #tilt legs and move them back to start position for rotation, stop command mov  es them back to default position if next command != rotate
        self.rotateLegs(group1, group2, -self._MaxAngle, self._MaxAngle, self._MaxAngle, -self._MaxAngle)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, 0],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

    #Rotate spider to the right
    def doMoveRotateRight(self):
        group2 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
        group1 = [self._MInterface._Legs[5], self._MInterface._Legs[3], self._MInterface._Legs[1]]        
        
        self.rotateLegs(group1, group2, 0, self._MaxAngle, 0, -self._MaxAngle)
       
        #move legs backward
        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, -self._MaxAngle],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, self._MaxAngle],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        #tilt legs and move them back to start position for rotation, stop command moves them back to default position if next command != rotate
        self.rotateLegs(group1, group2, -self._MaxAngle, self._MaxAngle, self._MaxAngle, -self._MaxAngle)

        leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, 0],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

    #Raise leg 1, 4, 6 and lower. After that same thing with 2, 3, 5
    def doMoveStamp(self, group):
        if(group == 1):
            self._MInterface.raiseLegs(self.group2)
            self._MInterface.LowerLegs(self.group2)
        else:
            self._MInterface.LowerLegs(self.group1)
            self._MInterface.raiseLegs(self.group1)
