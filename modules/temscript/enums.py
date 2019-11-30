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

class IllumNormalization(Enum):

    spotsize = 1
    intensity = 2
    condenser = 3
    miniCondenser = 4
    objectivePole = 5
    all = 6

class InstrumentMode(Enum):

    tem = 0
    stem = 1


class IllumMode(Enum):

    nanoProbe = 0
    microProbe = 1



class DarkFieldMode(Enum):

    Off = 1
    Cartesian = 2
    Conical = 3


class CondenserMode(Enum):

    ParallelIllumination = 0
    ProbeIllumination = 1


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

class StageAxes(Enum):
    """
    The ‘GoTo’ and ‘MoveTo’ methods require a parameter (of type long) that contains bitwise information about which 
    axis is to be involved in the movement. The bit order is BAZYX , so bit 0 contains the information about whether the
    X-axis is involved, bit 4 contains the information about the B axis. The members of the ‘StageAxes’ enumeration can
    be used instead of calculating with bits. You can combine them by bitwise  ‘OR’s 
    (i.e. in JScript: MyAxBits = (axisXY | axisA | axisB) to allow the X,Y,A,B axis to move, but leave the Z constant.
    """
    axisX = 1
    axisY = 2
    axisXY = 3
    axisZ = 4
    axisA = 8
    axisB = 16


class StageHolderType(Enum):
    NoHolder = 0
    SingleTilt = 1
    DoubleTilt = 2
    Invalid = 4
    Polara = 5
    DualAxis = 6

class MeasurementUnitType(Enum):
    Unknown = 0
    Meters = 1
    Radians = 2