__author__ = 'Speedy'
try:
    import RPi.GPIO as GPIO
except:
    print "could not open iopins"

class IOPIN(object):

    def __init__(self):
        try:
            GPIO.setmode(GPIO.BCM)
            GPIO.setup(30, GPIO.OUT)
            GPIO.output(30, True)
            GPIO.setup(31, GPIO.OUT)
            GPIO.output(31, True)
        except:
            pass