
from yapsy.PluginManager import PluginManager
import useTEM.pluginTypes as types
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

		print(connectionAddress)

		techniquesPath = path+'/plugins/techniques/'+pluginInfo.name
		print(techniquesPath)

		plugin.loadTechniques(techniquesPath)
		plugin.start_connection(connectionAddress)

		plugins[pluginInfo.name] = plugin

	return plugins

def availablePlugins():

	# setup the categories
	
	categories = {'Control' : types.IControlPlugin,
   		'Technique' : types.ITechniquePlugin}


	# Build the manager, set load location, and then collect them

	pluginManager = PluginManager(categories_filter=categories)
	pluginManager.setPluginPlaces([path+'/plugins'])


	#ip = 'http://172.16.181.144:8001/'
	ip = 'http://localhost:8001/'


	pluginManager.locatePlugins()
	pluginManager.loadPlugins()

	return startupPlugins(pluginManager)


