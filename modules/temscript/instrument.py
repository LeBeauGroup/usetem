
from comtypes.client import CreateObject, Constants
from comtypes.gen import TEMScripting

from comtypes.client import GetModule

from acquisition import Acquisition
from autoloader import AutoLoader
from illumination import Illumination



class Instrument():
    instrument = CreateObject("TEMScripting.Instrument.1")

    acquisition = Acquisition(instrument)
    autoloader = AutoLoader(instrument)
    illumination = Illumination(instrument)

    
