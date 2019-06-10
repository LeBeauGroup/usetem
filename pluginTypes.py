from yapsy.IPlugin import IPlugin
from yapsy.PluginManager import PluginManager


class ITechniquePlugin(IPlugin):
	pass

class IControlPlugin(IPlugin):
	
	techniques = dict()
	
	def loadTechniques(self,techniquesPath):
		
		categories = {'Control' : IControlPlugin,
   		'Technique' : ITechniquePlugin}
		# Build the manager, set load location, and then collect them

		pluginManager = PluginManager(categories_filter=categories)
		pluginManager.setPluginPlaces([techniquesPath])

		pluginManager.locatePlugins()
		pluginManager.loadPlugins()

		for pluginInfo in pluginManager.getPluginsOfCategory('Technique'):	

			# Get the object and store in dictionary
			self.techniques[pluginInfo.name] = pluginInfo.plugin_object
			print(pluginInfo.name)
			

class IWorkflow(IPlugin):
	pass