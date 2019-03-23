from enum import Enum

class AcqImageCorrection(Enum):
    Unprocessed = 0
    Default = 1

class AcqShutterMode(Enum):
    PreSpecimen = 0
    PostSpecimen =  1
    Both = 2

class AcqExposureMode(Enum):
    NoMode = 0
    Simultaneous = 1
    PreExposure = 2
    PreExposurePause = 3


class AcqMaxFrame(Enum):
    Full = 0
    Half = 1
    Quarter = 2

class AcqImageSize(Enum):
    Full = 0
    Half = 1
    Quarter = 2

class AcqFrameSize(Enum):
    Full = 1
    Half = 2
    Quarter = 4
    Eighth = 8

class RefrigerantLevel(Enum):
    AutoLoader = 0
    Column = 1
    Helium = 2

class VacuumStatus(Enum):

    Unknown = 0
    Off = 1
    CameraAir = 2
    Busy = 3
    Ready = 4
    Else = 5

class VacuumGauge(Enum):
    CCGp = 0
    IGPa = 1
    ICPcl = 2

class GaugeStatus(Enum):
    Undefined = 0
    Underflow = 1
    Overflow = 2
    Valid = 3
    Invalid = 4

class GaugePressureLevel(Enum):
    Undefined = 0
    Low = 1
    LowMedium = 2
    HighMedium = 3
    High = 4

class ScreenPosition(Enum):
    Unknown = 0
    Up = 2
    Down = 3
