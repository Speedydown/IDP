__author__ = 'Matthe Jacobs'
#Class that gets the finger control pulses and controls a leg with it
import threading

try:
    import serial
except:
    "serial not initialised"

class FingerControl(object):

    def __init__(self, MotionInterface):
        self._MotionInterface = MotionInterface
        self._MotionInterfaceThread = threading.Thread(target=self.run)
        self._MotionInterfaceThread.start()

    def executeCommand(self, Command):
        pass

    def run(self):

        self._DefaultSpeed = self._MotionInterface.getSpeed()
        self._MotionInterface.setSpeed(0.06)
        self.ser = serial.Serial('/dev/ttyUSB0', 9600)
        self._ForwardLegs = [self._MotionInterface._Legs[4], self._MotionInterface._Legs[5]]
        self._middleLegs = [self._MotionInterface._Legs[2], self._MotionInterface._Legs[3]]

        self._MotionInterface.raiseLegs(self._middleLegs)
        self._MotionInterface.MoveLegsForward(self._middleLegs, True, [0, 20])
        self._MotionInterface.LowerLegs(self._middleLegs)

        self._MotionInterface.raiseLegs(self._ForwardLegs)
        self._MotionInterface.MoveLegsForward(self._ForwardLegs, True, [0, 90])

        for Leg in self._ForwardLegs:
            Leg.moveAnkle(175)
            Leg.moveKnee(575)

        while(True):
            #Read incoming data
            incoming = self.ser.readline()
            try:
                if incoming[:2] == 'a1':
                    #Move the leg
                    pulse = int(incoming.strip('a1'))
                    if pulse > 450:
                        pulse = 450
                    self._MotionInterface._Legs[4].moveAnkle(pulse)
            except ValueError:
                pass
            try:
                if incoming[:2] == 'a2':
                    #Move the leg
                    pulse = int(incoming.strip('a2'))
                    if pulse > 450:
                        pulse = 450
                    self._MotionInterface._Legs[4].moveKnee(pulse)
            except ValueError:
                pass
            try:
                if incoming[:2] == 'b1':
                    #Move the leg
                    pulse = int(incoming.strip('b1'))
                    if pulse > 450:
                        pulse = 450
                    self._MotionInterface._Legs[5].moveAnkle(pulse)
            except ValueError:
                pass
            try:
                if incoming[:2] == 'b2':
                    #Move the leg
                    pulse = int(incoming.strip('b2'))
                    if pulse > 450:
                        pulse = 450
                    self._MotionInterface._Legs[5].moveKnee(pulse)
            except ValueError:
                pass

    def exit(self):
        print("ik ben hier")

        self._MotionInterface.raiseLegs(self._ForwardLegs)
        self._MotionInterface.MoveLegsBackward(self._ForwardLegs, True, [self._MotionInterface.convertPulseToDegrees((self._ForwardLegs[0].getHip() - 375)), 0])
        self._MotionInterface.LowerLegs(self._ForwardLegs)

        self._MotionInterface.raiseLegs(self._middleLegs)
        self._MotionInterface.MoveLegsBackward(self._middleLegs, True, [20, 0])
        self._MotionInterface.LowerLegs(self._middleLegs)

        self._MotionInterface.setSpeed(self._DefaultSpeed)
            
