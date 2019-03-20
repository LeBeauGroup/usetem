from comtypes.gen import ESVision
from comtypes.client import CreateObject, Constants
import acquisitionservers
import beamcontrol
import logging
import enums


logging.basicConfig(level=logging.INFO)



class AcquisitionManager():

    def __init__(self,app):
        self.acqm = app.AcquisitionManager()
        self.app = app

    def Acquire(self):
        self.acqm.Acquire()

    # acquires a set of points, positions in m, and time in s
    def AcquireSet(self,positions,dwelltime):

        posCollection = self.app.PositionCollection()

        for pos in positions:
            esVPos = self.app.Position2D(pos[0],pos[1])
            posCollection.Add(esVPos)

        self.acqm.AcquireSet(posCollection,dwelltime)

    def AddSetup(self, setupName):
        self.acqm.AddSetup(setupName)

    def CurrentSetup(self):
        return self.acqm.CurrentSetup

    def CanReset(self):
        return self.acqm.CanReset

    def CanStop(self):
        return self.acqm.CanStop

    def CanStart(self):
        return self.acqm.CanStart

    def ClearAcquireAnnotation(self):
        self.acqm.ClearAcquireAnnotation()

    def DeleteSetup(self, name):
        self.acqm.DeleteSetup(name)

    def DoesSetupExist(self, setupName):
        return self.acqm.DoesSetupExist(setupName)

    def EnabledSignalNames(self):
        names = list()

        for name in enumerate(self.acqm.EnabledSignalNames):
            names.append(name)

        return names

    def IsAcquiring(self):
        return self.acqm.IsAcquiring

    def IsAcquisitionHardware(self,type):
        return self.acqm.IsAcquisitionHardware(type)

    def IsCurrentSetup(self):
        return self.acqm.IsCurrentSetup()


    # TODO: Implement an approach for this
    def IsSignalLinked(self,signalName, displayObject):
        pass
        #return self.acqm.IsSignalLinked(signalName,displayObject)

    def LinkSignal(self, signalName, displayObject):
        pass

    def SelectSetup(self, setupName):
        self.acqm.SelectSetup(setupName)


    def SetAcquireAnnnotation(self, start, end=None):

        startLength = len(start)

        if startLength == 2:
            start = self.app.Position2D(start[0], start[1])
        elif startLength == 4:
            start = self.app.Range2D(start[0], start[1], start[2], start[3])

        if end is None:
            self.acqm.SetAcquireAnnotation(start)
        elif len(end) == 2:
            end = self.app.Position2D(end[0], end[1])
            self.acqm.SetAcquireAnnotation(start,end)


    def SetAnnotationDisplay(self, windowName, displayName):

        #displayWindow = self.app.FindDisplayWindow(displayName)
        self.app.ActivateDisplayWindow(windowName)
        window = self.app.ActiveDisplayWindow()
        display = window.FindDisplay(displayName)

        self.acqm.SetAnnotationDisplay(display)

    def SetAutoStart(self, setupName, state=True):
        self.acqm.SetAutoStart(setupName, state)

    def SignalNames(self):
        names = list()
        for name in enumerate(self.acqm.SignalNames):
            names.append(name)

        return names

    def SignalType(self, signalName):
        return Signals(self.acqm.SignalType(signalName)).name

    def Start(self):
        self.acqm.Start()

    def Stop(self):
        self.acqm.Stop()


    def TimeRemaining(self):
        self.acqm.TimeRemaining()

    def TypedSignalNames(self,type):

        signals = self.acqm.TypedSignalNames(Signals[type].value)

        signalNames = list()

        for signal in enumerate(signals):
            signalNames.append(signal)

        return signalNames

    def UnlinkAllSignals(self):
        self.acqm.UnlinkAllSignals()

    def UnlinkSignal(self,signalName):
        self.acqm.UnlinkAllSignals(signalName)



class Microscope():
    def __init__(self,app):
        self.microscope = app.Microscope()
        self.app = app

class Application():
    app = CreateObject("ESVision.Application")
    AcquisitionManager = AcquisitionManager(app)
    ScanningServer = acquisitionservers.ScanningServer(app)
    BeamControl = beamcontrol.BeamControl(app)
    Microscope = Microscope(app)
    CcdServer = acquisitionservers.CcdServer(app)

    def DisplayWindowNames(self):
        displayWindows = self.app.DisplayWindowNames()
        displayNames = list()
        for display in enumerate(displayWindows):

            displayNames.append(display)

        return displayNames



    def CloseDisplayWindow(self, windowName):
        self.app.CloseDisplayWindow(windowName)


# Helper functions

app = Application().app

def Range2D(range):

    return app.Range2D(range[0], range[1], range[2], range[3])

def FindDisplayInWindow(app, windowName, displayName):
    displayWindow = app.FindDisplayWindow(windowName)
    display = displayWindow.FindDisplay(displayName)

    return display

    # def FindDisplayObject(self, path):
    #     pass

    # def FindDisplayWindow(self, windowName):
    #     return self.app.FindDisplayWindow(windowName)
