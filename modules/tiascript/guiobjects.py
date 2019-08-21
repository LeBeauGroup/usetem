from .application import *
from comtypes.gen import ESVision
import numpy as np
import ctypes
from comtypes.gen import ESVision
import comtypes
from comtypes.client import CreateObject, Constants
from xmlrpc.client import Binary
from comtypes.safearray import safearray_as_ndarray
import pickle

data_types = (ESVision.IData1D, ESVision.IData2D)
object_types = (ESVision.IImage, ESVision.ISpectrum)


class EsvObject():
    name = 'none'
    type  = 0

    def __init__(self, obj):
        self.name = obj.Name
        self.type = obj.Type

    #    self.path= obj.Path()
# class ImageDisplay(DisplayObject):
#     pass

class ObjectDisplay():

    def __init__(self,app):
        self.app = app




class DisplayObject():

    def __init__(self, app):
        self.app = app
        # super(DisplayObject, self).__init__(object)

    def _obj(self):
        obj = self.app.FindDisplay(self.path)

        return obj

    def name(self,path):

        self.path = path
        return self._obj().Name

    def path(self,path):
        self.path = path
        return self._obj().Path

    def _path_comps(self,path):
        comps = path.split('/')

        window = (comps[0])
        display = window.FindDisplay(comps[1])
        object = display.FindObject(comps[2])

        return (window.Name,display, object)


    # def typeTest(self):
    #
    #     while True:
    #         for type in object_types:
    #             try:
    #                 object.QueryInterface(type)
    #                 self.type = type
    #                 self.object = object
    #             except:
    #                 continue
    #             break
    #         break
    #
    #     if self.type == ESVision.IImage:
    #         data = object.Data
    #
    #         import time
    #
    #         start = time.time()
    #
    #
    #
    #         for i in range(0, 60):
    #
    #             array = np.random.randn(128,128)*65535
    #             data.Array  = array
    #             object.Data = data
    #
    #         end = time.time()
    #         print(end - start)

            #
            #
            #
            # newData.Array = new
            # c = esvision.app.ComplexNumber(int(20),0)
            #
            #
            # newData.PixelIntensity(141,227, c)
            # object.Data = newData


    @property
    def sendable(self):

        toSend = dict()

        with safearray_as_ndarray:
            toSend['data'] = self.object.Data.Array

        return Binary(pickle.dumps(toSend))

class ImageDisplay(DisplayObject):


    def addImage(self, path, imageName, sizeX, sizeY, calibration):
        comps = path.split('/')

        window = self.app.FindDisplayWindow(comps[0])
        display = window.FindDisplay(comps[1])

        cal = self.app.Calibration2D(calibration[0],
                                     calibration[1],
                                     calibration[2],
                                     calibration[3],
                                     calibration[4],
                                     calibration[5])
        display.AddImage(imageName, sizeX, sizeY, cal)
        return path+f'/{imageName}'






class ImageObject(DisplayObject):

    def setImageDataWithArray(self, array):

        """
        Sends numpy data into the image

        The array cannot be directly copied to object.
        Instead we use an intermediary
        """
        data = object.Data
        data.Array  = array
        object.Data = data



class ObjectDisplay(EsvObject):

    path = 'none'

    def __init__(self, display):
        super(ObjectDisplay, self).__init__(ObjectDisplay)
        self.path = display.Path


class DisplayWindow():

    def __init__(self, window):
        self.name = window.Name
        self.window = window

        #super(DisplayWindow, self).__init__(window)

        self.selectedDisplay = DisplayObject(window.SelectedDisplay)
        self.selectedObject = EsvObject(window.SelectedObject)


    def _displayWindows(self):
        displays = dict()

        for displayName in self.displayWindowNames():
            display = window.FindDisplay('displayName')
            displays[displayName]  = DisplayWindow(display)

        return displays

        # self.SelectedObject = EsvObject(window.SelectedObject)

    def selectedObject(self):
        pass

    def addDisplay(name, type, subtype, splitdirection, newsplitportion,splitDisplay=None):
        pass
