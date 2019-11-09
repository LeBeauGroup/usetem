from useTEM.pluginTypes import ITechniquePlugin
import logging

import os
import json
path = os.path.dirname(os.path.realpath(__file__))


class IOpticsControl(ITechniquePlugin):

	client = None
	controlPlugins = None
	
	def __init__(self):

		super(IOpticsControl, self).__init__()
		self.cameraLengths = None

		try:
			with open(path + '/calibrations/cameraLengths.cal', 'r') as filehandle:
				self.cameraLengths = json.load(filehandle)
		except:
			print('calibrations not loaded, need to run init')


	# load up camera lengths and magnifications

	def magnification(self, value=None):

		instrument = self.client
		illumination = instrument.illumination

		return illumination.stemMagnification(value)

	def cameraLength(self, value=None):

		instrument = self.client
		projection = instrument.projection

		if self.cameraLengths is None:
			clIndex = 1
			clValue = 0.0

			clList = list()

			while True:

				projection.cameraLengthIndex(clIndex)
				newClValue = projection.cameraLength(clIndex)

				if newClValue <= clValue:
					break
				else:
					clValue = newClValue

				clDict = {'index': clIndex, 'length':int(clValue*1000)}
				clList.append(clDict)
				clIndex += 1

			with open(path+'/calibrations/cameraLengths.cal', 'w') as filehandle:
				json.dump(clList, filehandle, indent=4)
		else:
			selectedCl = int(value)

			for ind, cl in enumerate(self.cameraLengths):

				if ind == 0:
					runningDiff = abs(cl['length'] - selectedCl)
					newDiff = runningDiff
				else:
					newDiff = abs(cl['length'] - selectedCl)

				if newDiff > runningDiff:
					lowIndex = self.cameraLengths[ind-1]['index']
					projection.cameraLengthIndex(lowIndex)
					break

				runningDiff = newDiff

		return value


