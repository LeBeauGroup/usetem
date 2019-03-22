from comtypes.gen import TEMScripting
from stemDetectors import STEMDetectors
from enums import *
from comtypes.safearray import safearray_as_ndarray

class Acquisition():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._acq = instrument.Acquisition

    def addDetectorByName(self, name):
        self._acq.AddAcqDeviceByName(name)


    def acquireImages(self):
        images = self._acq.AcquireImages()

        outImages = list()

        for image in images:
            with safearray_as_ndarray:
                converted = image.AsSafeArray

            outImages.append(converted)

        return outImages


    def ccdCameras(self):
        camObjs = self._acq.Cameras

    @property
    def stemDetectors(self):

        dets = STEMDetectors(self._acq.Detectors)

        # detObjs = self._acq.Detectors
        #
        # dets = list()
        #
        # for det in detObjs:
        #     converted = STEMDetector(det)
        #     dets.append(converted)

        return dets

    def imageSize(self, imageSize = None):

        params = self._acq.AcqParams

        if value is None:
            return params.ImageSize
        else:
            params.ImageSize = imageSize.value
