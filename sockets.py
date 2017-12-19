import socket
import sys
import os
import threading
import base64
import hashlib
from client_commands import commands
from clients import CLIENTS

from ws4py.framing import Frame
from ws4py.streaming import Stream
# Frame opcodes defined in the spec.
OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xa

def build_client(socket, addr, type):
    return CLIENTS['BASE'](socket, addr).build_client(type)

def get_commands():
    cmds = [commands.__dict__[c]()
            for c in commands.__dict__.keys()
            if "Command" in c]
    return cmds

from printer import Printer, clrs
p = Printer()

class WebsocketServer:

    CLIENTS = []
    COMMANDS = get_commands()
    CLIENT_TYPE = None # Type of client to connect: javascript, ...
    # CLIENT: Initialized in constructor

    def __init__(self, local_host, local_port, client_type):
        self.local_host = local_host
        self.local_port = local_port
        if client_type is None:
            raise Exception("Must specify client_type in constructor")
        self.CLIENT_TYPE = client_type

        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((local_host, local_port))
        except Exception as e:
            p.error("Failed to listen on {}:{}".format(local_host, local_port))
            p.error(str(e))
            sys.exit(0)

        self.server = server

    def listen(self, persist=False):
        p.info("Listening on {}:{}".format(self.local_host, self.local_port))
        p.info("Use Ctrl+C to stop listening!")
        self.server.listen(5)

        waiting_list = []

        while True:

            # Check if any clients on the waiting_list have been activated
            new_list = []
            for client in waiting_list:
                if client.active:
                    p.color_message(self, clrs.GREEN, "Confirmed connection from {}".format(client.addr[0]), "==>")
                else:
                    new_list.append(client)
            waiting_list = new_list

            try:
                client_socket,addr = self.server.accept()
                new_client = build_client(client_socket, addr, self.CLIENT_TYPE)
                new_client.start_handler_thread()
                p.color_message(clrs.GREEN, "Received connection from {}".format(addr[0]), "<==")
                self.CLIENTS.append(new_client)
                waiting_list.append(new_client)

                if persist:
                    continue
                else:
                    return
            except KeyboardInterrupt:
                p.info("Stopped listening.\n")
                return


    def control_clients(self, client_sockets):
        print ""
        p.info("Javascript code interpreter! '>quit' to close out interpreter,")
        p.info("'>close' to close the client connection. '>help' for custom commands.")
        while True:
            p.prompt("Javascript Code to Execute on {}: ".format([c.addr for c in client_sockets]))
            try:
                payload = raw_input()
                if ">quit" == payload:
                    p.info("Quit client control.")
                    return
                if ">close" == payload:
                    for client_socket in client_sockets:
                        client_socket.close()
                        p.info("Closing client connection: {}".format(client_socket.addr))
                        self.CLIENTS.remove(client_socket)
                    return
                if ">help" == payload:
                    p.info(">quit - quits the Javascript interpreter")
                    p.info(">close - closes the client connection")
                    print ""
                    print "CUSTOM COMMANDS"
                    for command in self.COMMANDS:
                        print command.name
                        print "|--- >" + command.command
                        print "|--- " + command.description
                    continue
            except KeyboardInterrupt as e:
                p.info("Closing client")
                return

            # Shortcut Commands (see commands.py)
            for command in self.COMMANDS:
                if command.matches_command(payload):
                    payload = command.get_payload()
                    break

            for client_socket in client_sockets:
                client_socket.__send(self.packet_bytes_with_payload(payload))
                buffer = client_socket.__recv()
                s = Stream()

                s.parser.send(buffer)
                if s.has_message:
                    print s.message

    def packet_bytes_with_payload(self, payload):
        f = Frame(OPCODE_TEXT, payload, fin=1)
        return f.build()

    def send_data_to_client(self, data, client_socket):
        pass

    def close_websocket_client(self, client_socket):
        pass

