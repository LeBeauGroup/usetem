from launch.pluginTypes import ITechniquePlugin
import abc
#import matplotlib.pyplot as plt
import numpy as np
import pickle

class ISTEMControl(ITechniquePlugin):

	client = None

	def scanRotation(self,angle=0):

		print('Velox script cannot change rotation scan, use temscript ')
		pass
