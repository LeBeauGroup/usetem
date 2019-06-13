import useTEM.pluginTypes as pluginTypes
import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean
import os
from yapsy.PluginManager import PluginManager


class ITIAscriptPlugin(pluginTypes.IControlPlugin):

	client = None # server proxy or direct local comtypes
	name = None
	moduleName = 'useTEM.modules.tiascript.application'

	techniques = dict()

	def loadTechniques(self,techniquesPath):

		categories = {'Control' : pluginTypes.IControlPlugin,
   		'Technique' : pluginTypes.ITechniquePlugin}
		# Build the manager, set load location, and then collect them

		pm = PluginManager()
		pm.updatePluginPlaces([techniquesPath])
		pm.collectPlugins()

		#print(pm.getAllPlugins())
		#getPluginsOfCategory('Technique')

		for pluginInfo in pm.getAllPlugins():
			print('loading '+ pluginInfo.name + ' for: ' + self.name)
			# Get the object and store in dictionary

			self.techniques[pluginInfo.name] = pluginInfo.plugin_object

	def activate(self):
		print('activating')

	def	start_connection(self, address):
		techniques_path = os.path.dirname(os.path.abspath(__file__))+'\\techniques\\'+self.name

		if address == 'local':
			import importlib

			module = importlib.import_module(self.moduleName)
			self.client = module.Application()

		else:
			print(address)
			self.client = xmlrpc.client.ServerProxy(address)

		for key, value in self.techniques.items():
		 	#print(technique)
			print('This is a key:' + key)

			updated = self.techniques[key]
			updated.client = self.client
			value.client = self.client
