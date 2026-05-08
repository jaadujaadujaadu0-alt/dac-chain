import os

desktop_started = False


def start_desktop():
    global desktop_started

    if desktop_started:
        return {
            "success": True,
            "desktop_started": True,
            "display": ":99",
            "message": "desktop already running"
        }

    os.environ["DISPLAY"] = ":99"

    desktop_started = True

    return {
        "success": True,
        "desktop_started": True,
        "display": ":99",
        "message": "desktop ready via Docker/start.sh"
    }
