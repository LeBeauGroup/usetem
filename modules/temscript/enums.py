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
