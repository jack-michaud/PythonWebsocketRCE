import abc

'''
Abstract class to describe the command line interaction for a client.

'''

class Control(object):

	@abc.abstractmethod
	def get_commands(self):	
		'''
		Gets the commands that can be executed by this controller.

		:rtype: list[CMD]
		'''
		pass

	@abc.abstractmethod
	def control(self, client_sockets):
		'''
		Control loop; takes in commands. Exits on return.
		'''
		pass