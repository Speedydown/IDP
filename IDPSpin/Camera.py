import time
import picamera
import io

class Camera(object):
    def __init__(self):
        self._Camera = picamera.PiCamera()
        self._Camera.resolution = (640, 480)
        self._Camera.brightness = 50
        self._Camera.start_preview()
    
    def takeImage(self):
        my_stream = io.BytesIO()
        self._Camera.capture(my_stream, 'jpeg')
        return my_stream.getvalue()

    def Exit(self):
        self._Camera.stop_preview()
        
        
    
