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


class HightensionState(Enum):

    Disabled = 1
    Off = 2
    On = 3

class InstrumentMode(Enum):
    TEM = 0
    STEM = 1

class ProjNormalization(Enum):

    Objective = 10
    Projector = 11
    All = 12


class ProjMode(Enum):

    Imaging = 1
    Diffraction = 2


class ProjSubMode(Enum):

    LM = 1
    Mi = 2
    SA = 3
    Mh = 4
    LAD = 5
    D = 6


class ProjLensProg(Enum):
    Regular = 1
    EFTEM = 2


class ProjDetectorShift(Enum):

    OnAxis = 0
    NearAxis = 1
    OffAxis = 2


class ProjDetectorShiftMode(Enum):

    AutoIgnore = 1
    Manual = 2
    Alignment = 3


class RefrigerantLevel(Enum):
    AutoLoader = 0
    Column = 1
    Helium = 2


class ScreenPosition(Enum):
    Unknown = 1
    Up = 2
    Down = 3

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
