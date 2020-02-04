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


class ScanModes(Enum):
    Spot = 0
    Line = 1
    Frame = 2


class MicroscopeModes(Enum):
    Imaging = 0
    Diffraction = 1

class DisplayType(Enum):
    Image = 0
    Profile = 1
    Spectrum = 2

class SubType(Enum):
    Image = 0
    Reciprocal = 1
    EDX = 2
    EDXReciprocal = 3
    PEELS = 4
    PEELSReciprocal = 5
    Profile = 6
    ReciprocalProfile = 7

class SplitType(Enum):
    Right = 0
    Left = 1
    Top = 2
    Bottom = 3

