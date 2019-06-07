from yapsy.PluginManager import PluginManager
import numpy as np

import yapsy.IPlugin as IPlugin
import useTEM.pluginTypes as types

import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean

import logging
import os
path = os.path.dirname(os.path.abspath(__file__))



if __name__ == '__main__':

	categories = {'Control' : types.IControlPlugin,
   		'Technique' : types.ITechniquePlugin}


	# Build the manager, set load location, and then collect them

	pluginManager = PluginManager(categories_filter=categories)
	pluginManager.setPluginPlaces([path+'/plugins'])


	#ip = 'http://172.16.181.144:8001/'
	ip = 'http://localhost:8001/'

	# setup for later calling from
	plugins = dict()

	# Activate all loaded plugins
	#pluginManager.locatePlugins()
	#print(pluginManager.getPluginCandidates())

	pluginManager.locatePlugins()
	pluginManager.loadPlugins()


	for pluginInfo in pluginManager.getPluginsOfCategory('Control'):
				
		pluginManager.activatePluginByName(pluginInfo.name)

		address = pluginInfo.details['Documentation']['ServerAddress']
		port = pluginInfo.details['Documentation']['Port']
		prefix = pluginInfo.details['Documentation']['ServerPrefix']

		plugin = pluginInfo.plugin_object

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

	plugins['temscript'].techniques['STEMImage'].acquire()
