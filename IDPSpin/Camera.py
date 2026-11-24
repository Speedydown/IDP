import io
import base64

# Modern Raspberry Pi OS (libcamera) ships picamera2; the old picamera
# library only works on the legacy camera stack. Try both, run without a
# camera when neither is available.
try:
    from picamera2 import Picamera2
except Exception:
    Picamera2 = None

try:
    import picamera
except Exception:
    picamera = None


class Camera(object):

    def __init__(self):
        self._Camera = None
        self._Kind = None
        self._StoredImage = ""
        try:
            if Picamera2 is not None:
                self._Camera = Picamera2()
                self._Camera.configure(self._Camera.create_still_configuration(main={"size": (640, 480)}))
                self._Camera.start()
                self._Kind = "picamera2"
            elif picamera is not None:
                self._Camera = picamera.PiCamera()
                self._Camera.resolution = (640, 480)
                self._Camera.brightness = 50
                self._Camera.start_preview()
                self._Kind = "picamera"
        except Exception as e:
            print("could not start camera: %s" % e)
            self._Camera = None
            self._Kind = None

    def takeImage(self, SafeImage=True):
        my_stream = io.BytesIO()
        try:
            if self._Kind == "picamera2":
                self._Camera.capture_file(my_stream, format="jpeg")
            elif self._Kind == "picamera":
                self._Camera.capture(my_stream, 'jpeg')
        except Exception:
            pass
        encoded_string = base64.b64encode(my_stream.getvalue()).decode("ascii")
        if SafeImage:
            self._StoredImage = encoded_string
        return encoded_string

    def getImageFromMemory(self):
        if len(self._StoredImage) > 0:
            return self._StoredImage
        else:
            return self.takeImage(False)

    def Exit(self):
        try:
            if self._Kind == "picamera2":
                self._Camera.stop()
            elif self._Kind == "picamera":
                self._Camera.stop_preview()
        except Exception:
            pass
