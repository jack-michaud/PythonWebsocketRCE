import abc
import threading

'''
Abstract class to describe the command line interaction for a client.

'''


from printer import Printer, clrs
p = Printer()

class Control(object):

    def __init__(self):
        self.COMMANDS = None

    @abc.abstractmethod
    def get_command_module(self):
        """
        Gets the module with all the command objects in it. 
        Commands must be named with "Command" in the classname.
        """
        pass

    def get_commands(self):
        if self.COMMANDS is not None:
            return self.COMMANDS

        commands = self.get_command_module()
        cmds = [commands.__dict__[c]()
                for c in commands.__dict__.keys()
                if "Command" in c]
        self.COMMANDS = cmds
        return cmds  

    @abc.abstractmethod
    def send_payload(self, payload, socket):
        """
        Sends payload to the client
        """
        pass

    @abc.abstractmethod
    def recv_response(self, socket):
        """
        Receive response from socket.

        :returns: The response from the socket
        :rtype:   str | None
        """
        pass

    def control(self, client_sockets):
        '''
        Control loop; takes in commands. Exits on return.
        Client sockets must all be the same client type.
        '''
        p.info("Code interpreter! '>quit' to close out interpreter,")
        p.info("'>close' to close the client connection. '>help' for custom commands.")
        while True:
            p.prompt("Code to Execute on {}: ".format([str(c) for c in client_sockets]))
            try:
                payload = raw_input()
                if ">quit" == payload:
                    p.info("Quit client control.")
                    return
                if ">close" == payload:
                    for client_socket in client_sockets:
                        client_socket.close()
                        p.info("Closing client connection: {}".format(client_socket.addr))
                        self.CLIENTS.remove(client_socket)
                    return
                if ">help" == payload:
                    p.info(">quit - quits the interpreter")
                    p.info(">close - closes the client connection")
                    print ""
                    print "CUSTOM COMMANDS"
                    for command in self.get_commands():
                        print command.name
                        print "|--- >" + command.command
                        print "|--- " + command.description
                    continue
            except KeyboardInterrupt as e:
                p.info("Closing client")
                return

            # Shortcut Commands (see commands.py)
            for command in self.get_commands():
                if command.matches_command(payload):
                    payload = command.get_payload()
                    break

            def send_recv_thread(pl, c):
                self.send_payload(pl, c)
                p.success("Sent to {}".format(str(c)))   
                resp = self.recv_response(c)
                if resp is not None:
                    p.warn("Response from {}".format(str(c)))
                    p.raw_color_message(clrs.WHITE, resp)
                    print resp
                return 1

            for client_socket in client_sockets:
                t = threading.Thread(target=send_recv_thread, args=(payload, client_socket))
                t.daemon = True
                t.start()


                

