
from comtypes.safearray import safearray_as_ndarray

from .stemDetector import STEMDetector

class STEMDetectors():

    def __init__(self, detectors):

        self._detectors = detectors

    def imageSize(self, imgSize=None):

        if imgSize is None:
            return self._detectors.AcqParams.ImageSize
        else:
            self._detectors.AcqParams.ImageSize = imgSize

    def dwellTime(self, value=None):

        if value is None:
            return self._detectors.AcqParams.DwellTime
        else:
            self._detectors.AcqParams.DwellTime = value

    def setFrameSize(self, frameSize):

        self.binning(frameSize.value)

    def setMaxFrameSize(self, frameSize):

        self.imageSize(frameSize.value)

    def binning(self, value=None):

        if value is None:
            return self._detectors.AcqParams.Binning
        else:
            self._detectors.AcqParams.Binning = value

    def item(self, index):
        selectedDet = self._detectors.Item(index)

        converted = dict()
        converted['index'] = index
        converted['name'] = selectedDet.Info.Name
        converted['brightness'] = selectedDet.Info.Brightness
        converted['contrast'] = selectedDet.Info.Contrast

        with safearray_as_ndarray:
            binnings = selectedDet.Info.Binnings

        converted['binnings'] = binnings.tolist()

        return converted


    # def acqParams():
    #
    #     return self._detectors.AcqParams

    def count(self):
        return self._detectors.Count
