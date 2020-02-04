from .enums import *
from .instrument import Instrument

class InstrumentModeControl():

    _instrumentModeControl = None


    def __init__(self, instrument:Instrument):
        self._instrument = instrument
        self._instModeControl = instrument.InstrumentModeControl

    def stemAvailable(self):
		return self. _instModeControl.StemAvailable

	def instrumentMode(self, *argmode):

		try:
			return self._instModeControl.InstrumentMode(*argmode)
		except:
			print('could not check or change the mode')
