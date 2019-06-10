from useTEM.pluginTypes import IControlPlugin
import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
import os 
from yapsy.PluginManager import PluginManager


class ITEMscriptPlugin(IControlPlugin):

	client = None # server proxy or direct local comtypes

	def	start_connection(self, address):

		techniques_path = os.path.dirname(os.path.abspath(__file__))+'/techniques/temscript'

		if address == 'local':
			from useTEM.modules.temscript.instrument import Instrument

			self.client = Instrument()

		else:
			print(address)
			self.client = xmlrpc.client.ServerProxy(address)


		for key, value in self.techniques.items():
		 	#print(technique)

		 	updated = self.techniques[key] 	
		 	updated.client = self.client

		 	value.client = self.client
