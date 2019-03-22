import application
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
        pass
        #self.name = obj.Name
        #self.type = obj.Type

    #    self.path= obj.Path()
# class ImageDisplay(DisplayObject):
#     pass

class DisplayObject(EsvObject):

    path = 'none'
    calibration = None
    type = None
    object = None

    def __init__(self, object):
        super(DisplayObject, self).__init__(object)

        while True:
            for type in object_types:
                try:
                    object.QueryInterface(type)
                    self.type = type
                    self.object = object
                except:
                    continue
                break
            break

        if self.type == ESVision.IImage:
            pass

            # t = object.Data

            # newData = ps.real(object.Data)
            # print(newData.QueryInterface(ESVision.IData2D))
            # new =  2*np.ones((512,512))*newData.Array #* 1+1j
            # ps.Add(newData,newData)

            # with safearray_as_ndarray:
            #     a = object.Data.Array
            #
            # #a[100][400] = 1
            # #new = new.ctypes.data_as(ctypes.POINTER(ctypes.c_uint16))
            #
            # newData.Array = new
            # c = esvision.app.ComplexNumber(int(20),0)
            #
            #
            # newData.PixelIntensity(141,227, c)
            # object.Data = newData

            #object.Data = ps.FFT(object.Data)
            #newData = object.Data
            #newData.PixelIntensity(141,227, app.ComplexNumber(int(20),0))
            #newData.SetSize(512,512)


    @property
    def sendable(self):

        toSend = dict()

        with safearray_as_ndarray:
            toSend['data'] = self.object.Data.Array

        return Binary(pickle.dumps(toSend))



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

    def SelectedObject(self):
        pass

    def AddDisplay(name, type, subtype, splitdirection, newsplitportion,splitDisplay=None):
        pass
