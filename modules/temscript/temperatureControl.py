from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging

class TemperatureControl():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._tempController = instrument.TemperatureControl

    def isAvailable(self):
        return self._tempController.TemperatureControlAvailable

    def refrigerantLevel(self, dewarType = None):

        level = None

        if dewarType is None:
            try:
                level = self._tempController.RefrigerantLevel(RefrigerantLevel.Column.value)
            except:
                print('Could not read level')
        elif type(dewarType) is RefrigerantLevel:
            try:
                level = self._tempController.RefrigerantLevel(dewarType.value)

            except:
                print('Could not read level')

        return level

    def remainingTime(self):
        return self._tempController.DewarsRemainingTime

    def isBusyFilling(self):
        return self._tempController.DewarsAreBusyFilling

    def forceRefill(self):
        try:
            self._tempController.forceRefill
        except:
            logging.debug('Could not fill the dewar')
