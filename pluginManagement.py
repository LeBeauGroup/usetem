
from yapsy.PluginManager import PluginManager

import pluginTypes
import os

path = os.path.dirname(os.path.abspath(__file__))

def startupExtensions(pluginManager):

	plugins = dict()

	for pluginInfo in pluginManager.getPluginsOfCategory('Extension'):

		pluginManager.activatePluginByName(pluginInfo.name)

		plugin = pluginInfo.plugin_object
		plugin.name = pluginInfo.name

		print('finished loading:' + pluginInfo.name)
		plugins[pluginInfo.name] = plugin

	return plugins

def startupInterfaces(pluginManager):

	plugins = dict()

	for pluginInfo in pluginManager.getPluginsOfCategory('Interface'):

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

		techniquesPath = path+'\\techniques\\'+pluginInfo.name

		plugin.loadTechniques(techniquesPath, plugins)
		plugin.start_connection(connectionAddress)

		print('finished loading:' + pluginInfo.name)
		plugins[pluginInfo.name] = plugin

	return plugins

def availableInterfaces():
	# setup the categories

	categories = {'Interface': pluginTypes.IInterfacePlugin, 'Techniques':pluginTypes.ITechniquePlugin}

	# Build the manager, set load location, and then collect them

	interfaceManager = PluginManager(categories_filter=categories)
	# pluginManager.setPluginPlaces()

	loc = interfaceManager.getPluginLocator()
	loc.setPluginPlaces([path + '\\interfaces'])

	interfaceManager.locatePlugins()
	interfaceManager.loadPlugins()

	interfaces = startupInterfaces(interfaceManager)

	return interfaces


def availableExtensions():

	# setup the categories

	categories = {'Extension': pluginTypes.IExtensionPlugin}


	# Build the manager, set load location, and then collect them

	extManager = PluginManager(categories_filter=categories)
	#pluginManager.setPluginPlaces()

	loc = extManager.getPluginLocator()
	loc.setPluginPlaces([path+'\\extensions'])

	extManager.locatePlugins()
	extManager.loadPlugins()


	extensions = startupExtensions(extManager)



	return extensions
