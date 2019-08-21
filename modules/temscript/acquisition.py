from comtypes.gen import TEMScripting

from .stemDetectors import STEMDetectors
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import pickle
import numpy as np
from xmlrpc.client import Binary

import logging

logging.basicConfig(level=logging.INFO)
class Acquisition():

    _instrument = None
    stemDetectors = None
    ccdCameras = None

    def __init__(self, instrument):
        self._instrument = instrument
        self._acq = instrument.Acquisition
        self.stemDetectors = STEMDetectors(self._acq.Detectors)
#        self.ccdDetectors = CCDCameras(self._acq.Cameras)

    def addCameraByName(self, name):
        self._acq.AddAcqDeviceByName(name)

    def addDetectorByName(self, name):
        self._acq.AddAcqDeviceByName(name)

    def removeAcqDeviceByName(self, name):
        self._acq.RemoveAcqDeviceByName(name)

    def removeAllAcqDevices(self):
        self._acq.RemoveAllAcqDevices()

    def acquireImages(self):
        images = self._acq.AcquireImages()

        outImages = list()

        for image in images:

            with safearray_as_ndarray:
                converted = image.AsSafeArray

            outImages.append(converted)

        return Binary(pickle.dumps(outImages))


    #def ccdCameras(self):


    # def stemDetectors(self):
    #
    #     dets = STEMDetectors(self._acq.Detectors)
    #
    #     detectors = dict()
    #
    #     detectors['dwellTime'] = dets.dwellTime()
    #     detectorInfo = list()
    #
    #     for i in range(dets.count()):
    #         det = dets.item(i)
    #         detectorInfo.append(det)
    #
    #     detectors['info'] = detectorInfo
    #
    #     return dets

    def imageSize(self, imageSize = None):

        params = self._acq.AcqParams

        if value is None:
            return params.ImageSize
        else:
            params.ImageSize = imageSize.value
