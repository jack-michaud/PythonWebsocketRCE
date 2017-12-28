from __future__ import absolute_import 

from clients.clients import Client
from clients.bash.control import BashController


from printer import Printer, clrs
p = Printer()


class BashClient(Client):

    def __init__(self, socket, addr):
        super(BashClient, self).__init__(socket, addr)

    def connection_handler(self):
        p.color_message(clrs.GREEN, "Confirmed connection from {}".format(self.addr[0]), "==>")
        self.recv()

    def is_alive(self):
        return True

    def get_controller(self):
        return BashController