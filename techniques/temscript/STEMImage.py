from useTEM.pluginTypes import ITechniquePlugin
import abc
#import matplotlib.pyplot as plt
import numpy as np
import pickle

class ISTEMImage(ITechniquePlugin):

	client = None


	def setupAcquisition(self, detectorInfo):

		acq = self.client.acquisition
		stem = acq.stemDetectors
	

		for name in detectorInfo['names']:
			acq.addDetectorByName('HAADF')

		stem.binning(detectorInfo['binning'])
		stem.dwellTime(detectorInfo['dwellTime'])
		stem.imageSize(detectorInfo['imageSize'])

	def scanRotation(self,value):

		self.client.illumination.stemRotation(value)



	def acquire(self):

		acq = self.client.acquisition
				
		capturedImage = pickle.loads(acq.acquireImages().data)[0]
		
		return capturedImage

	def acquireSeries(self,numFrames):


		acq = self.client.acquisition
		stem = acq.stemDetectors

		stem.binning(8)
		stem.dwellTime(0.5e-6)
		
		# for i in range(stem.count()):
		# 	dets = stem.item(i)

		acq.addDetectorByName('HAADF')
		stem.imageSize(0)



		for _ in range(numFrames):
		
			print('start')				
			im = pickle.loads(acq.acquireImages().data)[0]
			# plt.imshow(im)
			# plt.show()
			print('stop')
		
		


		print('acquiring')
