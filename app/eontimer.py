from http.server import HTTPServer, SimpleHTTPRequestHandler
import threading
import subprocess
import os
from pathlib import Path

_SERVER = None
_SERVER_THREAD = None
_BROWSER_PROCESS = None
_ORIGINAL_CWD = None
_EXIT_CALLBACK = None


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        return


class EonTimerHandler(QuietHandler):
    def do_GET(self):
        if self.path.startswith("/eontimer/close"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"closing")
            threading.Thread(target=lambda: request_exit(), daemon=True).start()
            return

        super().do_GET()


def _get_eontimer_dir() -> Path:
    return Path(__file__).resolve().parent / "third_party" / "eontimer" / "EonTimer"


def _watch_browser_process():
    global _BROWSER_PROCESS

    if _BROWSER_PROCESS is None:
        return

    try:
        _BROWSER_PROCESS.wait(timeout=1)
    except subprocess.TimeoutExpired:
        return

    request_exit()


def request_exit(callback=None):
    global _EXIT_CALLBACK

    active_callback = callback if callback is not None else _EXIT_CALLBACK
    _EXIT_CALLBACK = None
    stop_eontimer()

    if active_callback is not None:
        active_callback()


def start_eontimer(exit_callback=None):
    global _SERVER, _SERVER_THREAD, _BROWSER_PROCESS, _ORIGINAL_CWD, _EXIT_CALLBACK

    if _SERVER is not None:
        return

    _EXIT_CALLBACK = exit_callback

    _ORIGINAL_CWD = Path.cwd()
    eontimer_dir = _get_eontimer_dir()

    if not eontimer_dir.exists():
        raise FileNotFoundError(f"EonTimer directory not found: {eontimer_dir}")

    os.chdir(eontimer_dir)

    _SERVER = HTTPServer(("127.0.0.1", 8000), EonTimerHandler)
    _SERVER_THREAD = threading.Thread(target=_SERVER.serve_forever, daemon=True)
    _SERVER_THREAD.start()

    chrome_path = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    if os.path.exists(chrome_path):
        _BROWSER_PROCESS = subprocess.Popen([
            chrome_path,
            "--new-window",
            "--kiosk",
            "--app=http://127.0.0.1:8000",
        ])
    else:
        _BROWSER_PROCESS = None

    if _BROWSER_PROCESS is not None:
        watcher = threading.Thread(target=_watch_browser_process, daemon=True)
        watcher.start()


def stop_eontimer():
    global _SERVER, _SERVER_THREAD, _BROWSER_PROCESS, _ORIGINAL_CWD, _EXIT_CALLBACK

    if _SERVER is not None:
        _SERVER.shutdown()
        _SERVER.server_close()
        _SERVER = None

    if _SERVER_THREAD is not None:
        _SERVER_THREAD.join(timeout=1)
        _SERVER_THREAD = None

    if _BROWSER_PROCESS is not None:
        _BROWSER_PROCESS.terminate()
        try:
            _BROWSER_PROCESS.wait(timeout=2)
        except subprocess.TimeoutExpired:
            _BROWSER_PROCESS.kill()
        _BROWSER_PROCESS = None

    try:
        subprocess.run([
            "taskkill",
            "/F",
            "/IM",
            "chrome.exe",
        ], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except Exception:
        pass

    if _ORIGINAL_CWD is not None:
        os.chdir(_ORIGINAL_CWD)
        _ORIGINAL_CWD = None

    _EXIT_CALLBACK = None

