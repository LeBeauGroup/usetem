
from comtypes.safearray import safearray_as_ndarray

class STEMDetector():

    def __init__(self,detObj):
        self.detector = detObj

    def name(self):
        return self.detector.Info.Name

    def brightness(self, value=None):

        if value is None:
            return self.detector.Info.Brightness
        else:
            self.detector.Info.Brightness = value

    def contrast(self, value=None):

        if value is None:
            return self.detector.Info.Contrast
        else:
            self.detector.Info.Contrast = value

    def binnings(self):

        with safearray_as_ndarray:
            binnings = self.detector.Info.Binnings
        return binnings
