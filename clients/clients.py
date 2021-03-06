from __future__ import absolute_import
import threading
import abc

from ws4py.framing import Frame

OPCODE_PING = 0x9

from clients.request import Request
from printer import Printer, clrs


p = Printer()

class Client(object):

    __metaclass__ = abc.ABCMeta

    active = False # is this connection active?

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr
        self.name = None

    def __str__(self):
        return "{} {}".format(self.addr, "" if self.name is None else "\"{}\"".format(self.name))

    def start_handler_thread(self):
        p.info("Starting thread.")
        thread = threading.Thread(target=self.connection_handler)
        thread.start()

    def rename(self, name):
        self.name = name

    @abc.abstractmethod
    def get_controller(self):
        """
        Gets the controller class for this Client
        """
        pass

    @abc.abstractmethod
    def connection_handler(self):
        '''
        Establishes connection through handshake.

        '''
        pass

    @abc.abstractmethod
    def is_alive(self):
        '''
        Check to see if the connection is still active.
        '''
        pass

    def recv(self):
        '''
        Get all data waiting to be received.

        @return Data buffer
        '''
        buffer = ""
        exit = False
        self.socket.settimeout(1) # TODO Fixthis 
        while len(buffer) == 0 and not exit:
            try:
                while True:
                    data = self.socket.recv(1024)
                    if len(data) > 0 and data[-1] == "\n":
                        buffer = buffer + data[:-1]
                        exit = True
                        break
                    if data == "":
                        exit = True
                        break
                    buffer = buffer + data
            except:
                pass
        print "Returning"
        return buffer

    def send(self, data):
        try:
            self.socket.send(data)
        except Exception as e:
            p.error("Unable to send to this client.")

    def close(self):
        '''
        Closes socket connection.
        '''
        self.socket.close()


from clients.javascript import JavascriptClient
from clients.bash import BashClient
from clients.python import PythonClient

CLIENTS = {
    "BASE": Client,
    "javascript": JavascriptClient,
    "bash": BashClient,
    "python": PythonClient,
}
