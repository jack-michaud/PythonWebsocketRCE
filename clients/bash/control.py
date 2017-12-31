
import re

from clients.control import Control
from clients.bash import commands

class BashController(Control):

    def get_command_module(self):
        return commands    

    def send_payload(self, payload, client_socket):
        client_socket.send(payload)

    def recv_response(self, socket):
        buffer = socket.recv()
        socket.send("\n")

        def parse_response(b):
            resp = re.search(r"(?:\r\n)(.*)(?:\r\nbash-.*\$ )", b).group(1)
            return resp

        buffer = socket.recv()

        while True:
            try:
                resp = parse_response(buffer)
                break
            except:
                pass
        
        return resp