
import re

from clients.control import Control
from clients.python import commands

class PythonController(Control):

    def get_command_module(self):
        return commands    

    def send_payload(self, payload, client_socket):
        if payload != "\n":
            client_socket.send(str(payload))
        client_socket.send("\n")

    def recv_response(self, socket):
        buffer = socket.recv()
        return buffer
