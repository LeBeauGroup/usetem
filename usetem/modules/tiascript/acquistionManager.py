from .application import *
from comtypes.gen.ESVision import IImage, IData2D

from comtypes.safearray import safearray_as_ndarray
import logging
import pickle
import xmlrpc
import numpy as np
logging.basicConfig(level=logging.INFO)
class AcquisitionManager():

    def __init__(self, app):
        self.acqm = app.AcquisitionManager()
        self.app = app

    def acquire(self, returnsImage=False, imagePath=None):


        # returnsImage = False, imagePath = self.imagePaths[0]

        logging.info('Acquiring an image')

        if returnsImage is True and imagePath is not None:

            comps = imagePath.split('/')

            self.acqm.Acquire()


            # window = self.app.FindDisplayWindow(comps[0])
            # display = window.FindDisplay(comps[1])
            # image = display.FindObject(comps[2])

            image = self.app.FindDisplayObject(imagePath).QueryInterface(IImage)

            imageData = image.Data

            with safearray_as_ndarray:
                imageArray = imageData.Array
            a = pickle.dumps(imageArray)




            return xmlrpc.client.Binary(a)

        else:
            self.acqm.Acquire()


    # acquires a set of points, positions in m, and time in s
    def acquireSet(self, positions, dwelltime):

        posCollection = self.app.PositionCollection()

        for pos in positions:
            esVPos = self.app.Position2D(pos[0],pos[1])
            posCollection.Add(esVPos)

        self.acqm.AcquireSet(posCollection,dwelltime)

    def addSetup(self, setupName):

        try:
            self.acqm.AddSetup(setupName)
        except:
            print('COM error')

    def currentSetup(self):
        return self.acqm.CurrentSetup

    def canReset(self):
        return self.acqm.CanReset

    def canStop(self):
        return self.acqm.CanStop

    def canStart(self):
        return self.acqm.CanStart

    def clearAcquireAnnotation(self):
        self.acqm.ClearAcquireAnnotation()

    def deleteSetup(self, name):
        self.acqm.DeleteSetup(name)

    def doesSetupExist(self, setupName):
        return self.acqm.DoesSetupExist(setupName)

    def enabledSignalNames(self):
        names = list()

        for name in enumerate(self.acqm.EnabledSignalNames):
            names.append(name)

        return names

    def isAcquiring(self):
        return self.acqm.IsAcquiring

    def isAcquisitionHardware(self,type):
        return self.acqm.IsAcquisitionHardware(type)

    def isCurrentSetup(self):
        testing = self.acqm.IsCurrentSetup


        return testing


    # TODO: Implement an approach for this
    def isSignalLinked(self,signalName, displayObject):
        pass
        #return self.acqm.IsSignalLinked(signalName,displayObject)

    def linkSignal(self, signalName, imagePath):
        print(imagePath)
        displayObject = self.app.FindDisplayObject(imagePath)
        print(displayObject)

        self.acqm.LinkSignal(signalName, displayObject)

    def reset(self):
        self.acqm.Reset()

    def selectSetup(self, setupName):
        self.acqm.SelectSetup(setupName)


    def setAcquireAnnotation(self, start, end=None):

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


    def setAnnotationDisplay(self, windowName, displayName):

        #displayWindow = self.app.FindDisplayWindow(displayName)
        self.app.ActivateDisplayWindow(windowName)
        window = self.app.ActiveDisplayWindow()
        display = window.FindDisplay(displayName)

        self.acqm.SetAnnotationDisplay(display)

    def setAutoStart(self, setupName, state=True):
        self.acqm.SetAutoStart(setupName, state)

    def signalNames(self):
        names = list()
        for name in enumerate(self.acqm.SignalNames):
            names.append(name)

        return names

    def signalType(self, signalName):
        return Signals(self.acqm.SignalType(signalName)).name

    def start(self):
        self.acqm.Start()

    def stop(self):
        self.acqm.Stop()


    def timeRemaining(self):
        self.acqm.TimeRemaining()

    def typedSignalNames(self, type):

        signals = self.acqm.TypedSignalNames(Signals[type].value)

        signalNames = list()

        for signal in enumerate(signals):
            signalNames.append(signal)

        return signalNames

    def unlinkAllSignals(self):
        self.acqm.UnlinkAllSignals()

    def unlinkSignal(self,signalName):
        self.acqm.UnlinkAllSignals(signalName)
