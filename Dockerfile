FROM mcr.microsoft.com/playwright/python:v1.52.0-jammy

ENV DEBIAN_FRONTEND=noninteractive
ENV DISPLAY=:99
ENV PYTHONPATH=/app

RUN apt-get update && apt-get install -y \
    xvfb \
    fluxbox \
    x11vnc \
    novnc \
    websockify \
    unzip \
    wget \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libgtk-3-0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libpango-1.0-0 \
    libnss3 \
    libxss1 \
    libxtst6 \
    fonts-liberation \
    libappindicator3-1 \
    libdrm2 \
    libxkbcommon0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

RUN playwright install chromium
RUN playwright install-deps

# DOWNLOAD METAMASK EXTENSION
RUN mkdir -p /app/metamask-extension && \
    wget -O /tmp/metamask-chrome-13.30.0.zip \
    https://github.com/MetaMask/metamask-extension/releases/download/v13.30.0/metamask-chrome-13.30.0.zip && \
    unzip /tmp/metamask-chrome-13.30.0.zip -d /app/metamask-extension && \
    rm /tmp/metamask-chrome-13.30.0.zip

COPY . /app/

RUN mkdir -p /app/pw-profile
RUN chmod +x /app/start.sh

EXPOSE 8000

CMD ["/app/start.sh"]
