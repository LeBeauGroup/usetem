import useTEM.pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy import ndimage
import time
import matplotlib.pyplot as plt
from skimage.util import noise
from PyQt5 import QtWidgets
from PyQt5 import Qt, QtCore
import types
import math

import skimage
import sys, os


class ManualFocus(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ManualFocus, self).__init__()

        self.isRunning = False
        self.event = None
      #  self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000, 'start_step_size':10})

       # self.defaultParameters.update({'dwellTime': 1e-6,
      #                            'binning': '100x100',
       #                           'numFrames': 1, 'detectors': ['HAADF']})
#
        #self.parameterTypes = {'rate':float, 'precision':float, 'max_iters':int, 'start_step_size':float}
        self.stepSize = 1.0
        self.defaultParameters.update({'dwellTime': 2e-6,
                                  'binning': '512x512',
                                  'numFrames': 1, 'detectors': ['HAADF'], 'stepSize':1.0})


    def ui(self, item, parent=None):

        theUi = super(ManualFocus, self).ui(item, parent)

        self.item = item
        # widget = theUi.findChild(QtWidgets.QWidget, 'widget')

        # widget.continueButton.clicked.connect(self.continueWorkflow)

        return theUi

    def continueWorkflow(self):

        self.isRunning = False

    def updateEvent(self, event):
        self.event = event
        print(event)

    def changeDefocus(self, sign: int, stepSize:float):
        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']

        currentDefocus = optics.defocus()
        optics.defocus(currentDefocus + sign*stepSize * 1e-9)

    def run(self, params=None, result=None):

        self.isRunning = True
        stepSize = 1
        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']


        # start stem scanning
        stem.setupFocus(params)
        stem.start()

        thread = QtCore.QThread.currentThread()

        while True:
            if self.event is None:
                continue

            if self.event.key() == QtCore.Qt.Key_Left:
                print('left arrow')
                self.changeDefocus(-1, stepSize)

            elif self.event.key() == QtCore.Qt.Key_Right:
                self.changeDefocus(1, stepSize)

            elif self.event.key() == QtCore.Qt.Key_Up:
                stepSize *=1.5

                print(thread)
                self.item.data['stepSize'] = stepSize
                thread.workflowItemNeedsUpdate.emit(self.item)

            elif self.event.key() == QtCore.Qt.Key_Down:
                stepSize /= 1.5
                self.item.data['stepSize'] = stepSize
                thread.workflowItemNeedsUpdate.emit(self.item)
                
            elif self.event.key() == QtCore.Qt.Key_Return :

                break
            else:
                continue
            self.event = None
        stem.stop()
        self.isRunning = False

        return True
