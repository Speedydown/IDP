__author__ = 'Ivar'

from Adafruit_PWM_Servo_Driver import PWM

class Servo(object):

    def __init__(self, address, channel, startingPulse, minPulse=150, maxPulse=600, freq=60):

        self.pulse = 0
        self.channel = channel              # channels of the adafruit servo driver (0 to 16) used 2times
        self.address = address              # 2 addresses of the adafruit (0x40,0x41)
        self.freq = freq                    # standard frequenty for the adafruit (60Hz)
        self.maxPulse = maxPulse            # setting the maximum pulse of the servo
        self.minPulse = minPulse            # setting the mininum pulse of the servo
        self.pwm = PWM()
        self.pwm.setPWMFreq(self.freq)
        self.setPulse(startingPulse)

    def setPulse(self, pulse):
        if pulse > self.maxPulse:
            pulse = self.maxPulse
        elif pulse < self.minPulse:
            pulse = self.minPulse

        self.pwm.setPWM(self.channel, 0, pulse)
        self.pulse = pulse

    def getPulse(self):
        return self.pulse
