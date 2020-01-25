import useTEM.pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy import ndimage
import time
import matplotlib.pyplot as plt
from skimage.util import noise
from PyQt5 import QtWidgets
import  types
import math

import skimage
import sys, os


class ManualFocus(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(ManualFocus, self).__init__()

        self.isRunning = False
      #  self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000, 'start_step_size':10})

       # self.defaultParameters.update({'dwellTime': 1e-6,
      #                            'binning': '100x100',
       #                           'numFrames': 1, 'detectors': ['HAADF']})
#
        #self.parameterTypes = {'rate':float, 'precision':float, 'max_iters':int, 'start_step_size':float}


    def ui(self, item, parent=None):
        theUi = super(ManualFocus, self).ui(item, parent)

        def patch(target):
            def keyPressEvent(target, event):
                print('a')

            target.keyPressEvent = types.MethodType(keyPressEvent, target)

        widget = theUi.findChild(QtWidgets.QWidget, 'widget')


        widget.continueButton.clicked.connect(self.continueWorkflow)

        return theUi

    def continueWorkflow(self):

        self.isRunning = False

    def run(self, params=None, result=None):

        self.isRunning = True

        #tem = self.interfaces['temscript']
        #tia = self.interfaces['tiascript']

        #optics = tem.techniques['OpticsControl']

        while self.isRunning:
            pass



        return True
