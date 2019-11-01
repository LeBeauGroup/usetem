from yapsy.MultiprocessPluginManager import MultiprocessPluginManager
import numpy as np
#import pluginManagement as plugm

import yapsy.IPlugin as IPlugin
import pluginTypes as types

import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean

import logging
import os
path = os.path.dirname(os.path.abspath(__file__))

# def startupPlugins(pluginManager):

# 	plugins = dict()

# 	for pluginInfo in pluginManager.getPluginsOfCategory('Control'):

# 		pluginManager.activatePluginByName(pluginInfo.name)

# 		address = pluginInfo.details['Documentation']['ServerAddress']
# 		port = pluginInfo.details['Documentation']['Port']
# 		prefix = pluginInfo.details['Documentation']['ServerPrefix']

# 		plugin = pluginInfo.plugin_object

# 		if address == 'local':
# 			connectionAddress = 'local'

# 		else:
# 			connectionAddress = 'http://'+address+':'+port+'/'+prefix

# 		print(connectionAddress)

# 		techniquesPath = path+'/plugins/techniques/'+pluginInfo.name
# 		print(techniquesPath)

# 		plugin.loadTechniques(techniquesPath)
# 		plugin.start_connection(connectionAddress)

# 		plugins[pluginInfo.name] = plugin

# 	return plugins

if __name__ == '__main__':

	# categories = {'Control' : types.IControlPlugin,
 #   		'Technique' : types.ITechniquePlugin}

	# # Build the manager, set load location, and then collect them

	pluginManager = MultiprocessPluginManager()
	pluginManager.setPluginPlaces([path+'/interfaces'])


	# #ip = 'http://172.16.181.144:8001/'
	# ip = 'http://localhost:8001/'

	# # setup for later calling from


	# # Activate all loaded plugins
	pluginManager.locatePlugins()


	 # pluginManager.locatePlugins()
	pluginManager.loadPlugins()

	print(pluginManager)

	for pluginInfo in pluginManager.getAllPlugins():
		plugin = pluginInfo.plugin_object
		plugin.name = pluginInfo.name
		print(plugin.child_pipe)

		print(plugin.child_pipe.recv())

	# plugins = pluginManager.availablePlugins()

	#
	#
	# im = [None]*10
	# for i in range(10):
	#
	# 	rot = i*90
	# 	plugins['temscript'].techniques['STEMImage'].scanRotation(rot)
	# 	im[i] = plugins['temscript'].techniques['STEMImage'].acquire()

	# save file here
