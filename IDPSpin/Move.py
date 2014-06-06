from MotionInterface import MotionInterface
from MovementAction import MovementAction
import time
import threading
from threading import Thread

class Move(MotionInterface):

    def __init__(self):
        self._MInterface = MotionInterface()
        self._Stop = False
        self.SleepTime = 0.005


    def runThread(self):

        self._MInterface.getExitSemaphore().acquire()
        while self._MInterface.isExited() == False:
            self.executeCommand(self._MInterface.get_CurrentCommand())
            self._MInterface.getExitSemaphore().release()
            time.sleep(0.001)

    def executeCommand(self, Command):
        Command = int(Command)

        if Command == 10:
            pass
        elif Command == 11:
            leg1Thread = threading.Thread(target=self.MoveLegForward, args = (self._MInterface._Legs[0], [
                MovementAction(375, 312),
                MovementAction(374, 329),
                MovementAction(200, 472),
                MovementAction(312, 375),
                MovementAction(329, 375),
                MovementAction(472, 200)],))
            leg1Thread.start()

            leg1Thread.join()

    def get_CurrentCommand(self):
        return self._MInterface.get_CurrentCommand()

    def set_CurrentCommand(self, _CurrentCommand):
        return self._MInterface.set_CurrentCommand(_CurrentCommand)

    def exit(self):
        self._MInterface.exit()


    def MoveLegForward(self, Leg, MovementActions):
        #down
        for step in range(1, 50):
            Leg.moveAnkle(self.calculatePulse(MovementActions[0].getStartPulse(), MovementActions[0].getEndPulse(), step, 50))
            Leg.moveKnee(self.calculatePulse(MovementActions[1].getStartPulse(), MovementActions[1].getEndPulse(), step, 50))
            time.sleep(self.SleepTime)

        #sideways
        for step in range(1, 161):
            Leg.moveHip(self.calculatePulse(MovementActions[2].getStartPulse(), MovementActions[2].getEndPulse(), step, 160))
            time.sleep(self.SleepTime)

        #up
        for step in range(1, 50):
            Leg.moveAnkle(self.calculatePulse(MovementActions[3].getStartPulse(), MovementActions[3].getEndPulse(), step, 50))
            Leg.moveKnee(self.calculatePulse(MovementActions[4].getStartPulse(), MovementActions[4].getEndPulse(), step, 50))
            time.sleep(self.SleepTime)

        #sideways
        for step in range(1, 161):
            Leg.moveHip(self.calculatePulse(MovementActions[5].getStartPulse(), MovementActions[5].getEndPulse(), step, 160))
            time.sleep(self.SleepTime)

    #Inverse Kinematics
    def calculatePulse(self, StartingPulse, EndPulse, Step, numberOfSteps=160):
        if Step > numberOfSteps or Step < 1:
            print "Step out of range - " + str(Step)
            #raise Exception("Step out of range - " + str(Step))

        pulsedifference = 150
        if EndPulse < StartingPulse:
            pulsedifference = StartingPulse - EndPulse
            pulse = StartingPulse - int((float(pulsedifference) / float(numberOfSteps)) * Step)
            print pulse
            return pulse
        else:
            pulsedifference = EndPulse - StartingPulse
            pulse =  StartingPulse + int((float(pulsedifference) / float(numberOfSteps)) * Step)
            print pulse
            return pulse

    def calculateEndPulse(self, hoogte, lengte):

        a = 80
        b = 127 #afstand servo naar einde poot
        c = 125
        d = 106 #lengte poot
        e = 70  #hoogte poot









