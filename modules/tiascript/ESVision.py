from comtypes.gen import ESVision
import comtypes
from comtypes.client import CreateObject, Constants
from comtypes.safearray import safearray_as_ndarray
from xmlrpc.client import Binary
import xmlrpc.client
import acquisitionservers
import beamcontrol
import logging
import enums
import pickle
import numpy as np
import ctypes
import array

"""
Requires numpy 1.15
"""

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


    def SetAcquireAnnotation(self, start, end=None):

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
    DisplayObject = None

    def ActiveDisplayWindow(self):

        activeWindow = self.app.ActiveDisplayWindow()
        window = DisplayWindow(activeWindow)

        return Binary(pickle.dumps(window))

    def FindDisplayObject(self, path):

        comps = path.split('/')

        window = self.app.FindDisplayWindow(comps[0])
        display = window.FindDisplay(comps[1])
        object = display.FindObject(comps[2])

        dispObject = DisplayObject(object)
        return Binary(pickle.dumps(dispObject))

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

class EsvObject():
    name = 'none'
    type  = 0

    def __init__(self, obj):

        self.name = obj.Name
        self.type = obj.Type
    #    self.path= obj.Path()

class DisplayObject(EsvObject):

    path = 'none'
    types = (ESVision.IData1D, ESVision.IData2D, ESVision.IMatrix)
    calibration = None

    def __init__(self, object):
        super(DisplayObject, self).__init__(object)

        #ESVision.Image
        #self.path = object.Path

        dataPointer = object.Data

        while True:
            for type in self.types:

                try:
                    data = dataPointer.QueryInterface(type)
                    self.type = type
                except:
                    continue
                break
            break

        #print(data.Points)
        if self.type == ESVision.IData2D:

            ps = app.ProcessingSystem()
            object.Data = ps.FFT(object.Data)
            newData = object.Data
            #newData.PixelIntensity(141,227, app.ComplexNumber(int(20),0))
            #newData.SetSize(512,512)

            new =  np.zeros((512,512)).astype(np.uint16)

            with safearray_as_ndarray:
                a = object.Data.Imag

            a[100][400] = 1
            #new = new.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))

            newData.Array = a

            #print(newData.PixelIntensity(2,2).Real)
            object.Data = newData
            #object.SetIntegerData(512)
            #object.Data.Array = np.array(oldDatra).ctypes.data
            # p = oldDatra.PixelIntensity(0,0)
            # p.Real = 5
            # print(oldDatra.PixelIntensity(0,0).Real)

            #with safearray_as_ndarray:
            #print(object.Data)


class ObjectDisplay(EsvObject):

    path = 'none'

    def __init__(self, display):
        super(ObjectDisplay, self).__init__(ObjectDisplay)
        self.path = display.Path


class DisplayWindow():

    def __init__(self, window):
        self.name = window.name

        #super(DisplayWindow, self).__init__(window)

        self.selectedDisplay = DisplayObject(window.SelectedDisplay)
        self.selectedObject = EsvObject(window.SelectedObject)

        # self.SelectedObject = EsvObject(window.SelectedObject)

    def SelectedObject(self):
        pass

    def AddDisplay(name, type, subtype, splitdirection, newsplitportion,splitDisplay=None):
        pass



def Range2D(range):

    return app.Range2D(range[0], range[1], range[2], range[3])

def Position2D(pos):

    return app.Position2D(pos[0], pos[1])

def FindDisplayObject(self, path):
    return  self.app.FindDisplayObject(path)


def FindDisplayInWindow(app, windowName, displayName):
    displayWindow = app.FindDisplayWindow(windowName)
    display = displayWindow.FindDisplay(displayName)

    return display

    # def FindDisplayObject(self, path):
    #     pass

    # def FindDisplayWindow(self, windowName):
    #     return self.app.FindDisplayWindow(windowName)
