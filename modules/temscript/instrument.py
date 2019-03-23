
from comtypes.client import CreateObject, Constants
from comtypes.gen import TEMScripting

from comtypes.client import GetModule

from acquisition import Acquisition
from autoloader import AutoLoader
from illumination import Illumination
from temperatureControl import TemperatureControl
from vacuum import Vacuum
from camera import Camera
from projection import Projection
from gun import Gun

class Instrument():
    instrument = CreateObject("TEMScripting.Instrument.1")

    acquisition = Acquisition(instrument)
    autoloader = AutoLoader(instrument)
    camera = Camera(instrument)
    gun = Gun(instrument)
    illumination = Illumination(instrument)
    projection = Projection(instrument)
    temperatureControl = TemperatureControl(instrument)
    vacuum = Vacuum(instrument)

    buttons  = instrument.UserButtons

    def isSTEMAvailable(self):
        return self.instrument.InstrumentModeControl.StemAvailable

    def mode(self, modeValue=None):

        if modeValue is None:

            return self.instrument.InstrumentModeControl.InstrumentMode

        else:
            self.instrument.InstrumentModeControl.InstrumentMode = modeValue