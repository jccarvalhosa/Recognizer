import pyaudio
import wave
import os
import httplib
import json
import sys

###  RECORD WAV FILE ###

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
RECORD_SECONDS = 3
WAVE_OUTPUT_FILENAME = "output.wav"
FLAC_FILENAME = "output.flac"

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

print "* recording"

frames = []

for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)

print "* done recording"

stream.stop_stream()
stream.close()
p.terminate()

wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(p.get_sample_size(FORMAT))
wf.setframerate(RATE)
wf.writeframes(b''.join(frames))
wf.close()

### CONVERT TO FLAC ###

print "* changing format to flac"

os.system("flac {0} -o{1} -f".format(WAVE_OUTPUT_FILENAME, FLAC_FILENAME))

print "* changed"

### USE GOOGLE RECOGNIZER API

with open(FLAC_FILENAME, "r") as f:
    audio = f.read()
    url = "www.google.com"
    path = "/speech-api/v1/recognize?xjerr=1&client=chromium&lang=pt-BR"
    headers = { "Content-type": "audio/x-flac; rate=44100" };
    params = {"xjerr": "1", "client": "chromium"}
    print("* asking google")
    conn = httplib.HTTPSConnection(url)
    conn.request("POST", path, audio, headers)
    response = conn.getresponse()
    data = response.read()
    jsdata = json.loads(data)
    print "you said: ", jsdata["hypotheses"][0]["utterance"]
