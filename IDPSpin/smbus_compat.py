"""
Minimal pure-Python replacement for the `smbus` module.

Used as a fallback when python3-smbus is not installed, so the spider can
still drive its PCA9685 servo boards and MPU6050 gyro over /dev/i2c-N
without any extra packages.
"""
import fcntl
import os
import threading

I2C_SLAVE = 0x0703
I2C_SLAVE_FORCE = 0x0706


class SMBus(object):

    def __init__(self, bus=1):
        self._fd = os.open("/dev/i2c-%d" % bus, os.O_RDWR)
        self._addr = None
        self._lock = threading.Lock()

    def _select(self, addr):
        if self._addr != addr:
            fcntl.ioctl(self._fd, I2C_SLAVE_FORCE, addr)
            self._addr = addr

    def _write(self, addr, data):
        with self._lock:
            self._select(addr)
            os.write(self._fd, bytes(bytearray(data)))

    def _write_read(self, addr, data, length):
        with self._lock:
            self._select(addr)
            os.write(self._fd, bytes(bytearray(data)))
            return list(bytearray(os.read(self._fd, length)))

    def write_byte(self, addr, value):
        self._write(addr, [value & 0xFF])

    def read_byte(self, addr):
        with self._lock:
            self._select(addr)
            return bytearray(os.read(self._fd, 1))[0]

    def write_byte_data(self, addr, reg, value):
        self._write(addr, [reg & 0xFF, value & 0xFF])

    def read_byte_data(self, addr, reg):
        return self._write_read(addr, [reg & 0xFF], 1)[0]

    def write_word_data(self, addr, reg, value):
        self._write(addr, [reg & 0xFF, value & 0xFF, (value >> 8) & 0xFF])

    def read_word_data(self, addr, reg):
        lo, hi = self._write_read(addr, [reg & 0xFF], 2)
        return lo | (hi << 8)

    def write_i2c_block_data(self, addr, reg, data):
        self._write(addr, [reg & 0xFF] + [d & 0xFF for d in data])

    def read_i2c_block_data(self, addr, reg, length=32):
        return self._write_read(addr, [reg & 0xFF], length)

    def close(self):
        os.close(self._fd)
