from useTEM.pluginTypes import ITechniquePlugin
import abc
#import matplotlib.pyplot as plt
import numpy as np
import pickle

class ISTEMImage(ITechniquePlugin):

	client = None
	controlPlugins = None

	signalTable = {'HAADF': 'Analog3', 'BF': 'Analog1', 'DF2': 'Analog4', 'DF4': 'Analog2'}

	def scanRotation(self, angle):

		try:
			t = self.controlPlugins['temscript'].client
			t.illumination.stemRotation(angle)
		except:
			print('TIA script cannot change rotation scan, temscript must be available')

	def setupAcquisition(self, detectorInfo):
		"""

		:param detectorInfo: dictionary with following information:
		detectorInfo = {'dwellTime': 2e-6, 'binning':4, 'numFrames':1,'names':['HAADF','BF']}

		:return:
		"""

		binning = detectorInfo['binning']
		pixelSkipping = 1
		maxSizeX = 4096

		sizeX = maxSizeX/1

		acq = self.client.acquisitionManager
		scanning = self.client.scanningServer

		newWindow = self.client.addDisplayWindow()
		self.client.activateDisplayWindow(newWindow)

		imagePaths = []

		frameWidth = maxSizeX/binning # detectorInfo['frameWidth']
		frameHeight = maxSizeX/binning #detectorInfo['frameHeight']

		acq.unlinkAllSignals()

		scanning.acquireMode(1) # Need to set into single mode if going to use acquire()
		scanning.scanMode(2) # Set to frame mode

		if acq.doesSetupExist('Acquire'):
			acq.deleteSetup('Acquire')
			print('deleted acquire')

		acq.addSetup('Acquire')
		acq.selectSetup('Acquire')

		for name in detectorInfo['names']:

			path = self.client.addDisplay(newWindow, name)
			cal = (0, 0, 1, 1, frameWidth/2, frameHeight/2)
			imagePath = self.client.imageDisplay.addImage(path, name, frameWidth, frameHeight, cal)
			acq.linkSignal(self.signalTable[name], imagePath)

		scanning.dwellTime(detectorInfo['dwellTime'])
		scanRange = scanning.getTotalScanRange()

		print(scanRange)
		resolution = (scanRange[2]-scanRange[0])/(frameWidth)

		print(resolution)

		scanning.scanResolution(pixelSkipping*resolution)

		rangeX = maxSizeX/1
		rangeY = maxSizeX/1


		xrange = rangeX * ((pixelSkipping * (scanRange[2]-scanRange[0]) / maxSizeX) / 2)
		yrange = rangeY * ((pixelSkipping * (scanRange[3]-scanRange[1]) / maxSizeX) / 2)

		range = (-xrange, -yrange, xrange, yrange)
		print(range)

		scanning.scanRange(range)

		print(scanning.scanResolution())
		scanning.scanRange(scanRange)
		scanning.seriesSize(detectorInfo['numFrames'])

	def subscan(self,rect):
		pass

	def preview(self):
		pass


	def acquire(self):

		acq = self.client.acquisitionManager
		try:
			acq.acquire()
		except:
			print('could not acquire')


		#capturedImage = pickle.loads(acq.acquireImages().data)[0]
		return None

	# def acquireSeries(self, numFrames):
	#
	#
	# 	acq = self.client.acquisition
	# 	stem = acq.stemDetectors
	#
	# 	stem.binning(8)
	# 	stem.dwellTime(0.5e-6)
	#
	# 	# for i in range(stem.count()):
	# 	# 	dets = stem.item(i)
	#
	# 	acq.addDetectorByName('HAADF')
	# 	stem.imageSize(0)
	#
	# 	for _ in range(numFrames):
	#
	# 		print('start')
	# 		im = pickle.loads(acq.acquireImages().data)[0]
	# 		# plt.imshow(im)
	# 		# plt.show()
	# 		print('stop')
	#
	# 	print('acquiring')
