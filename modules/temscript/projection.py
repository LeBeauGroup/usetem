from comtypes.gen import TEMScripting
from stemDetectors import STEMDetectors
from enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging

class Projection():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._proj = instrument.Projection

    def mode(self, value=None):
        pass

    def subMode(self):
        pass

    def subModeString(self):
        pass

    def lensProgram(self, value=None):
        pass

    def magnification(self, value=None):
        pass

    def magnificationIndex(self,value):
        pass

    def imageRotation(self):
        pass

    def detectorShift(self, value=None):
        pass

    def detectorShiftMode(self, value=None):
        pass
