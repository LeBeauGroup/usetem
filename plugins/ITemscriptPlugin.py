from useTEM.pluginTypes import IControlPlugin
import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
import os 
from yapsy.PluginManager import PluginManager

techniques_path = os.path.dirname(os.path.abspath(__file__))+'/techniques/temscript'

class ITemscriptPlugin(IControlPlugin):

	client = None

	def	start_connection(self, address):

		if address == 'local':
			from useTEM.modules.temscript.instrument import Instrument

			self.client = Instrument()

		else:
			self.client = xmlrpc.client.ServerProxy(address)

		# for technique in self.techniques:
		# 	print(technique)
		# 	technique.client = self.client
