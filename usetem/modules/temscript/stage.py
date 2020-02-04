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

    def _axisMask(self, delta):

        axisMask = 0
        delta = np.abs(delta)
        cutoff = 5e-9
        ABcutoff = 1e-5

        # X, Y axis
        if delta[0] >= cutoff and delta[1] >= cutoff:
            axisMask = axisMask | StageAxes.axisXY.value
        elif  delta[0] >= cutoff:
            axisMask = axisMask | StageAxes.axisX.value
        elif delta[1] >= cutoff:
            axisMask = axisMask | StageAxes.axisY.value

        # Z axis
        if delta[2] >= cutoff:
            axisMask = axisMask | StageAxes.axisZ.value

        #A  axis

        if delta[3] >= ABcutoff:
            axisMask = axisMask | StageAxes.axisA.value

        # B axis
        if delta[4] >= ABcutoff:
            axisMask = axisMask | StageAxes.axisB.value

        return axisMask

    def stepBy(self, delta):
        """
        A and B axes are in radians
        """

        axisMask = self._axisMask(delta)

        position = self._stage.Position
        posArray = np.array([position.X+delta[0], position.Y+delta[1], position.Z+delta[2], position.A+delta[3], position.B+delta[4]])

        position.SetAsArray(posArray.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))

        try:
            self._stage.GoTo(position, axisMask)
        except COMError as e:
            print(e)

    def _deltaCalc(self, newPos):

        position = self._stage.Position

        tempPos = np.array([0, 0, 0, 0, 0])
        tempPos = tempPos.ctypes.data_as(ctypes.POINTER(ctypes.c_double))

        position.GetAsArray(tempPos)

        currentPos = np.ctypeslib.as_array(tempPos, shape=(1, 5)).flatten()
        delta = currentPos - newPos

        return delta

    def goto(self, newPos):
        """
        TODO: Need to check for single/double tilt
        TODO: Validate parameters

        :param newPos: [X,Y,Z,A,B] vector
        :return:
        """
        delta  = self._deltaCalc(newPos)
        axisMask = self._axisMask(delta)

        # Check to make sure that we should actually move

        if axisMask != 0:

            print(f'Moving to {newPos} with axis mask {axisMask}')

            posArray = np.array(newPos)
            position = self._stage.Position

            position.SetAsArray(posArray.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
            self._stage.GoTo(position, axisMask)

    def gotoWithSpeed(self, newPos, speed):
        """
        TODO: Need to check for single/double tilt
        TODO: Validate parameters

        :param newPos: [X,Y,Z,A,B] vector
        :return:
        """

        delta = self._deltaCalc(newPos)
        axisMask = self._axisMask(delta)

        # Check to make sure that we should actually move

        if axisMask != 0:
            posArray = np.array(newPos)
            position = self._stage.Position

            position.SetAsArray(posArray.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
            self._stage.GoToWithSpeed(position, axisMask, speed)

    def moveTo(self, newPos):
        """
        TODO: Need to check for single/double tilt
        TODO: Validate parameters

        :param newPos: [X,Y,Z,A,B] vector
        :return:
        """
        delta = self._deltaCalc(newPos)
        axisMask = self._axisMask(delta)

        # Check to make sure that we should actually move

        if axisMask != 0:
            print(f'Moving to {newPos} with axis mask {axisMask}')

            posArray = np.array(newPos)
            position = self._stage.Position

            position.SetAsArray(posArray.ctypes.data_as(ctypes.POINTER(ctypes.c_double)))
            self._stage.MoveTo(position, axisMask)
