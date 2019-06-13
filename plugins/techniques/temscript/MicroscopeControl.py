from useTEM.pluginTypes import ITechniquePlugin
import abc
#import matplotlib.pyplot as plt
import numpy as np
import pickle

class IMicroscopeControl(ITechniquePlugin):

	client = None


	def setupAcquisition(self, detectorInfo):
		pass
