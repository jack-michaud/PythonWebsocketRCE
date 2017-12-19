import threading
from request import Request

from printer import Printer
p = Printer()

class Client:

    active = False # is this connection active?

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def build_client(self, type):
        if CLIENTS.get(type) is None:
            raise Exception("Must be a valid client type. Types: {}".format(CLIENTS.keys()))
        return CLIENTS.get(type)(self)

    def start_handler_thread(self):
        import pdb; pdb.set_trace()
        thread = threading.Thread(target=self.__connection_handler)
        thread.start()

    def __recv(self):
        '''
        Get all data waiting to be received.

        @return Data buffer
        '''
        buffer = ""
        self.socket.settimeout(1)
        try:
            while True:
                data = connection.recv(1024)
                if not data:
                    break
                buffer = buffer + data
        except:
            pass
        return buffer

    def __send(self, data):
        self.socket.send(data)

    def __connection_handler(self):
        data = self.__recv()

        req = Request(data)
        if req.is_valid_websocket():
            for resp in req.generate_websocket_response():
                self.__send(resp)
            self.__recv()
            self.active = True
            print "Is active"

    def close():
        '''
        Closes socket connection.
        '''
        self.socket.close()


class JavascriptClient(Client):

    def __init__(self, client):
        self.socket = client.socket
        self.addr = client.addr


CLIENTS = {
    "BASE": Client,
    "javascript": JavascriptClient,
}
