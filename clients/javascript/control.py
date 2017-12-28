
from clients.control import Control
from clients.javascript import commands

from ws4py.framing import Frame
from ws4py.streaming import Stream
# Frame opcodes defined in the spec.
OPCODE_CONTINUATION = 0x0
OPCODE_TEXT = 0x1
OPCODE_BINARY = 0x2
OPCODE_CLOSE = 0x8
OPCODE_PING = 0x9
OPCODE_PONG = 0xa

class JavascriptControl(Control):

    def get_command_module(self):
        return commands    

    def send_payload(self, payload, client_socket):
        f = Frame(OPCODE_TEXT, payload, fin=1)
        client_socket.send(f.build())

    def recv_response(self, socket):
        buffer = socket.recv()
        s = Stream()

        s.parser.send(buffer)
        if s.has_message:
            return s.message 

