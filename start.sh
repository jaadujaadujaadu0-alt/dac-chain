#!/bin/bash
set -e

export DISPLAY=:99

echo "starting xvfb..."
Xvfb :99 -screen 0 1440x900x24 &

sleep 2

echo "starting fluxbox..."
fluxbox &

echo "starting x11vnc..."
x11vnc -display :99 -forever -nopw -listen 0.0.0.0 -xkb &

echo "starting novnc..."
websockify --web=/usr/share/novnc/ 6080 localhost:5900 &

sleep 3

echo "starting fastapi..."
uvicorn app:app --host 0.0.0.0 --port 8000
