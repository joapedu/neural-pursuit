FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    libsdl2-dev \
    libsdl2-image-dev \
    libsdl2-mixer-dev \
    libsdl2-ttf-dev \
    libportmidi-dev \
    libswscale-dev \
    libavformat-dev \
    libavcodec-dev \
    x11-apps \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DISPLAY=:0
ENV PYTHONUNBUFFERED=1
ENV SDL_AUDIODRIVER=dummy
ENV PULSE_SERVER=unix:/tmp/pulse-socket

CMD ["python", "main.py"]

