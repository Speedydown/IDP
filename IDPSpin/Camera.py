import time
try:
    import picamera
except:
    "could not start camera"
import io
import base64
try:
    from VideoCapture import Device
except:
    "could not start local webcam"

class Camera(object):

    def __init__(self):
        try:
            self._Camera = picamera.PiCamera()
            self._Camera.resolution = (640, 480)
            self._Camera.brightness = 50
            self._Camera.start_preview()
            self._StoredImage = ""
        except:
            self._Camera = Device()

    
    def takeImage(self):
        my_stream = io.BytesIO()
        try:
            self._Camera.capture(my_stream, 'jpeg')
        except:
            my_stream = self._Camera.saveSnapshot('image.jpg')
        encoded_string = base64.b64encode(my_stream.getvalue())
        self._StoredImage = encoded_string
        return encoded_string

    def getImageFromMemory(self):
        if len(self._StoredImage) > 0:
            return self._StoredImage
        else:
            return self.takeImage()

    def Exit(self):
        self._Camera.stop_preview()
        
        
    
