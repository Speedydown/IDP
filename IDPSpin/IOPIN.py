__author__ = 'Speedy'

import time
import threading

# RPi.GPIO first; on current Raspberry Pi OS that is the rpi-lgpio shim, which
# refuses old-style board revisions (Pi 1 Model B). Fall back to lgpio directly.
GPIO = None
lgpio = None
try:
    import RPi.GPIO as GPIO
    GPIO.setmode(GPIO.BCM)
except Exception:
    GPIO = None
    try:
        import lgpio
    except Exception:
        print("could not open iopins")

HORN_PINS = (30, 31)


class IOPIN(object):

    def __init__(self):
        self._chip = None
        try:
            if GPIO is not None:
                for pin in HORN_PINS:
                    GPIO.setup(pin, GPIO.OUT)
                    GPIO.output(pin, False)
            elif lgpio is not None:
                self._chip = lgpio.gpiochip_open(0)
                for pin in HORN_PINS:
                    lgpio.gpio_claim_output(self._chip, pin, 0)
            else:
                print("IO pins not available")
        except Exception as e:
            print("IO pins failed! %s" % e)

    def _set(self, value):
        for pin in HORN_PINS:
            if GPIO is not None:
                GPIO.output(pin, value)
            elif self._chip is not None:
                lgpio.gpio_write(self._chip, pin, 1 if value else 0)

    def Horn(self):
        HornThread = threading.Thread(target=self.hornThread)
        HornThread.start()

    def hornThread(self):
        try:
            self._set(True)
            time.sleep(2.5)
            self._set(False)
            time.sleep(0.5)
            self._set(True)
            time.sleep(2.5)
            self._set(False)
        except Exception as e:
            print("horn failed: %s" % e)
