from useTEM.pluginTypes import ITechniquePlugin
import pickle
import numpy as np

class ISTEMImage(ITechniquePlugin):

	client = None


	def scanRotation(self, angle):

		try:
			t = self.controlPlugins['temscript'].client
			t.illumination.stemRotation(angle)
		except:
			print('Velox script cannot change rotation scan, temscript must be available')

	# def _frameSize(self,binning):
	#
	# 	maxSizeX = 4096
	#
	# 	if isinstance(binning,str):
	#
	# 		splitBinSize = binning.split('x')
	# 		frameWidth = int(splitBinSize[0])
	# 		frameHeight = int(splitBinSize[1])
	# 	elif isinstance(binning, int):
	# 		frameWidth = maxSizeX / binning  # detectorInfo['frameWidth']
	# 		frameHeight = maxSizeX / binning  # detectorInfo['frameHeight']
	#
	# 	return (frameWidth, frameHeight)
	#
	# def isScanning(self):
	# 	acq = self.client.acquisitionManager
	#
	# 	return acq.isAcquiring()
	#
	# def setupFocus(self, parameters):
	#
	# 	frame = self._frameSize(parameters['binning'])
	#
	# 	acq = self.client.acquisitionManager
	# 	scanning = self.client.scanningServer
	#
	# 	if acq.isAcquiring():
	# 		acq.stop()
	#
	# 	focusName = 'Focus'
	#
	# 	try:
	# 		self.client.activateDisplayWindow(focusName)
	# 	except Exception as e:
	# 		self.client.addDisplayWindow(focusName)
	#
	#
	# 	if not acq.doesSetupExist(focusName):
	# 		acq.addSetup(focusName)
	#
	# 	acq.selectSetup(focusName)
	# 	acq.unlinkAllSignals()
	#
	#
	# 	self.imagePaths = 4*[None]
	# 	cal = (0, 0, 2, 2, frame[0] / 2, frame[1] / 2)
	#
	# 	self._linkSignals(parameters['detectors'], focusName, frame,cal )
	#
	# 	scanRange = scanning.getTotalScanRange()
	# 	resolution = (scanRange[2] - scanRange[0]) / (frame[0])
	#
	# 	scanning.scanResolution(resolution)
	#
	# 	scanning.scanRange(scanRange)
	# 	scanning.dwellTime(parameters['dwellTime'])
	# 	scanning.scanMode(2)  # Set to frame mode
	# 	scanning.acquireMode(0)  # Need to set into single mode if going to use acquire()
	#
	#
	# 	# newWindow = self.client.addDisplayWindow('Focus')
	# 	# self.client.enableEvents(newWindow)
	#
	# def _linkSignals(self, signals, windowName, frame, cal):
	#
	# 	acq = self.client.acquisitionManager
	#
	# 	for ind, name in enumerate(signals):
	# 		path = windowName+'/'+ name + ' Display' + '/'+ name
	#
	# 		if not self.client.containsDisplayObject(path):
	# 			path = self.client.addDisplay(windowName, name)
	# 			imagePath = self.client.imageDisplay.addImage(path, name, frame[0], frame[1], cal)
	# 			self.imagePaths[ind] = imagePath
	# 		else:
	# 			self.imagePaths[ind]  = path
	# 			imagePath = path
	#
	# 		try:
	# 			acq.linkSignal(self.signalTable[name], imagePath)
	# 		except:
	# 			print(f'could not set detector named {self.signalTable[name]}')
	# 			continue
	#
	#
	#
	#
	#
	#
	# def setupAcquisition(self, detectorInfo):
	# 	"""
	#
	# 	:param detectorInfo: dictionary with following information:
	# 	detectorInfo = {'dwellTime': 2e-6, 'binning':4, 'numFrames':1,'detectors':['HAADF','BF']}
	#
	# 	:return:
	# 	"""
	# 	binning = detectorInfo['binning']
	#
	# 	pixelSkipping = 1
	# 	maxSizeX = 4096
	#
	# 	sizeX = maxSizeX/1
	#
	# 	if isinstance(binning,str):
	#
	# 		splitBinSize = binning.split('x')
	# 		frameWidth = int(splitBinSize[0])
	# 		frameHeight = int(splitBinSize[1])
	# 	elif isinstance(binning, int):
	# 		frameWidth = maxSizeX / binning  # detectorInfo['frameWidth']
	# 		frameHeight = maxSizeX / binning  # detectorInfo['frameHeight']
	#
	# 	acq = self.client.acquisitionManager
	# 	scanning = self.client.scanningServer
	#
	# 	if acq.isAcquiring():
	# 		acq.stop()
	#
	# 	newWindow = self.client.addDisplayWindow()
	# 	self.client.activateDisplayWindow(newWindow)
	# 	self.client.enableEvents(newWindow)
	#
	# 	if not acq.doesSetupExist('Acquire'):
	# 		acq.addSetup('Acquire')
	#
	# 	acq.selectSetup('Acquire')
	# 	acq.unlinkAllSignals()
	#
	# 	self.imagePaths = []
	#
	# 	for name in detectorInfo['detectors']:
	#
	# 		path = self.client.addDisplay(newWindow, name)
	# 		cal = (0, 0, 2, 2, frameWidth/2, frameHeight/2)
	# 		imagePath = self.client.imageDisplay.addImage(path, name, frameWidth, frameHeight, cal)
	# 		self.imagePaths.append(imagePath)
	#
	# 		try:
	# 			acq.linkSignal(self.signalTable[name], imagePath)
	# 		except:
	# 			print(f'could not set detector named {self.signalTable[name]}')
	# 			continue
	#
	# 	scanRange = scanning.getTotalScanRange()
	# 	resolution = (scanRange[2]-scanRange[0])/(frameWidth)
	#
	# 	scanning.scanResolution(pixelSkipping*resolution)
	#
	#
	# 	scanning.scanRange(scanRange)
	# 	scanning.dwellTime(detectorInfo['dwellTime'])
	# 	scanning.scanMode(2) # Set to frame mode
	# 	scanning.acquireMode(1) # Need to set into single mode if going to use acquire()
	#
	# 	scanning.seriesSize(detectorInfo['numFrames'])
	#
	#
	# def subscan(self,rect):
	# 	pass
	#
	# def preview(self):
	# 	pass
	#
	# def start(self):
	#
	# 	self.client.acquisitionManager.start()
	#
	# def stop(self):
	# 	self.client.acquisitionManager.stop()
	#
	# def acquire(self, returnsImage=False):
	#
	# 	acq = self.client.acquisitionManager
	#
	# 	try:
	# 		print(self.imagePaths[0])
	#
	# 		if returnsImage is True:
	# 			im = acq.acquire(returnsImage,self.imagePaths[0])
	# 			return pickle.loads(im.data)
	# 		else:
	# 			acq.acquire()
	#
	# 	except Exception as e:
	# 		print(e)
	# 		print('could not acquire')
	#
	# 	#capturedImage = pickle.loads(acq.acquireImages().data)[0]
	# 	return None
	#
	# def stdev(self):
	#
	# 	procsys = self.client.processingSystem
	#
	# 	return np.sqrt(procsys.variance(self.imagePaths[0]))
	#
	# # def acquireSeries(self, numFrames):
	# #
	# #
	# # 	acq = self.client.acquisition
	# # 	stem = acq.stemDetectors
	# #
	# # 	stem.binning(8)
	# # 	stem.dwellTime(0.5e-6)
	# #
	# # 	# for i in range(stem.count()):
	# # 	# 	dets = stem.item(i)
	# #
	# # 	acq.addDetectorByName('HAADF')
	# # 	stem.imageSize(0)
	# #
	# # 	for _ in range(numFrames):
	# #
	# # 		print('start')
	# # 		im = pickle.loads(acq.acquireImages().data)[0]
	# # 		# plt.imshow(im)
	# # 		# plt.show()
	# # 		print('stop')
	# #
	# # 	print('acquiring')
