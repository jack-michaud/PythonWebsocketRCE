
from clients.control import Control
from clients.javascript import commands

class JavascriptControl(Control):


    def get_commands(self):
        cmds = [commands.__dict__[c]()
                for c in commands.__dict__.keys()
                if "Command" in c]
        return cmds     

    def control(self, client_sockets):
        p.info("Javascript code interpreter! '>quit' to close out interpreter,")
        p.info("'>close' to close the client connection. '>help' for custom commands.")
        while True:
            p.prompt("Javascript Code to Execute on {}: ".format([c.addr for c in client_sockets]))
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
                    p.info(">quit - quits the Javascript interpreter")
                    p.info(">close - closes the client connection")
                    print ""
                    print "CUSTOM COMMANDS"
                    for command in self.get_commands:
                        print command.name
                        print "|--- >" + command.command
                        print "|--- " + command.description
                    continue
            except KeyboardInterrupt as e:
                p.info("Closing client")
                return

            # Shortcut Commands (see commands.py)
            for command in self.COMMANDS:
                if command.matches_command(payload):
                    payload = command.get_payload()
                    break

            for client_socket in client_sockets:
                client_socket.send(self.packet_bytes_with_payload(payload))
                buffer = client_socket.recv()
                s = Stream()

                s.parser.send(buffer)
                if s.has_message:
                    print s.message



