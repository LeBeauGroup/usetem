




try:
    from comtypes.gen import ESVision
except:
    from comtypes.client import GetModule
    GetModule("C:\Program Files (x86)\FEI\TIA\Bin\ESVision.tlb")
    from comtypes.gen import ESVision

from comtypes.client import CreateObject, Constants

from xmlrpc.client import Binary
import xmlrpc.client
from _ctypes import COMError
from .acquisitionservers import *
from .beamcontrol import *
from .guiobjects import *
from .acquistionManager import *
from .microscope import *
from .processingSystem import *
from comtypes.safearray import safearray_as_ndarray

import logging
from .enums import *
import pickle
import numpy as np
import ctypes
import array

import datetime

"""
Requires numpy 1.15, comtypes 1.17.1

"""

logging.basicConfig(level=logging.INFO)


class Application():
    app = CreateObject("ESVision.Application")

    imageDisplay = ImageDisplay(app)

    acquisitionManager = AcquisitionManager(app)
    scanningServer = ScanningServer(app)
    beamControl = BeamControl(app)
    microscope = Microscope(app)
    ccdServer = CcdServer(app)
    processingSystem = ProcessingSystem(app)
    objectDisplays = dict()

    _activeDisplayWindow = None

    # def resetApplication(self):
    #
    #     try:
    #         self.app = CreateObject("ESVision.Application")
    #     except COMError as e:
    #         print(e)
    #
    #
    #     self.imageDisplay = ImageDisplay(self.app)
    #
    #     self.acquisitionManager = AcquisitionManager(self.app)
    #     self.scanningServer = ScanningServer(self.app)
    #     self.beamControl = BeamControl(self.app)
    #     self.microscope = Microscope(self.app)
    #     self.ccdServer = CcdServer(self.app)

    def _timeStampName(self):
        return datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

    def _findDisplayWindow(self,name):

        return self.app.FindDisplayWindow(name)




    def addDisplayWindow(self, name=None):
        window = self.app.AddDisplayWindow()
#        window  = self.app.ActiveDisplayWindow()
        if name is None:
            name = self._timeStampName()

        window.Name = name

        return name

    def addDisplay(self, windowPath, displayName,type=DisplayType.Image.value, subType = SubType.Image.value,splitDirection=0,splitPortion=0.5, splitDisplay=None):

        window  = self.app.FindDisplayWindow(windowPath)
        newDisp = window.AddDisplay(displayName + ' Display', type, subType, splitDirection, splitPortion, splitDisplay)

        #cal = self.app.Calibration2D(0, 0, 1e-9, 1e-9, 0, 0)
        imageName = 'test'
        #img = newDisp.addImage(imageName, 512, 512, cal)

        return newDisp.Path#+f'/{imageName}'

    def activateDisplayWindow(self, name):
        self.app.ActivateDisplayWindow(name)

    def activeDisplayWindow(self):

        window  = self.app.ActiveDisplayWindow()
        # self._activeDisplayWindow = DisplayWindow(window)

        return window.Name

    # def activeDisplayPath(self):
    #
    #     self._activeDisplayWindow = DisplayWindow(window)
    #     print(self._activeDisplayWindow)
    #     return self._activeDisplayWindow.path

    def containsDisplayObject(self, path):

        containsObject = False
        if self.app.FindDisplayObject(path):
            containsObject = True

        return containsObject

    def _findDisplayObject(self, path):

        comps = path.split('/')

        window = self.app.FindDisplayWindow(comps[0])
        display = window.FindDisplay(comps[1])
        object = display.FindObject(comps[2])

        return object

    def _convertComplexData(self, data):
        """
        This method converts Complex Data into a real and imag components in the image display

        """
        pass

    def createSubImageDisplay(self, subName,size, cal=(0,0,1e-9,1e-9, 0, 0)):

        win = self.app.activeDisplayWindow()


        realDisp = win.AddDisplay(subName, ESVision.esImageDisplay, ESVision.esImageDisplayType, ESVision.esSplitRight, 0);

        realDisp.Visible = False

        numPixX = size[0]
        numPixY = size[1]
        calibration = calibration2D(cal)

        realDisp.AddImage('real', numPixX, numPixY, calibration)

        return win.name


    def createNewImageDisplay(self,  size, cal=(0,0,1e-9,1e-9, 0, 0)):

        win = self.app.AddDisplayWindow()
        realDisp = win.AddDisplay('real', ESVision.esImageDisplay, ESVision.esImageDisplayType, ESVision.esSplitRight, 0);

        realDisp.Visible = True

        numPixX = size[0]
        numPixY = size[1]
        print(cal)

        calibration = calibration2D(cal)

        realDisp.AddImage('real', numPixX, numPixY, calibration)

        return win.name

    def createNewComplexImageDisplay(self, size, cal=(0,0,1e-9,1e-9, 0, 0)):

        win = self.app.AddDisplayWindow()
        realDisp = win.AddDisplay("real", ESVision.esImageDisplay, ESVision.esImageDisplayType, ESVision.esSplitRight, 0);

        realDisp.Visible = False

        imgDisp = win.AddDisplay("imag", ESVision.esImageDisplay, ESVision.esImageDisplayType, ESVision.esSplitRight, 0);
        imgDisp.Visible = False

        display = win.AddDisplay("display", ESVision.esImageDisplay, ESVision.esImageDisplayType, ESVision.esSplitRight, 0);

        display.Visible = True

        numPixX = size[0]
        numPixY = size[1]

        calibration = calibration2D(cal)

        imgDisp.AddImage('imag', numPixX, numPixY, calibration)
        realDisp.AddImage('real', numPixX, numPixY, calibration)
        display.AddImage('display', numPixX, numPixY, calibration)

        return win.name



    def displayWindowNames(self):
        displayWindows = self.app.DisplayWindowNames()
        displayNames = list()

        for display in enumerate(displayWindows):
            displayNames.append(display)

        return displayNames

    def enableEvents(self,windowName):
        displayObject = self._findDisplayWindow(windowName)
        self.app.EnableEvents(displayObject)


    def closeDisplayWindow(self, windowName):
        self.app.CloseDisplayWindow(windowName)

# Helper functions
app = Application().app

def calibration2D(cal):

    return app.Calibration2D(cal[0],cal[1],cal[2],cal[3],cal[4],cal[5])


def complexNumber(r, i):
    return app.ComplexNumber(r,i)

def range2D(range):

    return app.Range2D(range[0], range[1], range[2], range[3])

def position2D(pos):

    return app.Position2D(pos[0], pos[1])

def findDisplayObject(app, path):
    return  app.FindDisplayObject(path)


def _findDisplayInWindow(app, windowName, displayName):
    displayWindow = app.FindDisplayWindow(windowName)
    display = displayWindow.FindDisplay(displayName)

    return display

    # def FindDisplayObject(self, path):
    #     pass

    # def FindDisplayWindow(self, windowName):
    #     return self.app.FindDisplayWindow(windowName)
