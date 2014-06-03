__author__ = 'Ivar'

from Adafruit_PWM_Servo_Driver import PWM

class Servo(object):
    """
    Setting the channels, address, startingPulse and frequency to create an servo.
    Using the Adafruit PWM servo driver to set the min and max Pulse of the servo.
    """
    def __init__(self, address, channel, startingPulse, minPulse=150, maxPulse=600, freq=60):
    # Constructor
        self.pulse = 0
        self.channel = channel
        self.address = address
        self.freq = freq
        self.maxPulse = maxPulse
        self.minPulse = minPulse
        self.pwm = PWM()
        self.pwm.setPWMFreq(self.freq)
        self.setPulse(startingPulse)

    def setPulse(self, pulse):
        # Setting the area of pulses between 150 and 600. If the input is bigger then 600 pulses
        # it will be set to the max 600 pulses. If pulses are lower then 150 it will be set tot 150 pulses

        if pulse > self.maxPulse:
            pulse = self.maxPulse
        elif pulse < self.minPulse:
            pulse = self.minPulse

        self.pwm.setPWM(self.channel, 0, pulse) # 0 means: zero pulse away from input pulse.
        self.pulse = pulse                      # setting the input pulse

    def getPulse(self):
        return self.pulse
