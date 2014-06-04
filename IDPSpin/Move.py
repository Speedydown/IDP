from MotionInterface import MotionInterface
import time
class Move(MotionInterface):

    def __init__(self):
        self._MInterface = MotionInterface()
        self._Stop = False

    def moveForward(self):
        self._MInterface._Legs[0].moveAnkle(312)
        self._MInterface._Legs[0].moveKnee(329)
        time.sleep(1)
        self._MInterface._Legs[0].moveHip(278)
        time.sleep(1)
        self._MInterface._Legs[0].moveAnkle(375)
        self._MInterface._Legs[0].moveKnee(375)
        time.sleep(1)
        self._MInterface._Legs[0].moveHip(375)
        time.sleep(1)

    def run(self):

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
            self.moveForward()

    def get_CurrentCommand(self):
        return self._MInterface.get_CurrentCommand()

    def set_CurrentCommand(self, _CurrentCommand):
        return self._MInterface.set_CurrentCommand(_CurrentCommand)

    def exit(self):
        self._MInterface.exit()
