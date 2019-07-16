from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
from .utilities import *

class Gun():

    _instrument = None

    def __init__(self, instrument):
        self._instrument = instrument
        self._gun = instrument.Gun

    def tilt(self, value=None):

        if value is None:
            return self._gun.Tilt
        else:
            self._gun.Tilt = vector(self._instrument, value)


    def shift(self, value=None):

        if value is None:
            return self._gun.Shift
        else:
            self._gun.Shift = vector(self._instrument, value)

    def htState(self, value=None):

        if value is None:
            return self._gun.HTState
        else:
            self._gun.HTState = value

    def htValue(self, value=None):

        if value is None:
            return self._gun.HTValue
        else:
            self._gun.HTValue = value

    def htMaxValue(self):
        return self._gun.HTMaxValue
