#!/bin/bash
set -e

export DISPLAY=:99

echo "checking xvfb..."
if ! pgrep Xvfb > /dev/null; then
  echo "starting xvfb..."
  Xvfb :99 -screen 0 1440x900x24 &
  sleep 3
fi

echo "checking fluxbox..."
if ! pgrep fluxbox > /dev/null; then
  echo "starting fluxbox..."
  fluxbox >/tmp/fluxbox.log 2>&1 &
fi

echo "checking x11vnc..."
if ! pgrep x11vnc > /dev/null; then
  echo "starting x11vnc..."
  x11vnc -display :99 -forever -nopw -listen 0.0.0.0 -xkb >/tmp/x11vnc.log 2>&1 &
fi

echo "checking novnc..."
if ! pgrep websockify > /dev/null; then
  echo "starting novnc..."
  websockify --web=/usr/share/novnc/ 6080 localhost:5900 >/tmp/novnc.log 2>&1 &
fi

sleep 5

echo "starting fastapi..."
exec uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}
