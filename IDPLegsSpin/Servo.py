__author__ = 'Ivar'

from Adafruit_PWM_Servo_Driver import PWM

class Servo(object):

    def __init__(self, channel, address, maxAngle=40.0, minAngle=40.0, freq=60):

        self.channel = channel
        self.address = address
        self.freq = freq
        self.maxAngle = maxAngle
        self.minAngle = minAngle
        self.maxmillisec = 2.0
        self.minmillisec = 1.0
        self.m = (self.minmillisec - self.maxmillisec)/(self.maxAngle - self.minAngle)
        self.b = self.maxmillisec - (self.m * self.minAngle)
        self.pwm = PWM()
        self.pwm.setPWMFreq(self.freq)
        self.cycle = 1.0/float(self.freq)
        self.timepertick = self.cycle / 4096

    def setAngle(self, angle):
        self.angle = angle
        print self.angle

        if self.angle > self.maxAngle:
            self.angle = self.maxAngle
        elif self.angle < self.minAngle:
            self.angle = self.minAngle
        self.millisec = self.angle * self.m + self.b
        print self.millisec

        if self.millisec > self.maxmillisec:
            self.millisec = self.maxmillisec
        elif self.millisec < self.minmillisec:
            self.millisec = self.minmillisec
        self.tickOn = (self.millisec/1000.0)/self.timepertick
        print self.tickOn
        self.pwm.setPWM(self.channel, 0, int(self.tickOn))

    def getAngle(self):
        return self.angle