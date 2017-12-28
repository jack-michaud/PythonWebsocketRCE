
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
        buffer = socket.recv()
        return buffer