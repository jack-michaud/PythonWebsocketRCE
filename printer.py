
class clrs:
    OKBLUE = '\033[94m'
    RED = '\033[31m'
    CYAN = '\033[36m'
    END = '\033[0m'

class Printer:

    def color_message(self, color, msg, insert):
        print "{}[{}]    {}{}".format(color, insert, msg, clrs.END)

    def info(self, msg):
        self.color_message(clrs.OKBLUE, msg, "*")

    def prompt(self, msg):
        self.color_message(clrs.CYAN, msg, "?")

    def error(self, msg):
        self.color_message(clrs.RED, msg, "!")



