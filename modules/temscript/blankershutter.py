from comtypes.gen import TEMScripting
from stemDetectors import STEMDetectors
from enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
from utilities import *

class BeamShutter():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._bs = instrument.BeamShutter

    def isShutterOverrideOn(self, value=None):
        if value is None:
            return self._bs.ShutterOverrideOn
        elif type(value) is bool:
            self._bs.ShutterOverrideOn = value
