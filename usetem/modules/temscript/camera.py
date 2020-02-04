from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging

class Camera():

    _instrument = None

    def __init__(self, instrument):
        self._instrument = instrument
        self._camera = instrument.Camera

    def mainScreenPosition(self, value=None):

        if value is None:
            return self._camera.MainScreen
        else:
            self._camera.MainScreen = value

    def isSmallScreenDown(self):
        return bool(self._camera.isSmallScreenDown)

    def screenCurrent(self):

        return self._camera.ScreenCurrent
