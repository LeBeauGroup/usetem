import logging

from enum import Enum

logging.basicConfig(level=logging.INFO)

class AcquireModes(Enum):
    ContinuousAcquire = 0
    SingleAcquire = 1

class AcquisitionServer():

    def __init__(self,app,classType):
        self.app = app
        self.server = getattr(app, classType)

    def BiasCorrection(self):
        pass

    def GainCorrection(self):
        pass

    def SeriesSize(self,size=0):

        if size == 0:
            return self.server.SeriesSize
        else:
            self.server.SeriesSize = size
            logging.info(f'Series size set as {size}')


class ImageServer(AcquisitionServer):

    def __init__(self,app):
            self.app = app
            self.server = app.ScanningServer()

    def BeamPosition(self, pos=None):
        if pos is None:
            pos2d = self.server.BeamPosition
            return (pos2d.X, pos2d.Y)
        else:
            self.server.BeamPosition = self.app.Position2D(pos[0], pos[1])
            logging.debug(f'Beam Position moved to {pos}')

    def AcquireMode(self, mode=None):

        if mode is None:
            return AcquireModes(self.server.AcquireMode).name
        else:
            self.server.AcquireMode = AcquireModes[mode].value
            logging.info(f'Acquire mode is now {AcquireModes[mode].name}')

    def CreateMagnification(self, magnification, imageRange, microscopeMode):
        pass

    def DeleteMagnification(self):
        pass


    def DriftRateX(self, value=None):

        if value is None:
            return self.server.DriftRateX
        else:
            self.server.DriftRateX = value
            logging.debug(f'DwellTime set as {value}')

    def DriftRateY(self, value=None):

        if value is None:
            return self.server.DriftRateY
        else:
            self.server.DriftRateY = value
            logging.debug(f'DwellTime set as {value}')


    def MagnificationName(self):
        pass

    def MagnificationNames(self):
        pass

    def ReferencePosition(self):
        pass

    def SetBiasImage(self):
        pass

    def SetDriftRate(self):
        pass

    def SetGainImage(self):
        pass



class ScanningServer(ImageServer):

    def __init__(self,app):
            self.app = app
            self.server = app.ScanningServer()

    def FrameWidth(self, value=None):

        if value is None:
            return self.server.FrameWidth
        else:
            self.server.FrameWidth = value
            logging.debug(f'Frame Width set as {value}')

    def DwellTime(self, value=None):

        if value is None:
            return self.server.DwellTime
        else:
            self.server.DwellTime = value
            logging.debug(f'DwellTime set as {value}')

    def FrameHeight(self, value=None):

        if value is None:
            return self.server.FrameHeight
        else:
            self.server.FrameHeight = value
            logging.debug(f'Frame Height set as {value}')



class ParallelImageServer(AcquisitionServer):

    def Camera(self):
        pass


class CcdServer(ParallelImageServer):

    def __init__(self,app):
        self.app = app
        self.acqserver = app.CcdServer()

    def Binning(self):
        self.acqserver.Binning = 2
