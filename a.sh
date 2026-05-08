#!/bin/bash

# Exit immediately if a command exits with a non-zero status
set -e

echo "--- Updating system and installing Python ---"
sudo apt update
sudo apt install python3 python3-pip -y

echo "--- Installing Python packages ---"
pip3 install python-telegram-bot python-dotenv playwright

echo "--- Installing Playwright and Chromium ---"
python3 -m playwright install
python3 -m playwright install chromium
python3 -m playwright install-deps

echo "--- Cleaning up Yarn sources ---"
# Check if file exists before trying to remove it
if [ -f /etc/apt/sources.list.d/yarn.list ]; then
    sudo rm /etc/apt/sources.list.d/yarn.list
fi

echo "--- Installing required system libraries ---"
sudo apt install -y \
    libatk1.0-0t64 \
    libatk-bridge2.0-0t64 \
    libgtk-3-0t64 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2t64 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    libdrm2 \
    libxkbcommon0

echo "--- Forcing Chromium installation ---"
python3 -m playwright install --force chromium

echo "--- Setup Complete! ---"