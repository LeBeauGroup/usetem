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
