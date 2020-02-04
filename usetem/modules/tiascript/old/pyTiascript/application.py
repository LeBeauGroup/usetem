from comtypes.client import CreateObject, Constants
from comtypes.gen import ESVision

# Have atleast some stubs to develop software also on off-line computers...
def GetApplication():
    """Returns Application instance."""
    raise RuntimeError("TIA  API is not accessible")

    return CreateObject("ESVision.Application")

class Stage:
    pass

class CCDCamera:
    pass

class CCDCameraInfo:
    pass

class CCDAcqParams:
    pass

class STEMDetector:
    pass

class STEMDetectorInfo:
    pass

class STEMAcqParams:
    pass

class AcqImage:
    pass

class Acquisition:
    pass

class Gauge:
    pass

class Vacuum:
    pass

class Configuration:
    pass

class Projection:
    pass

class Illumination:
    pass

class Gun:
    pass

class BlankerShutter:
    pass

class InstrumentModeControl:
    pass

class Instrument:
    pass
