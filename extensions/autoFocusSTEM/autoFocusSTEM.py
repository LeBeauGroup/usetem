import pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy.ndimage import gaussian_filter
import time
import matplotlib.pyplot as plt
from skimage.util import noise
from PyQt5 import QtWidgets

import skimage
import sys, os


class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000, 'start_step_size':10})

        self.defaultParameters.update({'dwellTime': 5e-6,
                                  'binning': '256x256',
                                  'numFrames': 1, 'detectors': ['HAADF']})

        self.parameterTypes = {'dwellTime': float, 'binning': str, 'numFrames': int, 'rate':float, 'precision':float, 'max_iters':int}


    def ui(self, item, parent=None):
        theUi = super(AutoFocusSTEM, self).ui(item,parent)


        theUi.findChild(QtWidgets.QWidget, 'widget').stopButton.clicked.connect(self.stopScan)        #theUi.stopButton.setDisabled(True)
        return theUi

    def stopScan(self):

        try:

            tia = self.interfaces['tiascript']
            stem = tia.techniques['STEMImage']

            if stem.isScanning():
                stem.stop()

        except:
            pass

    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']
        optics = tem.techniques['OpticsControl']

        rate = params['rate']  # Learning rate
        precision = params['precision']  # This tells us when to stop the algorithm
        previous_step_size = params['start_step_size']  #
        max_iters = params['max_iters']  # maximum number of iterations
        iters = 0  # iteration counter

        startDefocus = optics.defocus()

        # start stem scanning
        stem.setupFocus(params)
        stem.start()

        prev_x = startDefocus*1e9  # The algorithm starts at x=3
        prev_y = -stem.stdev()

        cur_x = prev_x + previous_step_size

        while previous_step_size > precision and iters < max_iters:

            optics.defocus(float(cur_x*1e-9))

            if -stem.stdev() == prev_y:
                continue

            if iters == 0:
                cur_y = -stem.stdev()
                print(cur_y, prev_y, cur_x, prev_x)

                grad = (cur_y-prev_y)/(cur_x-prev_x)

            else:
                # Store current x value in prev_x

                cur_y = -stem.stdev()
                grad = (cur_y - prev_y) / (cur_x - prev_x)
                prev_x = cur_x

            cur_x = cur_x - rate * grad  # Grad descent

            previous_step_size = abs(cur_x - prev_x)  # Change in x
            iters = iters + 1  # iteration count
            prev_y = cur_y

        stem.stop()
        print("The local minimum occurs at", cur_x)

        return True
