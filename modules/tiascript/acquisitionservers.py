import logging
from enums import *
import application


logging.basicConfig(level=logging.INFO)

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

    def CreateMagnification(self, mag, imageRange, modeString):

        mMode = MicroscopeModes[modeString].value
        self.server.CreateMagnification(mag, esvision.Range2D(imageRange),mMode)

    def DeleteMagnification(self, name, modeString):
        mMode = MicroscopeModes[modeString].value
        self.server.DeleteMagnification(name, mMode)


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


    def MagnificationName(self, mag, microscopeModeString):
        return self.server.MagnificationName(mag, MicroscopeModes[microscopeModeString].value)

    def MagnificationNames(self, microscopeModeString):

        names = self.server.MagnificationNames(MicroscopeModes[microscopeModeString].value)

        namesList = list()
        for name in names:
            namesList.append(name)

        return namesList

    def ReferencePosition(self, position=None):

        if position is None:
            return self.server.ReferencePosition
        else:
            ref = esvision.Position2D(position)
            self.server.ReferencePosition = ref
            logging.debug(f'Reference Position moved to {position}')

    def SetBiasImage(self, imageData):
        pass

    def SetDriftRate(self, driftX, driftY):
        self.server.SetDriftRate(driftX, driftY)
        logging.debug(f'Drift rate set to ({driftX}, {driftY})')

    def SetGainImage(self, imageData):
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


class EmpadServer(ScanningServer):
    a =2
