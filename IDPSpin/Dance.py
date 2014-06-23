__author__ = 'Matthe Jacobs'

import time
import threading
import math
from threading import Thread


class Dance(object):
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

    def executeCommand(self, Command):

        Command = int(Command)

        if Command == 30:
            self.dance()
            self._MInterface.set_CurrentCommand(10)

    #Calling dance methods
    def dance(self):
        for x in range (0, 3):
            self.doMoveForwards()
        self.startPos(1)
        for x in range (0, 3):
            self.doMoveBackwards()
        self.startPos(2)

        for x in range (0, 3):
            self.doMoveRotateLeft()
            time.sleep(self.sleepTime)
        self.startPos(3)

        for x in range (0, 3):
            self.doMoveRotateRight()
            time.sleep(self.sleepTime)
        self.startPos(4)        
        
        doMoveStamp(1)
        time.sleep(self.sleepTime)
        doMoveStamp(2)            
            
        self.doMoveWaveLeg()
        time.sleep(self.sleepTime)
        
        self.doMoveRaiseSingle(True)
        time.sleep(self.sleepTime)
        
        self.doMoveRaiseSingle(False)
        time.sleep(self.sleepTime)
            
        self.doMoveWaveLeg()
        
        #self.doMoveWave()
        
        self.doMoveFourLegs()

        for x in range (0, 3):
            self.doMoveForwards()
        self.startPos(1)
        for x in range (0, 3):
            self.doMoveBackwards()
        self.startPos(2)

        self.doMoveHip()

        self.doMoveUpDown()

        self.doMoveWaveLegTwo()

    #Sets the spin to his starting position
    def startPos(self, resetMove):
        if(resetMove == 1):
            self._MInterface.raiseLegs(self.group1)
            self._MInterface.MoveLegsBackward(self.group2, False, [self._DefaultMaxAngle, 0])
            self._MInterface.LowerLegs(self.group1)
        elif(resetMove == 2):
            self._MInterface.raiseLegs(self.group1)
            self._MInterface.MoveLegsForward(self.group2, False, [-self._MaxAngle, 0])
            self._MInterface.LowerLegs(self.group1)
        elif(resetMove == 3):
            group2 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
            group1 = [self._MInterface._Legs[5], self._MInterface._Legs[3], self._MInterface._Legs[1]]

            leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, 0],))
            leg1Thread.start()
            leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, 0],))
            leg2Thread.start()

            leg1Thread.join()
            leg2Thread.join()
        elif(resetMove == 4):
            group1 = [self._MInterface._Legs[4], self._MInterface._Legs[2], self._MInterface._Legs[0]]
            group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]

            leg1Thread = threading.Thread(target=self._MInterface.MoveLegsBackward, args = (group1, False, [self._MaxAngle, 0],))
            leg1Thread.start()
            leg2Thread = threading.Thread(target=self._MInterface.MoveLegsForward, args = (group2, False, [-self._MaxAngle, 0],))
            leg2Thread.start()

            leg1Thread.join()
            leg2Thread.join()                

    #Walk a step forward
    def doMoveForwards(self):
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

    #Walk a step backwards
    def doMoveBackwards(self):
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
        
        
    #Do a wave with all 6 legs. First lower the 1st two than 2nd two etc.
    def doMoveWave(self):
        pass
        
    #Wave with 2 legs
    def doMoveWaveLeg(self):
        self._MotionInterface._Legs[5].moveAnkle(175)
        self._MotionInterface._Legs[5].moveKnee(575)

        self._MotionInterface._Legs[5].moveAnkle(190)
        self._MotionInterface._Legs[5].moveAnkle(150)
        self._MotionInterface._Legs[5].moveAnkle(175)
        self._MotionInterface._Legs[5].moveAnkle(375)
        self._MotionInterface._Legs[5].moveAnkle(375)

    #Raises the 2 front legs and waves with them.
    def doMoveWaveLegTwo(self):
        group = [self._MInterface._Legs[4], self._MInterface._Legs[5]]
        self._DefaultSpeed = self._MotionInterface.getSpeed()
        self._MotionInterface.setSpeed(0.06)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self._ForwardLegs = [self._MotionInterface._Legs[4], self._MotionInterface._Legs[5]]
        self._middleLegs = [self._MotionInterface._Legs[2], self._MotionInterface._Legs[3]]

        self._MotionInterface.raiseLegs(self._middleLegs)
        self._MotionInterface.MoveLegsForward(self._middleLegs, True, [0, 20])
        self._MotionInterface.LowerLegs(self._middleLegs)

        self._MotionInterface.raiseLegs(self._ForwardLegs)
        self._MotionInterface.MoveLegsForward(self._ForwardLegs, True, [0, 80])

        for Leg in self._ForwardLegs:
            Leg.moveAnkle(175)
            Leg.moveKnee(575)

        #Movement
        self._MotionInterface.raiseLegs(

        #To start position
        self._MotionInterface.raiseLegs(self._ForwardLegs)
        self._MotionInterface.MoveLegsBackward(self._ForwardLegs, True, [self._MotionInterface.convertPulseToDegrees((self._ForwardLegs[0].getHip() - 375)), 0])
        self._MotionInterface.LowerLegs(self._ForwardLegs)

        self._MotionInterface.raiseLegs(self._middleLegs)
        self._MotionInterface.MoveLegsBackward(self._middleLegs, True, [20, 0])
        self._MotionInterface.LowerLegs(self._middleLegs)

        self._MotionInterface.setSpeed(self._DefaultSpeed)

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
        
        
    #Spider stands on 4 legs
    def doMoveFourLegs(self):
        group = [self._MInterface._Legs[2], self._MInterface._Legs[3]]
        self._MInterface.raiseLegs(group)
        time.sleep(2)
        self._MInterface.LowerLegs(group)
                
    #Raise and lower all 6 legs one by one
    def doMoveRaiseSingle(self, Start):        
        if(Start):
            for x in range(0, 6):
                array = [self.allLegs[x]]
                self._MInterface.raiseLegs(array)
                self._MInterface.LowerLegs(array)
                time.sleep(0,2)
        else:
            for x in range(5, -1, -1):
                array = [self.allLegs[x]]
                self._MInterface.raiseLegs(array)
                self._MInterface.LowerLegs(array)
                time.sleep(0,2)
        
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


    #Raise leg 1, 4, 6 and lower. After that same thing with 2, 3, 5
    def doMoveStamp(self, group):
        if(group == 1):
            self._MInterface.raiseLegs(self.group2)
            self._MInterface.LowerLegs(self.group2)
        else:
            self._MInterface.raiseLegs(self.group1)
            self._MInterface.LowerLegs(self.group1)
