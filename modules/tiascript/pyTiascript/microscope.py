from __future__ import division, print_function
from .enums import *
import math

# Get imports from library
try:
    # Python 3.X
    from urllib.parse import quote
except ImportError:
    # Python 2.X
    from urllib import quote


def _parse_enum(type, item):
    """Try to parse 'item' (string or integer) to enum 'type'"""
    try:
        return type[item]
    except:
        return type(item)


class Microscope(object):
    """
    A more pythonic interface to the microscope.

    Creating an instance of this class, already queries the COM interface for the instrument

        >>> microscope = Microscope()
        >>> microscope.get_family()
        "TITAN"
    """

    # Allowed stage axes
    STAGE_AXES = frozenset(('x', 'y', 'z', 'a', 'b'))

    def __init__(self):
        from .instrument import GetInstrument
        tem = GetInstrument()
        self._tem_instrument = tem
        self._tem_gun = tem.Gun
        self._tem_illumination = tem.Illumination
        self._tem_projection = tem.Projection
        self._tem_stage = tem.Stage
        self._tem_acquisition = tem.Acquisition
        self._tem_vacuum = tem.Vacuum
        self._family = tem.Configuration.ProductFamily

    def get_family(self):
        """Return product family (see :class:`ProductFamily`): "TITAN", "TECNAI", ..."""
        return ProductFamily(self._family).name

    def get_microscope_id(self):
        """
        Return microscope ID.
        Their is no way to read this via the scripting adapter directly.
        We here use the hostname instead
        """
        import socket
        return socket.gethostname()

    def get_version(self):
        """
        Return version string for temscript.

        .. versionadded:: 1.0.8

        :return: String "major.minor.patchlevel"
        """
        from .version import __version__
        return __version__

    def get_voltage(self):
        """
        Return acceleration voltage in kV.

        :return: Float with voltage
        """
        state = self._tem_gun.HTState
        if state == HighTensionState.ON:
            return self._tem_gun.HTValue * 1e-3
        else:
            return 0.0

    def get_vacuum(self):
        """
        Return status of the vacuum system. The method will return a dict with the following entries:

            * "status": Status of the vacuum system (see :class:`VacuumStatus`): "READY", "OFF", ...
            * "column_valves_open": Whether the column valves are currently open
            * "pvp_running": Whether the PVP is running
            * "gauges(Pa)": dict with Gauge values in Pascal (or the string "UNDERFLOW" or "OVERFLOW")

        .. versionchanged: 1.0.8
            Name of "gauges" return value changed
        """
        gauges = {}
        for g in self._tem_vacuum.Gauges:
            g.Read()
            status = GaugeStatus(g.Status)
            if status == GaugeStatus.UNDERFLOW:
                gauges[g.Name] = "UNDERFLOW"
            elif status == GaugeStatus.OVERFLOW:
                gauges[g.Name] = "OVERFLOW"
            elif status == GaugeStatus.VALID:
                gauges[g.Name] = g.Pressure
        return {
            "status" : VacuumStatus(self._tem_vacuum.Status).name,
            "column_valves_open" : self._tem_vacuum.ColumnValvesOpen,
            "pvp_running" : self._tem_vacuum.PVPRunning,
            "gauges(Pa)" : gauges,
        }

    def get_stage_holder(self):
        """Return holder currently in stage (see :class:`StageHolderType`)"""
        return StageHolderType(self._tem_stage.Holder).name

    def get_stage_status(self):
        """Return status of stage (see :class:`StageStatus`)"""
        return StageStatus(self._tem_stage.Status).name

    def get_stage_limits(self):
        """
        Returns dictionary with min/max tuples for all holder axes.
        The tuples are the values, the axis names are the keys.
        For axes "x", "y", "z" the unit is meters
        For axes "a", "b" the unit is radians
        """
        result = {}
        for axis in ('x', 'y', 'z', 'a', 'b'):
            mn, mx, unit = self._tem_stage.AxisData(axis)
            result[axis] = (mn, mx)
        return result

    def get_stage_position(self):
        """
        Returns dictionary with stage position (axes names are used as keys).
        For axes "x", "y", "z" the unit is meters
        For axes "a", "b" the unit is radians
        """
        return self._tem_stage.Position

    def set_stage_position(self, pos, method="GO"):
        """
        Set new stage position. The new position is passed as dict.
        Only the axes are driven which are mentioned in the `pos` dict.
        For axes "x", "y", "z" the unit is meters.
        For axes "a", "b" the unit is radians.

        There are two methods of movement:

            * "GO": Moves directly to new stage position
            * "MOVE": Avoids pole piece touches, by first zeroing the angle, moving the stage than, and setting the angles again.
        """
        if method == "GO":
            self._tem_stage.GoTo(**pos)
        elif method == "MOVE":
            self._tem_stage.MoveTo(**pos)
        else:
            raise ValueError("Unknown movement methods.")

    def get_detectors(self):
        """
        Return dictionary with all available detectors. The method will return a dict, indexed by detector name, with
        another dict as keys. The embedded dict has the key "type" with value "CAMERA" or "STEM_DETECTOR" identifying
        the detector type.

        For "CAMERA" detectors the embedded dict will additionally have the following keys:

                * "height": Height of the detector
                * "width": Width of the detector
                * "pixel_size(um)": Pixel size in micrometers
                * "binnings": List of supported binnings
                * "shutter_modes": List of supported shutter modes (see :class:`AcqShutterMode`)
                * "pre_exposure_limits(s)": Tuple with Min/Max values of pre exposure times in seconds
                * "pre_exposure_pause_limits(s)": Tuple with Min/Max values of pre exposure pause times in seconds

        For "STEM_DETECTOR" detectors the embedded dict will additionally have the following keys:

                * "binnings": List of supported binnings
        """
        detectors = {}
        for cam in self._tem_acquisition.Cameras:
            info = cam.Info
            param = cam.AcqParams
            name = quote(info.Name)
            detectors[name] = {
                "type": "CAMERA",
                "height": info.Height,
                "width": info.Width,
                "pixel_size(um)": tuple(size / 1e-6 for size in info.PixelSize),
                "binnings": [int(b) for b in info.Binnings],
                "shutter_modes": [AcqShutterMode(x).name for x in info.ShutterModes],
                "pre_exposure_limits(s)": (param.MinPreExposureTime, param.MaxPreExposureTime),
                "pre_exposure_pause_limits(s)": (param.MinPreExposurePauseTime, param.MaxPreExposurePauseTime)
            }
        for stem in self._tem_acquisition.Detectors:
            info = stem.Info
            detectors[name] = {
                "type": "STEM_DETECTOR",
                "binnings": [int(b) for b in info.Binnings],
            }
        return detectors

    def _find_detector(self, name):
        """Find detector object by name"""
        for cam in self._tem_acquisition.Cameras:
            if quote(cam.Info.Name) == name:
                return cam
        for stem in self._tem_acquisition.Detectors:
            if quote(stem.Info.Name) == name:
                return stem
        raise KeyError("No detector with name %s" % name)

    def _get_camera_param(self, det):
        """Create dict with camera parameters"""
        info = det.Info
        param = det.AcqParams
        return {
            "image_size": AcqImageSize(param.ImageSize).name,
            "exposure(s)": param.ExposureTime,
            "binning": param.Binning,
            "correction": AcqImageCorrection(param.ImageCorrection).name,
            "exposure_mode": AcqExposureMode(param.ExposureMode).name,
            "shutter_mode": AcqShutterMode(info.ShutterMode).name,
            "pre_exposure(s)": param.PreExposureTime,
            "pre_exposure_pause(s)": param.PreExposurePauseTime
        }

    def _set_camera_param(self, det, values):
        """Set camera parameters"""
        info = det.Info
        param = det.AcqParams
        # Silently ignore failures
        try:
            param.ImageSize = _parse_enum(AcqImageSize, values["image_size"])
        except Exception:
            pass
        try:
            param.ExposureTime = values["exposure(s)"]
        except Exception:
            pass
        try:
            param.Binning = values["binning"]
        except Exception:
            pass
        try:
            param.ImageCorrection = _parse_enum(AcqImageCorrection, values["correction"])
        except Exception:
            pass
        try:
            param.ExposureMode = _parse_enum(AcqExposureMode, values["exposure_mode"])
        except Exception:
            pass
        try:
            info.ShutterMode = _parse_enum(AcqShutterMode, values["shutter_mode"])
        except Exception:
            pass
        try:
            param.PreExposureTime = values["pre_exposure(s)"]
        except Exception:
            pass
        try:
            param.PreExposurePauseTime = values["pre_exposure_pause(s)"]
        except Exception:
            pass

    def _get_stem_detector_param(self, det):
        """Create dict with STEM detector parameters"""
        info = det.Info
        param = det.AcqParams
        return {
            "brightness": info.Brightness,
            "contrast": info.Contrast,
            "image_size": AcqImageSize(param.ImageSize).name,
            "binning": param.Binning,
            "dwelltime(s)": param.DwellTime
        }

    def _set_stem_detector_param(self, det, values):
        """Set STEM detector parameters"""
        info = det.Info
        param = det.AcqParams
        # Silently ignore failures
        try:
            info.Brightness = values["brightness"]
        except Exception:
            pass
        try:
            info.Contrast = values["contrast"]
        except Exception:
            pass
        try:
            param.ImageSize = _parse_enum(AcqImageSize, values["image_size"])
        except Exception:
            pass
        try:
            param.Binning = values["binning"]
        except Exception:
            pass
        try:
            param.DwellTime = values["dwelltime(s)"]
        except Exception:
            pass

    def get_detector_param(self, name):
        """
        Return parameters for detector `name` as dictionary.

        For "CAMERA" detectors the dict will have the following keys:

            * "image_size": Size of image (see :class:`AcqImageSize`): "FULL", "HALF", ...
            * "exposure(s)": Exposure time in seconds
            * "correction": Correction mode (see :class:`AcqImageCorrection`)
            * "exposure_mode": Exposure mode (see :class:`AcqExposureMode`)
            * "shutter_mode": Shutter mode (see :class:`AcqShutterMode`)
            * "pre_exposure(s)": Pre exposure time in seconds
            * "pre_exposure_pause(s)": Pre exposure pause time in seconds

        For "STEM_DETECTORS" the dict will have the following keys:

            * "brightness": Brightness settings
            * "contrast": Contrast setting
            * "image_size": Size of image (see :class:`AcqImageSize`): "FULL", "HALF", ...
            * "binning": Binning
            * "dwelltime(s)": Dwell time in seconds
        """
        from .instrument import CCDCamera, STEMDetector
        det = self._find_detector(name)
        if isinstance(det, CCDCamera):
            return self._get_camera_param(det)
        elif isinstance(det, STEMDetector):
            return self._get_stem_detector_param(det)
        else:
            raise TypeError("Unknown detector type.")

    def set_detector_param(self, name, param):
        """
        Set parameters for detector `name`. The parameters should be given as a dictionary.
        Allowed keys are described in the :meth:`get_detector_param` method.
        If setting a parameter fails, no error is given.
        """
        from .instrument import CCDCamera, STEMDetector
        det = self._find_detector(name)
        if isinstance(det, CCDCamera):
            self._set_camera_param(det, param)
        elif isinstance(det, STEMDetector):
            self._set_stem_detector_param(det, param)
        else:
            raise TypeError("Unknown detector type.")

    def acquire(self, *args):
        """
        Acquire images for all detectors given as argument.
        The images are returned in an dict indexed by detector name.
        """
        self._tem_acquisition.RemoveAllAcqDevices()
        for det in args:
            try:
                self._tem_acquisition.AddAcqDeviceByName(det)
            except Exception:
                pass
        # Read as dict of numpy arrays
        images = self._tem_acquisition.AcquireImages()
        result = {}
        for img in images:
            result[quote(img.Name)] = img.Array
        return result

    def get_image_shift(self):
        """
        Return image shift as (x,y) tuple.

        The units this is returned in are meters. The accuracy of ths value depends on the accuracy of the
        calibration within the microscope and thus is better not to be trusted blindly.
        
        On FEI microscopes this corresponds to the state of "User Image Shift" (in different units though).
        """
        return self._tem_projection.ImageShift

    def set_image_shift(self, pos):
        """
        Set image shift to position `pos`, which should be an (x, y) tuple, as returned for instance by :meth:`get_image_shift`.
        """
        self._tem_projection.ImageShift = pos

    def get_beam_shift(self):
        """
        Return beam shift as (x,y) tuple.

        The units this is returned in are meters. The accuracy of ths value depends on the accuracy of the
        calibration within the microscope and thus is better not to be trusted blindly.
       
        On FEI microscopes this corresponds to the state of "User Beam Shift" (in different units though).
        """
        return self._tem_illumination.Shift

    def set_beam_shift(self, pos):
        """
        Set beam shift to position `pos`, which should be an (x, y) tuple, as returned for instance by :meth:`get_image_shift`.
        """
        self._tem_illumination.Shift = pos

    def get_beam_tilt(self):
        """
        Return beam tilt as (x,y) tuple.

        The units this is returned in are radians. The accuracy of ths value depends on the accuracy of the
        calibration within the microscope and thus is better not to be trusted blindly.

        On FEI microscopes this corresponds to the state of "DF Tilt" (in different units though).
        """
        tilt = self._tem_illumination.Tilt
        mode = self._tem_illumination.DFMode
        if mode == DarkFieldMode.CONICAL:
            return tilt[0] * math.cos(tilt[1]), tilt[0] * math.sin(tilt[1])
        elif mode == DarkFieldMode.CARTESIAN:
            return tilt
        else:
            return 0.0, 0.0     # Microscope might return nonsense if DFMode is OFF
            
    def set_beam_tilt(self, tilt):
        """
        Set beam tilt to position `tilt`, which should be an (x, y) tuple, as returned for instance by :meth:`get_image_shift`.
        
        On FEI microscopes:
        * this will turn on dark field mode, unless (0, 0) is set, which will also turn off the dark field mode.
        """
        mode = self._tem_illumination.DFMode
        if tilt[0] == 0.0 and tilt[1] == 0.0:
            self._tem_illumination.Tilt = 0.0, 0.0
            self._tem_illumination.DFMode = DarkFieldMode.OFF
        elif mode == DarkFieldMode.CONICAL:
            self._tem_illumination.Tilt = math.sqrt(tilt[0]**2 + tilt[1]**2), math.atan2(tilt[1], tilt[0])
        elif mode == DarkFieldMode.OFF:
            self._tem_illumination.DFMode = DarkFieldMode.CARTESIAN
            self._tem_illumination.Tilt = tilt
        else:
            self._tem_illumination.Tilt = tilt
