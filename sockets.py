import socket
import sys
import os
import threading
import base64
import hashlib

from clients import CLIENTS as SOCKET_CLIENTS

from printer import Printer, clrs
p = Printer()

class WebsocketServer:

    CLIENTS = []
    CLIENT_TYPE = None # Type of client to connect: javascript, ...
    # CLIENT: Initialized in constructor

    def __init__(self, local_host, local_port, client_type):
        self.local_host = local_host
        self.local_port = local_port
        if client_type is None:
            raise Exception("Must specify client_type in constructor")
        if SOCKET_CLIENTS.get(client_type) is None:
            raise Exception("Must be a valid client type. Types: {}".format(SOCKET_CLIENTS.keys()))
        self.CLIENT_TYPE = client_type
        self.server = None

    def bind(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind((self.local_host, self.local_port))
        except Exception as e:
            p.error("Failed to listen on {}:{}".format(self.local_host, self.local_port))
            p.error(str(e))
            sys.exit(0)

    def listen(self, persist=False):
        p.info("Listening on {}:{}".format(self.local_host, self.local_port))
        p.info("Use Ctrl+C to stop listening!")
        self.bind()
        self.server.listen(5)

        while True:

            try:
                client_socket,addr = self.server.accept()
                new_client = SOCKET_CLIENTS[self.CLIENT_TYPE](client_socket, addr)
                new_client.start_handler_thread()
                self.CLIENTS.append(new_client)
                p.color_message(clrs.GREEN, "Received connection from {}".format(addr[0]), "<==")

                if persist:
                    continue
                else:
                    return
            except KeyboardInterrupt:
                break

        p.info("Stopped listening.\n")
        self.server.close()


    def control_clients(self, client_sockets):
        controller = client_sockets[0].get_controller()
        for client in client_sockets:
            if client.get_controller() is not controller:
                p.error("Cannot control these sockets; they are not all the same type.")
                return
        controller().control(client_sockets)

    def send_data_to_client(self, data, client_socket):
        pass

    def close_websocket_client(self):
        self.server.close()
        [client.close() for client in self.CLIENTS]

