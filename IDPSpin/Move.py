import time
import threading
import math
from threading import Thread

class Move(object):

    def __init__(self, _MInterface):
        self._MInterface = _MInterface
        self._LastCommand = 9
        self.group1 = [self._MInterface._Legs[0], self._MInterface._Legs[3], self._MInterface._Legs[4]]
        self.group2 = [self._MInterface._Legs[1], self._MInterface._Legs[2], self._MInterface._Legs[5]]

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 9:
            self._LastCommand = 9;
            self._MInterface.set_CurrentCommand(10)
            self.StopLegs()
            self._LastCommand = 10;
        elif Command == 10:
            self.StopLegs()
            self._LastCommand = 10;
        elif Command == 11:
            self.MoveForward()
            self._LastCommand = 11
        elif Command == 12:
            self.MoveForwardAndRotate(True)
            self._LastCommand = 12
        elif Command == 13:
            self.Rotate(False)
            self._LastCommand = 13
        elif Command == 14:
            self.MoveBackwardAndRotate(True)
            self._LastCommand = 14
        elif Command == 15:
            self.MoveBackward()
            self._LastCommand = 15
        elif Command == 16:
            self.MoveBackwardAndRotate(False)
            self._LastCommand = 16
        elif Command == 17:
            self.Rotate(True)
            self._LastCommand = 17
        elif Command == 18:
            self.MoveForwardAndRotate(False)
            self._LastCommand = 18

    def exit(self):
        pass #exit methode

    def raiseLegs(self, Legs):
        steps = 30
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        startpulseAnkle = Legs[0].getAnkle()
        startpulseKnee = Legs[0].getKnee()
        for step in range(1, steps):
            #raise leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[1] - 95, step, steps)) #was 312
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[0] - 95, step, steps)) #was 329
            time.sleep(self._MInterface.SleepTime)

    def LowerLegs(self, Legs):
        steps = 30
        startpulseAnkle = Legs[0].getAnkle() #klopt die array? twee keer 0 voor ankle en knee.
        startpulseKnee = Legs[0].getKnee()
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)

        for step in range(1, steps):
           #lower leg
            for Leg in Legs:
                Leg.moveAnkle(self._MInterface.calculateVerticalPulse(startpulseAnkle, pulses[1], step, steps))
                Leg.moveKnee(self._MInterface.calculateVerticalPulse(startpulseKnee, pulses[0], step, steps)) #startpulseKnee in plaats van Ankle
            time.sleep(self._MInterface.SleepTime)

    def MoveLegsForward(self, Legs, Raised=False, Turn=[0, 20]):
        startpoint = Turn[0]
        steps = Turn[1]
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        if Raised:
            pulses[0] -= 90
            pulses[1] -= 90
        for step in range(startpoint, steps):
            #move leg forward
            #pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface.calculateLengthLeg(self._MInterface._Length, step))

            #if Raised:
                #pulses[0] -= 90
                #pulses[1] -= 90

            for Leg in Legs:
                Leg.moveHip(self._MInterface.calculateHipPulse(step))
                #Leg.moveKnee(pulses[0])
                #Leg.moveAnkle(pulses[1])
            time.sleep(self._MInterface.SleepTime)


    def MoveLegsBackward(self, Legs, Raised=False, Turn=[20, 0]):
        startpoint = Turn[0]
        steps = Turn[1]
        pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
        if Raised:
            pulses[0] -= 90
            pulses[1] -= 90
        for step in range(startpoint, steps, -1):
            #pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface.calculateLengthLeg(self._MInterface._Length, step))

            #if Raised:
                #pulses[0] -= 90
                #pulses[1] -= 90

            #pulses = self._MInterface.calculatePulse(self._MInterface._Height, self._MInterface._Length)
            for Leg in Legs:
                Leg.moveHip(self._MInterface.calculateHipPulse(step))
                #Leg.moveKnee(pulses[0])
                #Leg.moveAnkle(pulses[1])

            time.sleep(self._MInterface.SleepTime)

    def rotateLegs(self, group1, group2, group1from, group1to, group2from, group2to):
        tempgroup = [group1[0], group2[0]]
        self.raiseLegs(tempgroup)
        self.MoveLegsForward([tempgroup[0]], True, [group1from, group1to])
        self.MoveLegsBackward([tempgroup[1]], True, [group2from, group2to])
        self.LowerLegs(tempgroup)

        tempgroup = [group1[1], group2[1]]
        self.raiseLegs(tempgroup)
        self.MoveLegsForward([tempgroup[0]], True, [group1from, group1to])
        self.MoveLegsBackward([tempgroup[1]], True, [group2from, group2to])
        self.LowerLegs(tempgroup)

        tempgroup = [group1[2], group2[2]]
        self.raiseLegs(tempgroup)
        self.MoveLegsForward([tempgroup[0]], True, [group1from, group1to])
        self.MoveLegsBackward([tempgroup[1]], True, [group2from, group2to])
        self.LowerLegs(tempgroup)


    def Rotate(self, Left=False):
        #make groups based on rotation direction
        if (Left):
            group1 = [self._MInterface._Legs[4], self._MInterface._Legs[2], self._MInterface._Legs[0]]
            group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]
        else:
            group2 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
            group1 = [self._MInterface._Legs[5], self._MInterface._Legs[3], self._MInterface._Legs[1]]

        #check if last command was also left or right, and move to start position if direction does not match
        if not(self._LastCommand == 13 or self._LastCommand == 17):
            self.StopLegs()
            self.rotateLegs(group1, group2, 0, 20, 0, -20)
        else:
            if (self._LastCommand == 13 and Left == True) or (self._LastCommand == 17 and Left == False):
                self.StopLegs()
                self.rotateLegs(group1, group2, 0, 20, 0, -20)


        #move legs backward
        leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (group1, False, [20, -20],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (group2, False, [-20, 20],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        #tilt legs and move them back to start position for rotation, stop command moves them back to default position if next command != rotate
        self.rotateLegs(group1, group2, -20, 20, 20, -20)

    def MoveForwardAndRotate(self, Right = False):

        if Right == True:
            group1 = self.group1
            group2 = self.group2
            forwardleftsidegroup1 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardrightsidegroup1 = [self._MInterface._Legs[3]]
            forwardrightsidegroup2 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardleftsidegroup2 = [self._MInterface._Legs[2]]
        else:
            group2 = self.group1
            group1 = self.group2
            forwardrightsidegroup2 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardleftsidegroup2 = [self._MInterface._Legs[3]]
            forwardleftsidegroup1 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardrightsidegroup1 = [self._MInterface._Legs[2]]

        if not(self._LastCommand == 12 or self._LastCommand == 18):
            self.StopLegs()
            self.raiseLegs(group2)
            self.MoveLegsForward(forwardrightsidegroup2, True, [0, 20])
            self.MoveLegsForward(forwardleftsidegroup2, True, [0, 6])
            self.LowerLegs(group2)
        else:
            if (self._LastCommand == 12 and Right == False) or (self._LastCommand == 18 and Right == True):
                self.StopLegs()
                self.raiseLegs(group2)
                self.MoveLegsForward(forwardrightsidegroup2, True, [0, 20])
                self.MoveLegsForward(forwardleftsidegroup2, True, [0, 6])
                self.LowerLegs(group2)

        self.raiseLegs(group1)

        leg1Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardleftsidegroup1, True, [0, 6]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardrightsidegroup1, True, [0, 20]))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardrightsidegroup2, False, [20, 0]))
        leg3Thread.start()
        leg4Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardleftsidegroup2, False, [6, 0]))
        leg4Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()
        leg4Thread.join()

        self.LowerLegs(group1)
        self.raiseLegs(group2)

        leg1Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardleftsidegroup2, True, [0, 6]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardrightsidegroup2, True, [0, 20]))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardrightsidegroup1, False, [20, 0]))
        leg3Thread.start()
        leg4Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardleftsidegroup1, False, [6, 0]))
        leg4Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()
        leg4Thread.join()
        self.LowerLegs(group2)

    def MoveBackwardAndRotate(self, Right = False):

        if Right == True:
            group1 = self.group1
            group2 = self.group2
            forwardleftsidegroup1 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardrightsidegroup1 = [self._MInterface._Legs[3]]
            forwardrightsidegroup2 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardleftsidegroup2 = [self._MInterface._Legs[2]]
        else:
            group2 = self.group1
            group1 = self.group2
            forwardrightsidegroup2 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardleftsidegroup2 = [self._MInterface._Legs[3]]
            forwardleftsidegroup1 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardrightsidegroup1 = [self._MInterface._Legs[2]]

        if not(self._LastCommand == 14 or self._LastCommand == 16):
            self.StopLegs()
            self.raiseLegs(group2)
            self.MoveLegsBackward(forwardrightsidegroup2, True, [0, -20])
            self.MoveLegsBackward(forwardleftsidegroup2, True, [0, -6])
            self.LowerLegs(group2)
        else:
            if (self._LastCommand == 14 and Right == False) or (self._LastCommand == 16 and Right == True):
                self.StopLegs()
                self.raiseLegs(group2)
                self.MoveLegsBackward(forwardrightsidegroup2, True, [0, -20])
                self.MoveLegsBackward(forwardleftsidegroup2, True, [0, -6])
                self.LowerLegs(group2)

        self.raiseLegs(group1)

        leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardleftsidegroup1, True, [0, -6]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardrightsidegroup1, True, [0, -20]))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardrightsidegroup2, False, [-20, 0]))
        leg3Thread.start()
        leg4Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardleftsidegroup2, False, [-6, 0]))
        leg4Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()
        leg4Thread.join()

        self.LowerLegs(group1)
        self.raiseLegs(group2)

        leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardleftsidegroup2, True, [0, -6]))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsBackward, args = (forwardrightsidegroup2, True, [0, -20]))
        leg2Thread.start()
        leg3Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardrightsidegroup1, False, [-20, 0]))
        leg3Thread.start()
        leg4Thread = threading.Thread(target=self.MoveLegsForward, args = (forwardleftsidegroup1, False, [-6, 0]))
        leg4Thread.start()

        leg1Thread.join()
        leg2Thread.join()
        leg3Thread.join()
        leg4Thread.join()
        self.LowerLegs(group2)


    def StopLegs(self):
        #laatste pootbeweging
        if self._LastCommand == 11:
            self.raiseLegs(self.group1)
            self.MoveLegsBackward(self.group2)
            self.LowerLegs(self.group1)
        elif self._LastCommand == 9:
            self.LowerLegs(self._MInterface._Legs)
        elif self._LastCommand == 12:
            forwardrightsidegroup2 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardleftsidegroup2 = [self._MInterface._Legs[2]]

            self.raiseLegs(self.group1)
            self.MoveLegsBackward(forwardrightsidegroup2, False, [20, 0])
            self.MoveLegsBackward(forwardleftsidegroup2, False, [6, 0])
            self.LowerLegs(self.group1)
        elif self._LastCommand == 13:
            group2 = [self._MInterface._Legs[0], self._MInterface._Legs[2], self._MInterface._Legs[4]]
            group1 = [self._MInterface._Legs[5], self._MInterface._Legs[3], self._MInterface._Legs[1]]

            leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (group1, False, [20, 0],))
            leg1Thread.start()
            leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (group2, False, [-20, 0],))
            leg2Thread.start()

            leg1Thread.join()
            leg2Thread.join()

        elif self._LastCommand == 14:
            forwardrightsidegroup2 = [self._MInterface._Legs[1], self._MInterface._Legs[5]]
            forwardleftsidegroup2 = [self._MInterface._Legs[2]]

            self.raiseLegs(self.group1)
            self.MoveLegsForward(forwardrightsidegroup2, False, [-20, 0])
            self.MoveLegsForward(forwardleftsidegroup2, False, [-6, 0])
            self.LowerLegs(self.group1)


        elif self._LastCommand == 15:
            self.raiseLegs(self.group1)
            self.MoveLegsForward(self.group2, False, [-20, 0])
            self.LowerLegs(self.group1)

        elif self._LastCommand == 16:
            forwardrightsidegroup1 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardleftsidegroup1 = [self._MInterface._Legs[3]]

            self.raiseLegs(self.group2)
            self.MoveLegsForward(forwardrightsidegroup1, False, [-20, 0])
            self.MoveLegsForward(forwardleftsidegroup1, False, [-6, 0])
            self.LowerLegs(self.group2)

        elif self._LastCommand == 17:
            group1 = [self._MInterface._Legs[4], self._MInterface._Legs[2], self._MInterface._Legs[0]]
            group2 = [self._MInterface._Legs[1], self._MInterface._Legs[3], self._MInterface._Legs[5]]

            leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (group1, False, [20, 0],))
            leg1Thread.start()
            leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (group2, False, [-20, 0],))
            leg2Thread.start()

            leg1Thread.join()
            leg2Thread.join()
        elif self._LastCommand == 18:
            forwardrightsidegroup1 = [self._MInterface._Legs[0], self._MInterface._Legs[4]]
            forwardleftsidegroup1 = [self._MInterface._Legs[3]]


            self.raiseLegs(self.group2)
            self.MoveLegsBackward(forwardrightsidegroup1, False, [20, 0])
            self.MoveLegsBackward(forwardleftsidegroup1, False, [6, 0])
            self.LowerLegs(self.group2)
        else:
            pass

    def MoveBackward(self):

        #eerste pootbeweging
        if self._LastCommand != 15:
            self.StopLegs()
            self.raiseLegs(self.group2)
            self.MoveLegsBackward(self.group2, True, [0, -20])
            self.LowerLegs(self.group2)

        self.raiseLegs(self.group1)

        leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (self.group1, True, [0, -20],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (self.group2, False, [-20, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self.LowerLegs(self.group1)
        self.raiseLegs(self.group2)

        leg1Thread = threading.Thread(target=self.MoveLegsBackward, args = (self.group2, True, [0, -20],))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsForward, args = (self.group1, False, [-20, 0],))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self.LowerLegs(self.group2)

    def MoveForward(self):

        #eerste pootbeweging
        if self._LastCommand != 11:
            self.StopLegs()
            self.raiseLegs(self.group2)
            self.MoveLegsForward(self.group2, True)
            self.LowerLegs(self.group2)

        self.raiseLegs(self.group1)

        leg1Thread = threading.Thread(target=self.MoveLegsForward, args = (self.group1, True,))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsBackward, args = (self.group2,))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        self.LowerLegs(self.group1)
        self.raiseLegs(self.group2)

        leg1Thread = threading.Thread(target=self.MoveLegsForward, args = (self.group2, True,))
        leg1Thread.start()
        leg2Thread = threading.Thread(target=self.MoveLegsBackward, args = (self.group1,))
        leg2Thread.start()

        leg1Thread.join()
        leg2Thread.join()

        #self.MoveLegsForward(self.group2, True)
        #self.MoveLegsBackward(self.group1)
        self.LowerLegs(self.group2)

