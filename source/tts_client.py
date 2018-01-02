# -*- coding: utf-8 -*-

import threading

# asrclient from Yandex.cloud SDK
from yandexcloudSDK import ttsclient as client
from .settings import speaker as s

import pyaudio
import wave

import subprocess
import time


class Speaker(threading.Thread):
    def __init__(self, communicator):
        threading.Thread.__init__(self)
        self.c = communicator
        self.c.tts["sig"].connect(self.tts)

    def tts(self):
        file = open("./out.wav", "wr")
        client.generate(text=self.c.tts["text"].decode('utf8'), speaker=s, file=file)
        # define stream chunk
        chunk = 1024

        # open a wav format audio
        f = wave.open(r"./out.wav", "rb")
        # instantiate PyAudio
        p = pyaudio.PyAudio()
        # open stream
        stream = p.open(format=p.get_format_from_width(f.getsampwidth()),
                        channels=f.getnchannels(),
                        rate=f.getframerate(),
                        output=True)
        # read data
        data = f.readframes(chunk)

        # toggle microphone
        subprocess.check_output(['bash', '-c', "amixer -q -D pulse sset Capture toggle"])

        # play stream
        while data:
            stream.write(data)
            data = f.readframes(chunk)

        # sleep half a second so audio would not interrupt
        time.sleep(.5)
        stream.stop_stream()
        stream.close()

        # toggle microphone
        subprocess.check_output(['bash', '-c', "amixer -q -D pulse sset Capture toggle"])

        # close PyAudio
        p.terminate()
