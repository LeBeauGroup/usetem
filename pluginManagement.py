
from yapsy.PluginManager import PluginManager
import pluginTypes
import os
path = os.path.dirname(os.path.abspath(__file__))


def startupPlugins(pluginManager):

	plugins = dict()

	for pluginInfo in pluginManager.getPluginsOfCategory('Control'):

		pluginManager.activatePluginByName(pluginInfo.name)

		address = pluginInfo.details['Documentation']['ServerAddress']
		port = pluginInfo.details['Documentation']['Port']
		prefix = pluginInfo.details['Documentation']['ServerPrefix']

		plugin = pluginInfo.plugin_object
		plugin.name = pluginInfo.name

		if address == 'local':
			connectionAddress = 'local'

		else:
			connectionAddress = 'http://'+address+':'+port+'/'+prefix

		techniquesPath = path+'\\plugins\\techniques\\'+pluginInfo.name

		plugin.loadTechniques(techniquesPath, plugins)
		plugin.start_connection(connectionAddress)

		print('finished loading:' + pluginInfo.name)
		plugins[pluginInfo.name] = plugin

	return plugins

def availablePlugins():

	# setup the categories

	categories = {'Control' : pluginTypes.IControlPlugin,
   		'Technique' : pluginTypes.ITechniquePlugin}


	# Build the manager, set load location, and then collect them

	pluginManager = PluginManager(categories_filter=categories)
	#pluginManager.setPluginPlaces()

	loc = pluginManager.getPluginLocator()
	loc.setPluginPlaces([path+'\\plugins'])

	pluginManager.locatePlugins()
	pluginManager.loadPlugins()


	plugins = startupPlugins(pluginManager)



	return plugins
