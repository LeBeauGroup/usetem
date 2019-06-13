import logging
from .enums import *
from .application import *
import comtypes


logging.basicConfig(level=logging.INFO)

class BeamControl():

    def __init__(self, app):
        self.app = app
        self.beamcontrol = self.app.BeamControl()

    def CanStart(self):
        return self.beamcontrol.CanStart

    def DwellTime(self, dwell=None):
        # Units of seconds

        if dwell is None:
            return self.beamcontrol.DwellTime
        elif dwell > 0:
            self.beamcontrol.DwellTime = dwell

    def IsScanning(self):
        return self.beamcontrol.IsScanning

    def LoadPositions(self, positions):
        # List of positions

        collection = self.app.PositionCollection()

        for pos in positions:
            #esv_pos = self.app.Position2D(pos[0], pos[1])
            collection.AddPosition(pos[0], pos[1])

        self.beamcontrol.LoadPositions(collection)

    def MoveBeam(self, xPos, yPos):
        self.beamcontrol.MoveBeam(xPos,yPos)

    def PositionCalibrated(self, state=None):
        if state is None:
            return self.beamcontrol.PositionCalibrated
        elif type(state) is bool:
            self.beamcontrol.PositionCalibrated = state

    def Reset(self):

        self.beamcontrol.Reset()

    def SetContinuousScan(self):
        self.beamcontrol.SetContinuousScan()

    def SetFrameScan(self, scanRange, numPointsX, numPointsY):

        range = self.app.Range2D(scanRange[0], scanRange[1],scanRange[2],scanRange[3])
        print(range.EndY)
        self.beamcontrol.SetFrameScan(range, numPointsX, numPointsY)

    def SetLineScan(self, startPoint, endPoint, numPoints):

        start = self.app.Position2D(startPoint[0], startPoint[1])
        end = self.app.Position2D(endPoint[0], endPoint[1])

        self.beamcontrol.SetLineScan(start,end, numPoints)

    def SetSingleScan(self):
        self.beamcontrol.SetSingleScan()

    def Start(self):

        try:
            self.beamcontrol.Start()
        except comtypes.COMError as inst:
            logging.info(inst.args[2])


    def Stop(self):

        try:
            self.beamcontrol.Stop()
        except comtypes.COMError as inst:
            logging.info(inst.args[2])
