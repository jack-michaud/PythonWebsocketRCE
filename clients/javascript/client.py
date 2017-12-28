from __future__ import absolute_import 

from clients.clients import Client
from clients.request import Request

from printer import Printer, clrs
p = Printer()

from clients.javascript.control import JavascriptControl


class JavascriptClient(Client):

    def __init__(self, socket, addr):
        super(JavascriptClient, self).__init__(socket, addr)

    def connection_handler(self):
        data = self.recv()
        req = Request(data)
        if req.is_valid_websocket():
            for resp in req.generate_websocket_response():
                self.send(resp)
            p.color_message(clrs.GREEN, "Confirmed connection from {}".format(self.addr[0]), "==>")

    def is_alive(self):
        f = Frame(OPCODE_PING, "", fin=1)
        self.send(f.build())
        resp = self.recv()
        return resp != ''

    def get_controller(self):
        return JavascriptControl
