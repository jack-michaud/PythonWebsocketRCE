from __future__ import absolute_import 

from clients.clients import Client
from clients.python.control import PythonController


from printer import Printer, clrs
p = Printer()


class PythonClient(Client):

    def __init__(self, socket, addr):
        super(PythonClient, self).__init__(socket, addr)

    def connection_handler(self):
        p.color_message(clrs.GREEN, "Confirmed connection from {}".format(self.addr[0]), "==>")
        self.recv()

    def is_alive(self):
        self.send("AAAAAAAAAA\n")
        resp = self.recv()
        return "EOF" in resp

    def get_controller(self):
        return PythonController