from yapsy.PluginManager import PluginManager
import numpy as np
import useTEM.pluginManagement as plugm

import yapsy.IPlugin as IPlugin
#import useTEM.pluginTypes as types

import xmlrpc.client
from xmlrpc.client import MultiCall, Boolean

import logging
import os
path = os.path.dirname(os.path.abspath(__file__))


if __name__ == '__main__':


	plugins = plugm.availablePlugins()

	#print(plugins['temscript'].techniques)
	tia = plugins['tiascript']
	stem = tia.techniques['STEMImage']
	numFrames = 12

	im = [None]*numFrames

	detectorInfo = {'dwellTime': 0.5e-6, 'binning':8, 'numFrames':numFrames,'names':['DF2','BF']}

	stem.setupAcquisition(detectorInfo)

	for i in range(numFrames):
		rot = i*90
		plugins['tiascript'].techniques['STEMImage'].scanRotation(rot)
		im[i] = stem.acquire()

