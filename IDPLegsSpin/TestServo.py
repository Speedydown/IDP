__author__ = 'Ivar'

from Servo import servo
import time

servo = servo(1,0x40)
servo.setAngle(40)
time.sleep(1)
servo.setAngle(-40)