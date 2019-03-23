from comtypes.gen import TEMScripting
from stemDetectors import STEMDetectors
from enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np

class Illumination():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._illum = instrument.Illumination

    def rotationCenter(self):


        if value is None:
            return self._illum.RotationCenter
        else:
            self._illum.RotationCenter = vector(self._instrument, value)




    def mode(self, value=None):
        if value is None:
            return self._illum.mode
        else:
            self._illum.Mode = value

    def dfMode(self, value=None):
        if value is None:
            return self._illum.DFMode
        else:
            self._illum.DFMode = value

    def isBeamBlanked(self, value=None):
        if value is None:
            return self._illum.BeamBlanked
        elif type(value) is bool:
            self._illum.BeamBlanked = value


    def condenserStigmator(self):
        if value is None:
            return self._illum.CondenserStigmator
        else:
            self._illum.CondenserStigmator = vector(self._instrument, value)

    def spotSizeIndex(self, value=None):
        if value is None:
            return self._illum.SpotSizeIndex
        else:
            self._illum.SpotSizeIndex = int(value)


    def intensity(self, value=None):
        if value is None:
            return self._illum.Intensity
        else:
            self._illum.Intensity = value

    def c3ImageDistanceParallelOffset(self, value=None):
        if value is None:
            return self._illum.C3ImageDistanceParallelOffset
        else:
            self._illum.C3ImageDistanceParallelOffset = value


    def isIntensityZoomEnabled(self, value=None):
        if value is None:
            return self._illum.IntensityZoomEnabled
        elif type(value) is bool:
            self._illum.IntensityZoomEnabled = value
        pass

    def isIntensityLimitEnabled(self, value=None):
        if value is None:
            return self._illum.IntensityLimitEnabled
        elif type(value) is bool:
            self._illum.IntensityLimitEnabled = value

    def shift(self):
        if value is None:
            return self._illum.Shift
        else:
            self._illum.Shift = vector(self._instrument, value)

    def stemRotation(self, value=None):
        if value is None:
            return self._illum.StemRotation * 180/np.pi
        else:
            self._illum.StemRotation = value * np.pi/180

    def stemMagnification(self, value=None):

        if value is None:
            return self._illum.StemMagnification
        else:
            self._illum.StemMagnification = value

    def tilt(self):
        if value is None:
            return self._illum.Tilt
        else:
            self._illum.Tilt = vector(self._instrument, value)

    def condenserMode(self, value=None):

        if value is None:
            return self._illum.CondenserMode
        else:
            self._illum.CondenserMode = value

    def illuminatedArea(self, value=None):

        if value is None:
            return self._illum.IlluminatedArea
        else:
            self._illum.IlluminatedArea = value

    def probeDefocus(self):
        """
        Not clear this is actually doing anything

        Probably use projection.defocus instead (objective lens)

        """
        return self._illum.ProbeDefocus


    def convergenceAngle(self):
        """
        Not clear this is actually doing anything

        """
        return self._illum.ConvergenceAngle
