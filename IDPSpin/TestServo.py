__author__ = 'Ivar'

from Servo import Servo

from Adafruit_PWM_Servo_Driver import PWM
import time

pwm = PWM (0x40, debug=True)
#servo = Servo(0x40, 0)
#servo.setAngle(-40)
#time.sleep(1)
#servo.setAngle(40)

servoMin = 150  # Min pulse length out of 4096
servoMax = 600  # Max pulse length out of 4096

def setServoPulse(channel, pulse):
  pulseLength = 1000000                   # 1,000,000 us per second
  pulseLength /= 60                       # 60 Hz
  print "%d us per period" % pulseLength
  pulseLength /= 4096                     # 12 bits of resolution
  print "%d us per bit" % pulseLength
  pulse *= 1000
  pulse /= pulseLength
  pwm.setPWM(channel, 0, pulse)

pwm.setPWMFreq(60)                        # Set frequency to 60 Hz
angle = 0

def servoSet(a):
    global angle
    if angle > servoMax:
        angle = servoMax
    elif angle < servoMin:
        angle= servoMin

    pwm.setPWM(0, 0, angle)
    return angle

while (True):
  # Change speed of continuous servo on channel O
  angle = int(raw_input("Angle 150 to 600: "))

  pwm.setPWM(0, 0, servoSet(angle))
