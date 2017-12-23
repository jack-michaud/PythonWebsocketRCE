import threading

from request import Request
from printer import Printer, clrs



p = Printer()

class Client(object):

    active = False # is this connection active?

    def __init__(self, socket, addr):
        self.socket = socket
        self.addr = addr

    def build_client(self, type):
        if CLIENTS.get(type) is None:
            raise Exception("Must be a valid client type. Types: {}".format(CLIENTS.keys()))
        return CLIENTS.get(type)(self)

    def start_handler_thread(self):
        p.info("Starting thread.")
        thread = threading.Thread(target=self.connection_handler)
        thread.start()

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

    def connection_handler(self):
        data = self.recv()
        req = Request(data)
        if req.is_valid_websocket():
            for resp in req.generate_websocket_response():
                self.send(resp)
            # self.recv()
            import pdb; pdb.set_trace()
            self.active = True
            p.color_message(clrs.GREEN, "Confirmed connection from {}".format(self.addr[0]), "==>")

    def close():
        '''
        Closes socket connection.
        '''
        self.socket.close()


class JavascriptClient(Client):

    def __init__(self, client):
        super(JavascriptClient, self).__init__(client.socket, client.addr)
        # self.socket = client.socket
        # self.addr = client.addr


CLIENTS = {
    "BASE": Client,
    "javascript": JavascriptClient,
}
