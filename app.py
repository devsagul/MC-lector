# -*- coding: utf-8 -*-

import sys

# asr
from source import asr_client

# tts
from source import tts_client

# chat
from source import chat_client_lector

# gui
from source import gui

from PyQt5.QtCore import pyqtSignal, QObject


# Class for communication between different parts of the app
class Communicate(QObject):
    send = {"sig": pyqtSignal(), "text": ""}
    recieve = {"sig": pyqtSignal(), "text": ""}
    recieveQuestion = {"sig": pyqtSignal(), "text": "", "username": ""}
    answerQuestion = {"sig": pyqtSignal()}
    tts = {"sig": pyqtSignal(), "text": ""}


if __name__ == "__main__":
    communicator = Communicate()
    chat = chat_client_lector.ChatClient(communicator)
    chat.start()
    listener = asr_client.Listener(communicator)
    listener.start()
    speaker = tts_client.Speaker(communicator)
    speaker.start()
    app = gui.LectorApp(sys.argv, communicator)
    sys.exit(app.app.exec_())
