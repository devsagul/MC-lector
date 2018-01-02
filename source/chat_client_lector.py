import threading
import sys
import select
import json
from websocket import create_connection
from .settings import host


class ChatClient(threading.Thread):
    def __init__(self, communicator):
        threading.Thread.__init__(self)
        self.c = communicator
        self.c.sendMessage.connect(self.send["sig"])

    def run(self):
        # connect to remote host
        try:
            s = create_connection(host)
            s.send('{"command": "join", "room": "1"}')
        except:
            print('Unable to connect')
            sys.exit()

        while 1:
            socket_list = [sys.stdin, s]
            # Get the list sockets which are readable
            ready_to_read, ready_to_write, in_error = select.select(socket_list, [], [])

            for sock in ready_to_read:
                if sock == s:
                    # incoming message from remote server, s
                    data = sock.recv()
                    if not data:
                        print('\nDisconnected from chat server')
                        sys.exit()
                    else:
                        dataJson = json.loads(data)
                        if "username" in dataJson.keys and "message" in dataJson and "msg_type" in dataJson.keys:
                            if dataJson["msg_type"] == 0:
                                self.c.recieve["text"] = dataJson["message"].encode("utf-8")
                                self.c.recieve["sig"].emit()
                            if dataJson["msg_type"] == 2:
                                self.c.questionText = dataJson["message"].encode("utf-8")
                                self.c.questionUsername = dataJson["username"].encode("utf-8")
                                self.c.recieveQuestion["sig"].emit()

    def send(self):
        self.s.send('{"command": "send", "room": 1, "message": "' + self.c.sendText + '"}')
        sys.stdout.write('{"command": "send", "room": 1, "message": "' + self.c.sendText + '"}')
        sys.stdout.flush()