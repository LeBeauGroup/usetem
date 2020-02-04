from comtypes.gen import TEMScripting
from .enums import *
from comtypes.safearray import safearray_as_ndarray
import numpy as np
import logging

class Projection():

    _instrument = None

    def __init__(self, instrument):
        self._instrument = instrument
        self._proj = instrument.Projection

    def mode(self, value=None):

        if value is None:
            return self._proj.mode
        else:
            self._proj.Mode = value

    def subMode(self):
        return self._proj.subMode

    def subModeString(self):
        return self._proj.subModeString

    def lensProgram(self, value=None):
        """
        Will error out if microscope does not have EFTEM mode
        """

        if value is None:

            return self._proj.LensProgram
        else:
            self._proj.LensProgram = value

    def magnification(self, value=None):

        return self._proj.Magnification

    def magnificationIndex(self, value=None):
        logging.warning(value)

        if value is None:

            return self._proj.MagnificationIndex
        else:
            self._proj.MagnificationIndex = value


    def imageRotation(self):
        return self._proj.ImageRotation * 180/np.pi

    def detectorShift(self,value=None):

        """
        Value corresponds to ProjectionDetectorShift enum value
        """
        if value is None:

            return self._proj.DetectorShift
        else:
            self._proj.DetectorShift = value




    def detectorShiftMode(self, value=None):
        """
        Value corresponds to ProjectionDetectorShift enum value
        """
        if value is None:

            return self._proj.DetectorShiftMode
        else:
            self._proj.DetectorShiftMode = value

    def diffractionShift(self, value=None):
        """
        Set with a tuple, (x,y), units of radians
        """
        if value is None:

            vec =  self._proj.DiffractionShift
            return (vec.X, vec.Y)
        else:
            vec = self._proj.DiffractionShift
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.DiffractionShift = vec


    # Mode A dependendent
    def focus(self, value=None):
        """
        TODO: set some control on range -1 to 1

        """

        if value is None:

            return self._proj.Focus
        else:
            self._proj.Focus = value

    def defocus(self, value=None):
        """

        """

        if value is None:

            return self._proj.Defocus
        else:
            self._proj.Defocus = value

    def objectiveExcitation(self):
        """

        """
        return self._proj.ObjectiveExcitation



    def cameraLength(self,value = None):
        """

        """

        if value is None:
            return self._proj.CameraLengthIndex
        else:
            self._proj.CameraLengthIndex = value

        return self._proj.CameraLength

    def cameraLengthIndex(self, value=None):
        if value is None:

            return self._proj.CameraLengthIndex
        else:
            self._proj.CameraLengthIndex = value

    def objectiveStigmator(self, value=None):
        """
        Set with a tuple, (x,y)
        """
        if value is None:
            vec =  self._proj.ObjectiveStigmator
            return (vec.X, vec.Y)
        else:
            vec = self._proj.ObjectiveStigmator
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.ObjectiveStigmator = vec

    def diffractionStigmator(self, value=None):
        """
        Set with a tuple, (x,y)
        TODO: make sure provided values are within range (-1, 1)

        TODO: Add try/except to make sure this will work
        """
        if value is None:
            vec =  self._proj.DiffractionStigmator
            return (vec.X, vec.Y)
        else:
            vec = self._proj.DiffractionStigmator
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.DiffractionStigmator = vec

    def imageShift(self, value=None):
        """
        Set with a tuple, (x,y), units of meters
        TODO: make sure provided values are within range (-1, 1)
        TODO: Add try/except to make sure this will work in current mode
        """
        if value is None:
            vec =  self._proj.ImageShift
            return (vec.X, vec.Y)
        else:
            vec = self._proj.ImageShift
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.ImageShift = vec


    def imageBeamShift(self, value=None):
        """
        Set with a tuple, (x,y), units of meters
        TODO: make sure provided values are within range (-1, 1)
        TODO: Add try/except to make sure this will work in current mode

        Attention: Avoid intermixing ImageShift and ImageBeamShift, otherwise it would mess up the beam shift (=Illumination.Shift). If you want to use both alternately, then reset the other to zero first.

        """
        if value is None:
            vec =  self._proj.ImageBeamShift
            return (vec.X, vec.Y)
        else:
            vec = self._proj.ImageBeamShift
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.ImageBeamShift = vec

    def imageBeamTilt(self, value=None):
        """
        Set with a tuple, (x,y), units of radians
        TODO: make sure provided values are within range (-1, 1)
        TODO: Add try/except to make sure this will work in current mode

        Attention: Avoid intermixing Tilt (of the beam in Illumination) and ImageBeamTilt. If you want to use both alternately, then reset the other to zero first

        """
        if value is None:
            vec =  self._proj.imageBeamTilt
            return (vec.X, vec.Y)
        else:
            vec = self._proj.imageBeamTilt
            vec.X = value[0]
            vec.Y = value[1]
            self._proj.imageBeamTilt = vec

    def projectionIndex(self, value=None):
        """
        [Long], read/write
        This index always contains a value. It corresponds to the camera length index or the magnification index, dependent on the microscope mode.


        """

        if value is None:

            return self._proj.ProjectionIndex
        else:
            self._proj.ProjectionIndex = value


    def subModeMinIndex(self, value=None):

        """
        The minimum ProjectionIndex of the current submode. Check this if you want to change the ProjectionIndex or MagnificationIndex but do not want to leave the submode.
        """

        return self._proj.SubModeMinIndex

    def subModeMaxIndex(self, value=None):

        """
        The max ProjectionIndex of the current submode. Check this if you want to change the ProjectionIndex or MagnificationIndex but do not want to leave the submode.
        """
        return self._proj.SubModeMaxIndex

    def zeroDefocus(self):
        self._proj.ResetDefocus()

    def stepProjectionIndexBy(self, value):
        self._proj.ChangeProjectionIndex(value)

    def normalize(self, value):
            self._proj.Normalize(value)
