
from sockets import WebsocketServer
import threading

class Listener:

    def __init__(self, port):
        self.listener_thread = None
        self.server = WebsocketServer("0.0.0.0", port)

    def start_listen(self, client_type):
        self.listener_thread = threading.Thread(target=self.server.listen, args=(client_type,), kwargs={"persist":True})
        self.listener_thread.daemon = True
        self.listener_thread.start()
        return
        
    def stop_listen(self):
        if self.listener_thread is not None:
            self.listener_thread.stop()
            self.listener_thread = None
        return

    def get_clients(self):
        return self.server.CLIENTS



