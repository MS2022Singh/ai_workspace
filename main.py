"""
AI Workspace - desktop entry point.

Starts the local FastAPI server (reachable on this machine and, if Mobile
access is turned on, your LAN) and opens it in a native desktop window via
pywebview. Close the window to exit; background tasks that are mid-run will
resume being processed next time the app is started (queued tasks persist
in the local database).
"""
import sys
from pathlib import Path

# When launched via pythonw.exe (no console window), Windows gives the
# process NO real stdout/stderr -- they are None. If anything underneath
# (uvicorn, asyncio, a dependency) tries to log a startup error the normal
# way, that write itself silently fails, which can hide the real error
# completely. Redirect to a real file FIRST, before any other import, so
# every layer always has somewhere safe to write.
_APP_DIR = Path.home() / ".ai_workspace"
_APP_DIR.mkdir(parents=True, exist_ok=True)
_LOG_FILE = None
if sys.stdout is None or sys.stderr is None:
    # No real console attached (this is what happens under pythonw.exe) --
    # redirect to a file so nothing silently fails trying to write to None.
    _LOG_FILE = open(_APP_DIR / "app.log", "a", encoding="utf-8", buffering=1)
    sys.stdout = _LOG_FILE
    sys.stderr = _LOG_FILE
# If a real console IS attached (e.g. running with "python main.py
# --browser" instead of pythonw), leave stdout/stderr alone so that
# diagnostic output is actually visible live, which is the whole point
# of that mode.

import os

# Some Windows machines (especially managed/corporate ones) have a
# system-wide proxy configured that, misconfigured, intercepts even
# 127.0.0.1 traffic and silently stalls it. Force local traffic to bypass
# any such proxy -- this app never needs one for itself, and it must be
# set before urllib/requests are used anywhere in this process.
os.environ["NO_PROXY"] = "127.0.0.1,localhost,::1," + os.environ.get("NO_PROXY", "")
os.environ["no_proxy"] = os.environ["NO_PROXY"]

import threading
import time
import socket
import traceback
import urllib.request
import urllib.error

import uvicorn
import webview

HOST = "127.0.0.1"
LOG_PATH = _APP_DIR / "startup_error.log"
GENERAL_LOG_PATH = _APP_DIR / "app.log"

_server_error = []  # populated if the server thread crashes


def _log(msg: str):
    print(f"[main] {msg}")


def _find_free_port(start=8765, tries=20):
    port = start
    for _ in range(tries):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex((HOST, port)) != 0:
                return port
        port += 1
    return start


def _wait_for_server(port, timeout=60.0):
    deadline = time.time() + timeout
    url = f"http://{HOST}:{port}/api/health"
    # Explicit no-proxy opener as a second layer of defense, independent of
    # the NO_PROXY env vars set above.
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
    while time.time() < deadline:
        if _server_error:
            return False
        try:
            # Generous per-attempt timeout: on some machines (commonly due
            # to antivirus/security software inspecting each new local
            # connection) a request can take several seconds to complete
            # even though it ultimately succeeds. A short per-attempt
            # timeout here would abort a request that was about to work.
            with opener.open(url, timeout=10) as resp:
                if resp.status == 200:
                    return True
        except (urllib.error.URLError, ConnectionError, OSError):
            pass
        time.sleep(0.5)
    return False


def _error_page(message: str) -> str:
    safe = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return f"""
    <html><body style="background:#0B0E14;color:#E7EAEE;font-family:sans-serif;
    padding:40px;line-height:1.6;">
    <h2 style="color:#E5484D;">AI Workspace couldn't start</h2>
    <p>The local server hit an error on startup. Details:</p>
    <pre style="background:#161B25;border:1px solid #1E242E;border-radius:6px;
    padding:14px;white-space:pre-wrap;font-size:13px;">{safe}</pre>
    <p style="color:#8A93A3;font-size:13px;">
    Full log saved to: {LOG_PATH}<br>
    Try closing this window and running <b>run.bat</b> again so it can
    reinstall/check dependencies, then reopen the app.</p>
    </body></html>
    """


def _port_in_use(port) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(0.5)
        return s.connect_ex((HOST, port)) == 0


def _tail_log(n_chars=4000) -> str:
    try:
        text = GENERAL_LOG_PATH.read_text(encoding="utf-8", errors="replace")
        return text[-n_chars:] if text else "(log file is empty)"
    except Exception as e:
        return f"(could not read log file: {e})"


class DesktopAPI:
    """
    Exposed to JavaScript as window.pywebview.api.*. Downloads inside an
    embedded WebView2 window can't reliably rely on the usual browser
    trick of a hidden, auto-clicked <a download> link -- so instead the
    frontend hands bytes/text to Python here, and Python shows a real,
    native "Save As" dialog and writes the file itself. (In browser mode,
    via "Open in Browser (diagnostic).bat", this class isn't used at all
    -- the frontend falls back to the normal browser download mechanism,
    which works fine there.)
    """

    def __init__(self):
        self.window = None

    def _save(self, filename, write_fn):
        try:
            result = self.window.create_file_dialog(webview.SAVE_DIALOG, save_filename=filename)
            if not result:
                return {"ok": False, "cancelled": True}
            path = result[0] if isinstance(result, (list, tuple)) else result
            write_fn(path)
            return {"ok": True, "path": str(path)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    def save_binary(self, filename, base64_data):
        import base64
        data = base64.b64decode(base64_data)
        return self._save(filename, lambda path: open(path, "wb").write(data))

    def save_text(self, filename, text):
        return self._save(filename, lambda path: open(path, "w", encoding="utf-8").write(text))


def main():
    browser_mode = "--browser" in sys.argv

    _log("=" * 60)
    _log("Starting AI Workspace" + (" (browser mode)" if browser_mode else ""))
    port = _find_free_port()
    _log(f"Selected port: {port}")

    def run_server():
        try:
            if _port_in_use(port):
                raise RuntimeError(
                    f"Port {port} is already in use. A previous AI Workspace "
                    "process may still be running in the background. Open "
                    "Task Manager, end any 'pythonw.exe' or 'AI Workspace' "
                    "processes, then try again."
                )
            _log("Importing backend app...")
            from backend.app import app
            app.state.port = port
            _log("Calling uvicorn.run() now -- this blocks while serving...")
            uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
            _log("uvicorn.run() returned on its own (server stopped).")
        except BaseException:
            tb = traceback.format_exc()
            _server_error.append(tb)
            _log("Server thread failed:\n" + tb)
            try:
                LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
                LOG_PATH.write_text(tb, encoding="utf-8")
            except Exception:
                pass

    t = threading.Thread(target=run_server, daemon=True)
    t.start()

    if browser_mode:
        # Skip pywebview entirely. Useful both as a workaround (a regular
        # browser is a much more "normal" HTTP client than an embedded
        # WebView2 control) and as a diagnostic: if the regular browser
        # also can't reach it, the cause is outside this app (most likely
        # security software intercepting loopback traffic), not pywebview.
        import webbrowser
        url = f"http://{HOST}:{port}/"
        print(f"\nWaiting for the server, then opening {url} in your default browser...")
        ok = _wait_for_server(port)
        if ok:
            webbrowser.open(url)
            print(f"Opened {url} -- if your browser also can't reach it, this isn't a pywebview issue.")
            print("Leave this window open while using the app. Press Ctrl+C here to stop the server.\n")
        else:
            print("Server did not become ready. See details above/in app.log.")
        t.join()
        return

    ok = _wait_for_server(port)
    _log(f"_wait_for_server result: {ok}")

    api = DesktopAPI()

    if ok:
        window = webview.create_window(
            "AI Workspace",
            f"http://{HOST}:{port}/",
            width=1280,
            height=820,
            min_size=(1000, 650),
            js_api=api,
        )
    else:
        if _server_error:
            detail = _server_error[0]
        else:
            detail = (
                "The server did not respond in time, and didn't report any "
                "Python error either. Here is the raw startup log, which "
                "may show what actually happened (e.g. from uvicorn itself):\n\n"
                + _tail_log()
            )
        window = webview.create_window(
            "AI Workspace - Error",
            html=_error_page(detail),
            width=1000,
            height=700,
            js_api=api,
        )
    api.window = window

    try:
        # Force the modern Chromium-based engine. Without this, pywebview
        # can silently fall back to the old Internet Explorer engine on
        # some Windows setups, which doesn't support the JavaScript this
        # app uses (buttons/forms can appear to "do nothing").
        webview.start(gui="edgechromium")
    except Exception as e:
        print(
            "Could not start the modern app window engine "
            f"(Microsoft Edge WebView2 Runtime). Error: {e}\n"
            "Install it from: "
            "https://developer.microsoft.com/microsoft-edge/webview2/\n"
            "Falling back to the default engine, which may not work correctly."
        )
        webview.start()


if __name__ == "__main__":
    main()
