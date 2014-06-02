__author__ = 'Ivar'

from Adafruit_PWM_Servo_Driver import PWM

class Servo(object):
    """
    Setting the channels, address, startingPulse and frequency. Using the Adafruit PWM servo driver to
    set the min and max Pulse of the servo for maximum degrees possible.
    """
    def __init__(self, address, channel, startingPulse, minPulse=150, maxPulse=600, freq=60):

        self.pulse = 0                      # set pulse on 0
        self.channel = channel              # channels of the adafruit servo driver (0 to 16) used 2times
        self.address = address              # 2 addresses of the adafruit (0x40,0x41)
        self.freq = freq                    # standard frequency for the adafruit (60Hz)
        self.maxPulse = maxPulse            # setting the maximum pulse of the servo
        self.minPulse = minPulse            # setting the minimum pulse of the servo
        self.pwm = PWM()
        self.pwm.setPWMFreq(self.freq)
        self.setPulse(startingPulse)

    def setPulse(self, pulse):
        # If the input pulse is bigger then maxPulse, then set to maxPulse,
        # for input smaller then minPulse, then set to minPulse.
        if pulse > self.maxPulse:
            pulse = self.maxPulse
        elif pulse < self.minPulse:
            pulse = self.minPulse

        self.pwm.setPWM(self.channel, 0, pulse) # 0 means: zero pulse away from input pulse.
        self.pulse = pulse

    def getPulse(self):
        return self.pulse
