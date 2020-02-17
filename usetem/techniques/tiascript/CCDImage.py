from usetem.pluginTypes import ITechniquePlugin
import pickle
import numpy as np

class ICCDImage(ITechniquePlugin):

	client = None
	controlPlugins = None

	#signalTable = {'HAADF': 'Analog3', 'BF': 'Analog1', 'DF2': 'Analog4', 'DF4': 'Analog2'}

	def __init__(self):
		super(ICCDImage, self).__init__()
		self.imagePaths = []

	def availableCameras(self):

		try:
			ccds = self.client.ccdServer.cameraNames()
			print(ccds)
		except Exception as e:
			print(e)
			ccds = ['None']

		return ccds


	def _frameSize(self,binning):

		maxSizeX = 4096

		if isinstance(binning,str):

			splitBinSize = binning.split('x')
			frameWidth = int(splitBinSize[0])
			frameHeight = int(splitBinSize[1])
		elif isinstance(binning, int):
			frameWidth = maxSizeX / binning  # detectorInfo['frameWidth']
			frameHeight = maxSizeX / binning  # detectorInfo['frameHeight']

		return (frameWidth, frameHeight)

	def isAcquiring(self):
		acq = self.client.acquisitionManager

		return acq.isAcquiring()

	def setupFocus(self, parameters):

		frame = self._frameSize(parameters['binning'])

		acq = self.client.acquisitionManager
		scanning = self.client.scanningServer

		if acq.isAcquiring():
			acq.stop()

		focusName = 'Focus'

		try:
			self.client.activateDisplayWindow(focusName)
		except Exception as e:
			self.client.addDisplayWindow(focusName)


		if not acq.doesSetupExist(focusName):
			acq.addSetup(focusName)

		acq.selectSetup(focusName)
		acq.unlinkAllSignals()


		self.imagePaths = 4*[None]
		cal = (0, 0, 2, 2, frame[0] / 2, frame[1] / 2)

		self._linkSignals(parameters['detectors'], focusName, frame,cal )

		scanRange = scanning.getTotalScanRange()
		resolution = (scanRange[2] - scanRange[0]) / (frame[0])

		scanning.scanResolution(resolution)

		scanning.scanRange(scanRange)
		scanning.dwellTime(parameters['dwellTime'])
		scanning.scanMode(2)  # Set to frame mode
		scanning.acquireMode(0)  # Need to set into single mode if going to use acquire()


		# newWindow = self.client.addDisplayWindow('Focus')
		# self.client.enableEvents(newWindow)

	def _linkSignals(self, signals, windowName, frame, cal):

		acq = self.client.acquisitionManager

		for ind, name in enumerate(signals):
			path = windowName+'/'+ name + ' Display' + '/'+ name

			if not self.client.containsDisplayObject(path):
				path = self.client.addDisplay(windowName, name)
				imagePath = self.client.imageDisplay.addImage(path, name, frame[0], frame[1], cal)
				self.imagePaths[ind] = imagePath
			else:
				self.imagePaths[ind]  = path
				imagePath = path

			try:
				acq.linkSignal(self.signalTable[name], imagePath)
			except:
				print(f'could not set detector named {self.signalTable[name]}')
				continue


	def setupAcquisition(self, detectorInfo):
		"""

		:param detectorInfo: dictionary with following information:
		detectorInfo = {'integrationTime': 2e-6, 'binning':4, 'numFrames':1,'detectors':['HAADF','BF']}

		:return:
		"""

		binning = detectorInfo['binning']

		maxSizeX = 40961

		frameWidth = maxSizeX / binning  # detectorInfo['frameWidth']
		frameHeight = maxSizeX / binning  # detectorInfo['frameHeight']


		acq = self.client.acquisitionManager
		ccd = self.client.ccdServer

		ccd.integrationTime(detectorInfo['integrationTime'])

		if acq.isAcquiring():
			acq.stop()

		newWindow = self.client.addDisplayWindow()
		self.client.activateDisplayWindow(newWindow)
		self.client.enableEvents(newWindow)

		if not acq.doesSetupExist('Acquire'):
			acq.addSetup('Acquire')

		acq.selectSetup('Acquire')
		acq.unlinkAllSignals()

		self.imagePaths = []

		path = self.client.addDisplay(newWindow, name)
		cal = (0, 0, 2, 2, frameWidth / 2, frameHeight / 2)
		imagePath = self.client.imageDisplay.addImage(path, name, frameWidth, frameHeight, cal)
		acq.linkSignal('CCD', imagePath)

# 	// Declarations
# 	are
# 	skipped
# 	here
# 	FDisplayWindow := FTia.AddDisplayWindow;
# 	FDisplayWindow.Name := 'My displaywindow';
# 	FDisplay := FDisplayWindow.AddDisplay('Acquire CCD Image Display', esImageDisplay, esImageDisplayType,
# 	                                      esSplitRight,
# 	                                      1); // for diffraction patterns use esRecImageDisplayType instead of esImageDisplayType ! ImageSizeX := EndX-StartX; // Make sure all parameters fit, get from CcdServer.GetTotalPixelReadoutRange ImageSizeY := EndY-StartY;
# 	FImage := FDisplay.AddImage('Acquire CCD Image', ImageSizeX, ImageSizeY, FTia.Calibration2D(0, 0, 2, 2, 256, 256));
# 	if FTia.AcquisitionManager.IsAcquiring then FTia.AcquisitionManager.Stop; // should check that stop worked ! if not FTia.AcquisitionManager.DoesSetupExist('MySetupName') then // this setup stuff is necessary
# 	FTia.AcquisitionManager.AddSetup('MySetupName');
# 	FTia.AcquisitionManager.SelectSetup('MySetupName');
# 	FTia.AcquisitionManager.UnlinkAllSignals;
# 	FTia.AcquisitionManager.LinkSignal('CCD', FImage); // "CCD" is generic, independent
# 	of
# 	the
# 	actual
# 	CCD
# 	name FTia.CcdServer.IntegrationTime := Time;
# 	FTia.CcdServer.Binning := Binning;
# 	FTia.CcdServer.PixelReadOutRange := FTia.Range2D(StartX * Bin, StartY * Bin, EndX * Bin,
# 	                                                 EndY * Bin); if FTia.CcdServer.IsCameraRetractable then
# 	begin
# 	if not FTia.CcdServer.CameraInserted then begin
# 	FTia.CcdServer.CameraInserted := true;
# 	Sleep(5000); // have
# 	to
# 	wait
# 	until
# 	it is in
#
#
# end;
# end;
# FTia.CcdServer.AcquireMode := esSingleAcquire;
# if not VarIsEmpty(FTia.ScanningServer) then FTia.ScanningServer.ScanMode := esSpotMode;
# // important: check
# on
# ScanningServer.If
# the
# system is not a
# STEM, Scanningserver
# does
# not exist // also
# for CCD must be in SpotMode
# FTia.AcquisitionManager.Start; // now
# wait
# until
# image is in.
# // Either
# monitor
# AcquisitionManager.IsAcquiring or use
# acquisition
# events


	def subscan(self,rect):
		pass

	def preview(self):
		pass

	def start(self):

		self.client.acquisitionManager.start()

	def stop(self):
		self.client.acquisitionManager.stop()

	def acquire(self, returnsImage=False):

		acq = self.client.acquisitionManager

		try:
			print(self.imagePaths[0])

			if returnsImage is True:
				im = acq.acquire(returnsImage,self.imagePaths[0])
				return pickle.loads(im.data)
			else:
				acq.acquire()

		except Exception as e:
			print(e)
			print('could not acquire')

		#capturedImage = pickle.loads(acq.acquireImages().data)[0]
		return None

	def variance(self):

		procsys = self.client.processingSystem

		return procsys.variance(self.imagePaths[0])

	def stdev(self):

		procsys = self.client.processingSystem

		return np.sqrt(procsys.variance(self.imagePaths[0]))

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
