from useTEM.pluginTypes import ITechniquePlugin
import logging
import abc
# import matplotlib.pyplot as plt
import numpy as np
import pickle


class IOpticsControl(ITechniquePlugin):

	client = None
	controlPlugins = None

	def magnification(self, value=None):

		instrument = self.client
		illumination = instrument.illumination

		return illumination.stemMagnification(value)


