from comtypes.gen import TEMScripting
from stemDetectors import STEMDetectors
from enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
from utilities import *

class Stage():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._stage = instrument.Stage

    def status(self):
        pass

    def position(self):

        return positionDict(self._stage.Position)

    def holder(self):
        pass

    def axisData():
        pass

    def goto(self, newPos):

        self._stage.GoTo(temPosition(self._instrument,newPos))

    def gotoWithSpeed():
        pass

    def moveTo():
        pass
