import useTEM.pluginTypes as pluginTypes
import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
import os
from yapsy.PluginManager import PluginManager


class ITEMscriptPlugin(pluginTypes.IInterfacePlugin):

	client = None # server proxy or direct local comtypes
	name = None
	moduleName = 'useTEM.modules.temscript.instrument'

	def activate(self):
		print('activating')

	def	start_connection(self, address):

		if address == 'local':
			import importlib

			module = importlib.import_module(self.moduleName)
			self.client = module.Instrument()

		else:
			self.client = xmlrpc.client.ServerProxy(address)

		for key, value in self.techniques.items():
			updated = self.techniques[key]
			updated.client = self.client
			value.client = self.client
