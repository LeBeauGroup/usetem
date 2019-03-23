
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

class Instrument():
    instrument = CreateObject("TEMScripting.Instrument.1")

    acquisition = Acquisition(instrument)
    autoloader = AutoLoader(instrument)
    camera = Camera(instrument)

    illumination = Illumination(instrument)
    projection = Projection(instrument)
    temperatureControl = TemperatureControl(instrument)
    vacuum = Vacuum(instrument)
