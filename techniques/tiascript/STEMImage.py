from useTEM.pluginTypes import ITechniquePlugin


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
		detectorInfo = {'dwellTime': 2e-6, 'binning':4, 'numFrames':1,'detectors':['HAADF','BF']}

		:return:
		"""
		binning = detectorInfo['binning']

		pixelSkipping = 1
		maxSizeX = 4096

		sizeX = maxSizeX/1

		if isinstance(binning,str):

			splitBinSize = binning.split('x')
			frameWidth = int(splitBinSize[0])
			frameHeight = int(splitBinSize[1])
		elif isinstance(binning, int):
			frameWidth = maxSizeX / binning  # detectorInfo['frameWidth']
			frameHeight = maxSizeX / binning  # detectorInfo['frameHeight']

		acq = self.client.acquisitionManager
		scanning = self.client.scanningServer

		if acq.isAcquiring():
			acq.stop()

		newWindow = self.client.addDisplayWindow()
		self.client.activateDisplayWindow(newWindow)

		if not acq.doesSetupExist('Acquire'):
			acq.addSetup('Acquire')

		acq.selectSetup('Acquire')
		acq.unlinkAllSignals()


		for name in detectorInfo['detectors']:

			path = self.client.addDisplay(newWindow, name)
			cal = (0, 0, 2, 2, frameWidth/2, frameHeight/2)
			imagePath = self.client.imageDisplay.addImage(path, name, frameWidth, frameHeight, cal)

			try:
				acq.linkSignal(self.signalTable[name], imagePath)
			except:
				print(f'could not set detector named {self.signalTable[name]}')
				continue

		scanRange = scanning.getTotalScanRange()
		resolution = (scanRange[2]-scanRange[0])/(frameWidth)

		scanning.scanResolution(pixelSkipping*resolution)


		scanning.scanRange(scanRange)
		scanning.dwellTime(detectorInfo['dwellTime'])
		scanning.scanMode(2) # Set to frame mode
		scanning.acquireMode(1) # Need to set into single mode if going to use acquire()

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
