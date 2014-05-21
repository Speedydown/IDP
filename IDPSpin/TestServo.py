__author__ = 'Ivar'

from Leg import Leg

Leg1 = Leg(["0x40", "0x40", "0x40"], [0, 1, 2], [375, 375, 375])

while (True):
  # Change speed of continuous servo on channel O
  angle = int(raw_input("Angle 150 to 600: "))
  Leg1.moveHip(angle)
