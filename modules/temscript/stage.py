from _ctypes import COMError
from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging
from .utilities import *
import array
import numpy as np
import ctypes


class Stage():

    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._stage = instrument.Stage

    def status(self):

        return self._stage.StageStatus

    def position(self):

        return positionDictFromTem(self._stage.Position)

    def holder(self):
        """
        :returns holder type to be enumerated

        """

        return self._stage.Holder



    def axisData(self, axis):
        """
        The ‘GoTo’ and ‘MoveTo’ methods require a parameter (of type long) that contains bitwise information about which
        axis is to be involved in the movement. The bit order is BAZYX , so bit 0 contains the information about whether the
        X-axis is involved, bit 4 contains the information about the B axis. The members of the ‘StageAxes’ enumeration can
        be used instead of calculating with bits. You can combine them by bitwise  ‘OR’s
        (i.e. in JScript: MyAxBits = (axisXY | axisA | axisB) to allow the X,Y,A,B axis to move, but leave the Z constant.
        """

        dataObject = self._stage.AxisData(axis)

        axisDataDict = {
            "minPos": dataObject.MinPos,
            "maxPos": dataObject.MaxPos,
            "unitType": dataObject.UnitType
        }

        return axisDataDict

    def stepByAlong(self, delta):
        """
        A and B axes are in radians
        """

        axisMask = 0

        # X, Y axis
        if delta[0] != 0 and delta[1] != 0:
            axisMask = axisMask | StageAxes.axisXY.value
        elif  delta[0] != 0:
            axisMask = axisMask | StageAxes.axisX.value
        elif delta[1] != 0:
            axisMask = axisMask | StageAxes.axisY.value

        # Z axis
        if delta[2] != 0:
            axisMask = axisMask | StageAxes.axisZ.value

        #A  axis

        if delta[3] != 0:
            axisMask = axisMask | StageAxes.axisA.value

        # B axis
        if delta[4] != 0:
            axisMask = axisMask | StageAxes.axisB.value

        position = self._stage.Position
        posArray = np.array([position.X+delta[0], position.Y+delta[1], position.Z+delta[2], position.A+delta[3], position.B+delta[4]])

        position.SetAsArray(posArray.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

        try:
            self._stage.GoTo(position, axisMask)
        except COMError as e:
            print(e)

    def goto(self, newPos,axesToUSe):
        """
        TODO: Automatically determine which axes to use based on which positions have changed

        """
        temPos = temPositionFromDict(self._instrument, newPos)
        self._stage.GoTo(temPos, axesToUSe)

    def gotoWithSpeed():
        pass

    def moveTo():
        pass
