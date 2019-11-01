import yapsy.IPlugin as plugin

from yapsy.PluginManager import PluginManager

class ITechniquePlugin(plugin.IPlugin):
	pass

class IExtensionPlugin(plugin.IPlugin):
	pass

# categories = {'Control' : IInterfacePlugin,
#    		'Technique' : ITechniquePlugin, 'Extension':IExtensionPlugin}

class IInterfacePlugin(plugin.IPlugin):

	def loadTechniques(self,techniquesPath, controls=None):


		# Build the manager, set load location, and then collect them

		pm = PluginManager()
		pm.updatePluginPlaces([techniquesPath])
		pm.collectPlugins()

		self.techniques = dict()

		for pluginInfo in pm.getAllPlugins():
			print('loading '+ pluginInfo.name + ' for: ' + self.name)
			# Get the object and store in dictionary

			self.techniques[pluginInfo.name] = pluginInfo.plugin_object
			self.techniques[pluginInfo.name].controlPlugins = controls


class IWorkflow(plugin.IPlugin):
	pass
