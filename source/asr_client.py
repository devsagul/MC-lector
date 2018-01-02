# -*- coding: utf-8 -*-
import threading

# asrclient from Yandex.cloud SDK
from .yandexcloudSDK import client


class Listener(threading.Thread):
    def __init__(self, communicator):
        threading.Thread.__init__(self)
        self.c = communicator

    def run(self):
        chunks = client.read_chunks_from_pyaudio()
        client.recognize(chunks, callback=self.my_callback)

    def my_callback(self, utterance):
        if utterance in ("Ваши вопросы.", 'Следующий вопрос :'):
            self.c.answerQuestion["sig"].emit()
        else:
            self.c.send["text"] = utterance
            self.c.send["sig"].emit()
