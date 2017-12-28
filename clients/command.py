from __future__ import absolute_import

import abc

class CMD(object):
    '''
    An abstract Command class. Every command must extend/implement this.
    '''
    
    def __init__(self, name, command, description):
        self.name = name
        self.command = command
        self.description = description
        self.argv = []

    def matches_command(self, arg):
        if len(arg) > 0 and arg[0] == ">":
            if arg[1:].split(' ')[0] == self.command:
                self.argv = arg.split(' ')
                return True
        return False

    @abc.abstractmethod
    def get_payload(self):
        pass
