from comtypes.gen import TEMScripting

class AutoLoader():
    _instrument = None


    def __init__(self, instrument):
        self._instrument = instrument
        self._autoloader = instrument.AutoLoader
