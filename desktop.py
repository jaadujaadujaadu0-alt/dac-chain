import os
import subprocess

desktop_started = False


def start_desktop():
    global desktop_started

    if desktop_started:
        return

    os.environ["DISPLAY"] = ":99"

    subprocess.Popen([
        "Xvfb",
        ":99",
        "-screen",
        "0",
        "1440x900x24"
    ])

    subprocess.Popen(["fluxbox"])

    subprocess.Popen([
        "x11vnc",
        "-display",
        ":99",
        "-forever",
        "-nopw",
        "-listen",
        "localhost",
        "-xkb"
    ])

    subprocess.Popen([
        "websockify",
        "--web=/usr/share/novnc/",
        "6080",
        "localhost:5900"
    ])

    desktop_started = True