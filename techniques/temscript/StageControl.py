from useTEM.pluginTypes import ITechniquePlugin
import logging

import os
import json
path = os.path.dirname(os.path.realpath(__file__))


class IStageControl(ITechniquePlugin):

	client = None
	controlPlugins = None
	
	def __init__(self):

		super(IStageControl, self).__init__()


	def goto(self, position, speed = None):
		instrument = self.client
		stage = instrument.stage

		stage.gotoWithSpeed(position, speed)





