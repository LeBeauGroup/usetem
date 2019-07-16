from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging

class Vacuum():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._vac = instrument.Vacuum

    def status(self):
        return self._vac.Status

    def columnValvesOpen(self, value = None):

        if value is None:
            return self._vac.ColumnValvesOpen
        else:
            self._vac.ColumnValvesOpen = value

    def isPvpRunning(self):
        return self._vac.PVPRunning

    def gauges(self, name=None):

        if name is None:

            gaugeObjs = self._vac.Gauges

            gauges = dict()

            for gaugeObj in gaugeObjs:
                newGauge = dict()
                newGauge['name'] = gaugeObj.Name
                newGauge['status'] = gaugeObj.Status
                newGauge['pressure'] = gaugeObj.Pressure
                newGauge['pressureLevel'] = gaugeObj.PressureLevel

            return gauges

        elif type(name) is not None:
            gaugeObj = self._vac.Gauges(name)

            newGauge = dict()
            newGauge['name'] = gaugeObj.Name
            newGauge['status'] = gaugeObj.Status
            newGauge['pressure'] = gaugeObj.Pressure
            newGauge['pressureLevel'] = gaugeObj.PressureLevel

            return newGauge


    def runBufferCycle(self):
        self._vac.RunBufferCycle()
