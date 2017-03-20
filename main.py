# -*- coding: utf-8 -*-


import signal
import sys
from sockets import WebsocketServer



if __name__ == "__main__":

    try:
        server = WebsocketServer("localhost", 1337)
        server.listen()

    except KeyboardInterrupt:
        print "[*] Closing connection..."
        server.server.close()
