import threading
import abc

from ws4py.framing import Frame

OPCODE_PING = 0x9

from request import Request
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
        self.socket.settimeout(1)
        try:
            while True:
                data = self.socket.recv(1024)
                if not data:
                    break
                buffer = buffer + data
        except:
            pass
        return buffer

    def send(self, data):
        self.socket.send(data)

    def close(self):
        '''
        Closes socket connection.
        '''
        self.socket.close()


from clients.javascript import JavascriptClient

CLIENTS = {
    "BASE": Client,
    "javascript": JavascriptClient,
}
