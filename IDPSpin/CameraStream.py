"""
spInOS camera stream - live MJPEG over HTTP, viewable in any browser.

    http://spin.local:8080/             page with live view + drive buttons
    http://spin.local:8080/stream.mjpg  raw MJPEG stream (VLC, OBS, <img>)
    http://spin.local:8080/snapshot.jpg single frame

The camera (rpicam-vid, MJPEG) only runs while at least one viewer is connected,
so the Pi 1 keeps its CPU for walking otherwise. Drive buttons talk to the spInOS
controller on localhost:1337 with the same commands the old Windows 8 app sent.
"""
import os
import socket
import subprocess
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PORT = int(os.environ.get("SPIN_CAM_PORT", "8080"))
WIDTH = int(os.environ.get("SPIN_CAM_WIDTH", "640"))
HEIGHT = int(os.environ.get("SPIN_CAM_HEIGHT", "480"))
FPS = int(os.environ.get("SPIN_CAM_FPS", "6"))
QUALITY = int(os.environ.get("SPIN_CAM_QUALITY", "60"))
IDLE_STOP_SECONDS = 5
SOI = b"\xff\xd8\xff"

ALLOWED_COMMANDS = {
    "move 10", "move 11", "move 12", "move 13", "move 14", "move 15", "move 16",
    "move 17", "move 18", "horn", "ping", "gmde",
    "smde 1", "smde 4", "smde 8",
    "smul 1", "smul 2", "smul 3", "smul 4", "smul 5",
}


class Camera(object):
    """Runs rpicam-vid on demand and keeps the latest JPEG frame."""

    def __init__(self):
        self._cond = threading.Condition()
        self._frame = None
        self._frame_id = 0
        self._viewers = 0
        self._last_viewer = 0.0
        self._proc = None
        self._lock = threading.Lock()
        threading.Thread(target=self._watchdog, daemon=True).start()

    # -- viewer bookkeeping -------------------------------------------------
    def acquire(self):
        with self._lock:
            self._viewers += 1
            self._last_viewer = time.time()
            if self._proc is None or self._proc.poll() is not None:
                self._start()

    def release(self):
        with self._lock:
            self._viewers -= 1
            self._last_viewer = time.time()

    def _watchdog(self):
        while True:
            time.sleep(1)
            with self._lock:
                idle = self._viewers <= 0 and time.time() - self._last_viewer > IDLE_STOP_SECONDS
                if idle and self._proc is not None:
                    self._stop()

    # -- camera process -----------------------------------------------------
    def _start(self):
        cmd = ["rpicam-vid", "-n", "-t", "0", "--codec", "mjpeg",
               "--width", str(WIDTH), "--height", str(HEIGHT),
               "--framerate", str(FPS), "-q", str(QUALITY), "-o", "-"]
        print("camera start: " + " ".join(cmd), flush=True)
        self._proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=0)
        threading.Thread(target=self._reader, args=(self._proc,), daemon=True).start()

    def _stop(self):
        print("camera stop (no viewers)", flush=True)
        try:
            self._proc.terminate()
            self._proc.wait(5)
        except Exception:
            self._proc.kill()
        self._proc = None
        with self._cond:
            self._frame = None  # never hand out a stale frame after a restart

    def _reader(self, proc):
        buf = b""
        while True:
            chunk = proc.stdout.read(65536)
            if not chunk:
                break
            buf += chunk
            # frames are concatenated JPEGs: emit everything before the next SOI
            while True:
                nxt = buf.find(SOI, 3)
                if nxt < 0:
                    break
                frame, buf = buf[:nxt], buf[nxt:]
                if frame.startswith(SOI):
                    with self._cond:
                        self._frame = frame
                        self._frame_id += 1
                        self._cond.notify_all()
            if len(buf) > 4 * 1024 * 1024:  # garbage guard
                buf = b""

    def wait_frame(self, last_id, timeout=5.0):
        with self._cond:
            self._cond.wait_for(lambda: self._frame is not None and self._frame_id != last_id, timeout)
            return self._frame_id, self._frame


CAMERA = Camera()


def spin_command(cmd):
    """Send one command to the spInOS controller (TCP 1337) and return its reply."""
    with socket.create_connection(("127.0.0.1", 1337), timeout=5) as s:
        s.sendall((cmd + "<EOF>").encode())
        buf = b""
        while b"<EOF>" not in buf:
            chunk = s.recv(4096)
            if not chunk:
                break
            buf += chunk
    return buf.decode("utf-8", "ignore").split("<EOF>")[0]


PAGE = """<!doctype html>
<html lang="nl"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Spin camera</title>
<style>
 :root { color-scheme: dark; }
 body { margin: 0; background: #111; color: #eee; font: 15px system-ui, sans-serif; display: flex; flex-direction: column; align-items: center; }
 h1 { font-size: 18px; font-weight: 600; margin: 12px 0 8px; }
 img { width: min(100vw - 16px, 960px); aspect-ratio: 4 / 3; background: #222; border-radius: 6px; }
 .pad { display: grid; grid-template-columns: repeat(3, 64px); gap: 6px; margin: 12px 0; }
 button { height: 52px; font-size: 20px; border: 0; border-radius: 8px; background: #2d2d2d; color: #eee; cursor: pointer; }
 button:active, button.on { background: #3d6ee8; }
 .row { display: flex; gap: 6px; flex-wrap: wrap; justify-content: center; }
 .row button { height: 36px; font-size: 14px; padding: 0 12px; }
 #status { color: #9a9a9a; min-height: 20px; margin-bottom: 12px; }
</style></head><body>
<h1>Spin - live camera</h1>
<img src="/stream.mjpg" alt="live camerabeeld">
<div class="pad">
 <button data-c="move 18">&#8598;</button><button data-c="move 11">&#8593;</button><button data-c="move 12">&#8599;</button>
 <button data-c="move 17">&#8634;</button><button data-c="move 10" class="stop">&#9632;</button><button data-c="move 13">&#8635;</button>
 <button data-c="move 16">&#8601;</button><button data-c="move 15">&#8595;</button><button data-c="move 14">&#8600;</button>
</div>
<div class="row">
 <button data-t="smul 1">langzaam</button><button data-t="smul 3">snel</button><button data-t="smul 5">turbo</button>
 <button data-t="smde 4">dans</button><button data-t="smde 1">lopen</button><button data-t="horn">toeter</button>
</div>
<div id="status">Houd een pijl ingedrukt om te lopen (of W/A/S/D), loslaten = stop.</div>
<script>
const status = document.getElementById('status');
async function send(c) {
  try { const r = await fetch('/cmd?c=' + encodeURIComponent(c), {method: 'POST'}); status.textContent = c + ' → ' + await r.text(); }
  catch (e) { status.textContent = 'fout: ' + e; }
}
document.querySelectorAll('.pad button').forEach(b => {
  const c = b.dataset.c;
  if (c === 'move 10') { b.addEventListener('click', () => send(c)); return; }
  b.addEventListener('pointerdown', e => { b.setPointerCapture(e.pointerId); b.classList.add('on'); send(c); });
  const up = () => { if (b.classList.contains('on')) { b.classList.remove('on'); send('move 10'); } };
  b.addEventListener('pointerup', up); b.addEventListener('pointercancel', up);
});
document.querySelectorAll('.row button').forEach(b => b.addEventListener('click', () => send(b.dataset.t)));
const keys = {w: 'move 11', s: 'move 15', a: 'move 17', d: 'move 13', q: 'move 18', e: 'move 12', z: 'move 16', c: 'move 14'};
let held = null;
addEventListener('keydown', e => { const c = keys[e.key.toLowerCase()]; if (c && held !== e.key) { held = e.key; send(c); } if (e.key === ' ') send('move 10'); });
addEventListener('keyup', e => { if (keys[e.key.toLowerCase()] && held !== null && held.toLowerCase() === e.key.toLowerCase()) { held = null; send('move 10'); } });
// safety: key released while the window lost focus -> no keyup ever arrives
addEventListener('blur', () => { if (held !== null) { held = null; send('move 10'); } });
document.addEventListener('visibilitychange', () => { if (document.hidden) send('move 10'); });
</script>
</body></html>
"""


class Handler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt, *args):
        pass

    def _send(self, code, ctype, body):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        path = urlparse(self.path).path
        if path in ("/", "/index.html"):
            self._send(200, "text/html; charset=utf-8", PAGE.encode("utf-8"))
        elif path == "/stream.mjpg":
            self._stream()
        elif path == "/snapshot.jpg":
            CAMERA.acquire()
            try:
                _, frame = CAMERA.wait_frame(-1, timeout=20)
                if frame:
                    self._send(200, "image/jpeg", frame)
                else:
                    self._send(503, "text/plain", b"no camera frame")
            finally:
                CAMERA.release()
        else:
            self._send(404, "text/plain", b"not found")

    def do_POST(self):
        u = urlparse(self.path)
        if u.path != "/cmd":
            self._send(404, "text/plain", b"not found")
            return
        cmd = parse_qs(u.query).get("c", [""])[0]
        if cmd not in ALLOWED_COMMANDS:
            self._send(400, "text/plain", b"command not allowed")
            return
        try:
            reply = spin_command(cmd)
            self._send(200, "text/plain; charset=utf-8", reply.encode("utf-8"))
        except Exception as e:
            self._send(502, "text/plain; charset=utf-8", ("spin not reachable: %s" % e).encode("utf-8"))

    def _stream(self):
        self.send_response(200)
        self.send_header("Content-Type", "multipart/x-mixed-replace; boundary=frame")
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.end_headers()
        CAMERA.acquire()
        print("viewer connected: %s" % self.client_address[0], flush=True)
        last = -1
        try:
            while True:
                last, frame = CAMERA.wait_frame(last)
                if not frame:
                    continue
                self.wfile.write(b"--frame\r\nContent-Type: image/jpeg\r\nContent-Length: "
                                 + str(len(frame)).encode() + b"\r\n\r\n" + frame + b"\r\n")
        except (BrokenPipeError, ConnectionResetError, OSError):
            pass
        finally:
            CAMERA.release()
            print("viewer left: %s" % self.client_address[0], flush=True)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("", PORT), Handler)
    server.daemon_threads = True
    print("spin camera on http://0.0.0.0:%d/" % PORT, flush=True)
    server.serve_forever()
