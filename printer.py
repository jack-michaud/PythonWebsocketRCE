import logging

logger = logging.getLogger()

class clrs:
    OKBLUE = '\033[94m'
    RED = '\033[31m'
    CYAN = '\033[36m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    END = '\033[0m'
    WHITE = '\033[97m'

class Printer:

    def color_message(self, color, msg, insert):
        logger.info("{}[{}]    {}{}".format(color, insert, msg, clrs.END))
    def raw_color_message(self, color, msg):
        logger.info("{}{}{}".format(color, msg, clrs.END))
    def info(self, msg):
        self.color_message(clrs.OKBLUE, msg, "*")

    def success(self, msg):
        self.color_message(clrs.GREEN, msg, "+")

    def prompt(self, msg):
        self.color_message(clrs.CYAN, msg, "?")

    def error(self, msg):
        self.color_message(clrs.RED, msg, "!")

    def warn(self, msg):
        self.color_message(clrs.YELLOW, msg, ".")


