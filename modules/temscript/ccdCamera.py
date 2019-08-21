
from comtypes.safearray import safearray_as_ndarray

class CCDCamera():

    def __init__(self,camObj):
        self._camera = camObj

    def name(self):
        return self._camera.Info.Name

    def height(self):
        return self._camera.Info.Height

    def width(self):
        return self._camera.Info.Width

    def pixelSize(self):

        pixSize = self._camera.Info.PixelSize

        return (pixSize.X, pixSize.Y)



    def shutterModes(self):

        with safearray_as_ndarray:
            modes = self._camera.Info.ShutterModes
        return modes

    def shutterMode(self, value=None):

        if value is None:
            return self._camera.ShutterMode
        else:
            self._camera.ShutterMode = value


    def binnings(self):

        with safearray_as_ndarray:
            binnings = self._camera.Info.Binnings

        return binnings
