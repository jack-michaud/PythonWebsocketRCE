import socket
import sys
import os
import threading
import base64
import hashlib
import commands

from ws4py.framing import Frame
from ws4py.streaming import Stream
# Frame opcodes defined in the spec.
OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xa

def get_commands():
    cmds = [commands.__dict__[c]()
            for c in commands.__dict__.keys()
            if "Command" in c]
    return cmds

from printer import Printer
p = Printer()

class WebsocketServer:

    CLIENTS = []
    COMMANDS = get_commands()

    def __init__(self, local_host, local_port):
        self.local_host = local_host
        self.local_port = local_port
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server.bind((local_host, local_port))
        except Exception as e:
            print "[!!]  Failed to listen on {}:{}".format(local_host, local_port)
            print str(e)
            sys.exit(0)

        self.server = server

    def listen(self, persist=False):
        p.info("Listening on {}:{}".format(self.local_host, self.local_port))
        p.info("Use Ctrl+C to stop listening!")
        self.server.listen(5)

        while True:
            try:
                client_socket,addr = self.server.accept()
                print "[==>] Received incoming connection from {}:{}".format(addr[0], addr[1])

                proxy_thread = threading.Thread(target=self.__connection_handler,
                                args=(client_socket, addr))
                proxy_thread.start()

                if persist:
                    continue
                else:
                    return
            except KeyboardInterrupt:
                p.info("Stopped listening.\n")
                return


    def __connection_handler(self, client_socket, addr):
        print "[*]   Handling connection"
        data = self.__recv_from(client_socket)
        req = Request(data)
        print "[*]   Is valid WebSocket: " + str(req.is_valid_websocket())

        if req.is_valid_websocket():
            print "[<==] Attempting to make connection..."
            try:
                for resp in req.generate_websocket_response():
                    client_socket.send(resp)
                print self.__recv_from(client_socket)
                print "[*]   Succeeded!"
                self.CLIENTS.append({"socket": client_socket, "addr": addr})
            except Exception as e:
                print "[!!]  Failed"
                print str(e)

    def control_clients(self, client_sockets):
        print ""
        p.info("Javascript code interpreter! '>quit' to close out interpreter,")
        p.info("'>close' to close the client connection. '>help' for custom commands.")
        while True:
            p.prompt("Javascript Code to Execute on {}: ".format([c['addr'] for c in client_sockets]))
            try:
                payload = raw_input()
                if ">quit" == payload:
                    p.info("Quit client control.")
                    return
                if ">close" == payload:
                    client_socket['socket'].close()
                    p.info("Closing client connection.")
                    for client_socket in client_sockets:
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
                client_socket['socket'].send(self.packet_bytes_with_payload(payload))
                buffer = self.__recv_from(client_socket['socket'])
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

    def __recv_from(self, connection):
        buffer = ""
        connection.settimeout(1)
        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                buffer = buffer + data
        except:
            pass

        return buffer

class Request:

    def __init__(self, raw):
        request_parts = raw.split('\n')
        request_parts = [part.replace('\r','') for part in request_parts]
        self.header = request_parts.pop(0)

        self.data = {part.split(': ')[0]: part.split(': ')[1]
                     for part in request_parts if part is not ''}

    def keys(self):
        return self.data.keys()

    def is_valid_websocket(self):
        keys = self.keys()

        return "Host" in keys and\
               "Upgrade" in keys and\
               "Connection" in keys and\
               "Sec-WebSocket-Key" in keys and\
               "Sec-WebSocket-Version" in keys and\
               "Origin" in keys

    def generate_accept_value(self):
        key = self.data['Sec-WebSocket-Key']
        GUID = "258EAFA5-E914-47DA-95CA-C5AB0DC85B11"

        decoded = key + GUID
        sha_decoded = hashlib.sha1(decoded).digest()
        return base64.b64encode(sha_decoded)

    def generate_websocket_response(self):
        return ["HTTP/1.1 101 Switching Protocols\r",
               "Upgrade: websocket\r" + \
               "Connection: Upgrade\r" + \
               "Sec-WebSocket-Protocol: chat\r" + \
               "Sec-WebSocket-Accept: " + self.generate_accept_value() + "\r\n\n"]
