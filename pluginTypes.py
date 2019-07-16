import yapsy.IPlugin as plugin

from yapsy.PluginManager import PluginManager

class ITechniquePlugin(plugin.IPlugin):
	pass

class IControlPlugin(plugin.IPlugin):

	def loadTechniques(self,techniquesPath):

		categories = {'Control' : IControlPlugin,
   		'Technique' : ITechniquePlugin}
		# Build the manager, set load location, and then collect them

		pm = PluginManager()
		pm.updatePluginPlaces([techniquesPath])
		pm.collectPlugins()

		#print(pm.getAllPlugins())
		#getPluginsOfCategory('Technique')

		self.techniques = dict()

		for pluginInfo in pm.getAllPlugins():
			print('loading '+ pluginInfo.name + ' for: ' + self.name)
			# Get the object and store in dictionary

			self.techniques[pluginInfo.name] = pluginInfo.plugin_object


class IWorkflow(plugin.IPlugin):
	pass