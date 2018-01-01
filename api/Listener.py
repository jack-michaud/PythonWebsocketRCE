
from sockets import WebsocketServer
import threading

class Listener:

    def __init__(self, port):
        self.listener_thread = None
        self.server = WebsocketServer("0.0.0.0", port)

    def start_listen(self, client_type):
        '''
        Listens for one client to connect.

        '''
        self.listener_thread = threading.Thread(target=self.server.listen, args=(client_type,), kwargs={"persist":False})
        self.listener_thread.daemon = True
        self.listener_thread.start()
        return
        
    def stop_listen(self):
        '''
        Stops listening once the listen thread collects one client.

        '''
        if self.listener_thread is not None:
            self.listener_thread.join()
            self.listener_thread = None
        return

    def get_clients(self):
        '''
        Gets EvalClient wrapper of each client for easier payload sending.
        '''
        return [EvalClient(c) for c in self.server.CLIENTS]

    def eval_in_all(self, cmd):
        '''
        
        '''
        client_sockets = self.get_clients()

        results = [None] * len(client_sockets)
        threads = [None] * len(client_sockets)

        def send_recv_thread(pl, c, idx):
            resp = c.eval(pl)
            results[idx] = resp
            return resp

        for idx in range(len(client_sockets)):
            t = threading.Thread(target=send_recv_thread, args=(cmd, client_sockets[idx], idx))
            threads[idx] = t
            t.daemon = True
            t.start()

        return results

class EvalClient:

    def __init__(self, client):
        self.client = client

    def eval(self, pl):
        controller = self.client.get_controller()()
        controller.send_payload(pl, self.client)
        resp = controller.recv_response(self.client)
        return resp






