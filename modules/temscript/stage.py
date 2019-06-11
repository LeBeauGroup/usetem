from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
from .utilities import *

class Stage():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._stage = instrument.Stage

    def status(self):
        pass

    def position(self):

        return positionDictFromTem(self._stage.Position)

    def holder(self):
        pass

    def axisData():
        pass

    def stepByAlong(self, delta,axis):
        """
        TODO: Automatically determine which axes to use based on which positions have changed
        """

        temPos = temPositionFromDict(self._instrument,newPos)
        self._stage.GoTo(temPos,axesToUSe)

    def goto(self, newPos,axesToUSe):
        """
        TODO: Automatically determine which axes to use based on which positions have changed

        """
        temPos = temPositionFromDict(self._instrument,newPos)
        self._stage.GoTo(temPos,axesToUSe)

    def gotoWithSpeed():
        pass

    def moveTo():
        pass
