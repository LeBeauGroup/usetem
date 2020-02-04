
from comtypes.client import CreateObject, Constants
try:
    from comtypes.gen import TEMScripting
except:
    CreateObject("TEMScripting.Instrument")
    from comtypes.gen import TEMScripting


from comtypes.client import GetModule

from .acquisition import Acquisition
from .autoloader import AutoLoader
from .illumination import Illumination
from .temperatureControl import TemperatureControl
from .vacuum import Vacuum
from .camera import Camera
from .projection import Projection
from .gun import Gun
from .stage import Stage

class Instrument():

    try:
        instrument = CreateObject("TEMScripting.Instrument")
    except:
        print('Could not create instrument')

    acquisition = Acquisition(instrument)
    autoloader = AutoLoader(instrument)
    camera = Camera(instrument)
    gun = Gun(instrument)
    illumination = Illumination(instrument)
    projection = Projection(instrument)
    stage = Stage(instrument)
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
