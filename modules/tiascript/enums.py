from enum import Enum

class Hardware(Enum):
    CCD = 0
    Video = 1
    Scanning = 2
    Edx = 3
    Peels = 4

class Signals(Enum):
    AnalogImage = 0
    PulseImage = 1
    Peels = 2
    PeelsMapping = 3
    Edx = 4
    EdxMapping = 5
    CCD = 6
    Video = 7


class AcquireModes(Enum):
    Continuous = 0
    Single = 1



class MicroscopeModes(Enum):
    Imaging = 0
    Diffraction = 1
