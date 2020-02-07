import usetem.pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy import ndimage
import time
import matplotlib.pyplot as plt
from skimage.util import noise
from PyQt5 import QtWidgets
import math

import skimage
import sys, os


class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000, 'start_step_size':10})

        self.defaultParameters.update({'dwellTime': 1e-6,
                                  'binning': '100x100',
                                  'numFrames': 1, 'detectors': ['HAADF']})

        self.parameterTypes = {'rate':float, 'precision':float, 'max_iters':int, 'start_step_size':float}


    def ui(self, item, parent=None):
        theUi = super(AutoFocusSTEM, self).ui(item,parent)

        widget = theUi.findChild(QtWidgets.QWidget, 'widget')
        widget.stopButton.clicked.connect(self.stopScan)        #theUi.stopButton.setDisabled(True)

        return theUi

    def stopScan(self):

        try:

            tia = self.interfaces['tiascript']
            stem = tia.techniques['STEMImage']

            if stem.isScanning():
                stem.stop()

        except:
            pass

    # def gradientDescent():
    #     while previous_step_size > precision and iters < max_iters:
    #
    #
    #         cur_y = -stem.variance()
    #
    #         if abs(cur_y - prev_y) < 1e-3:
    #             continue
    #
    #         if iters == 0:
    #             print(cur_y, prev_y, cur_x, prev_x)
    #             grad = (cur_y-prev_y)/(cur_x-prev_x)
    #
    #         else:
    #             grad = (cur_y - prev_y) / (cur_x - prev_x)
    #             prev_x = cur_x
    #
    #
    #         #plt.scatter(cur_x, cur_y)
    #         #plt.pause(0.005)
    #
    #         step = rate*grad
    #         print(np.sign(grad))
    #
    #         if abs(step) > 5:
    #             cur_x -= np.sign(step)*5
    #         else:
    #             cur_x -= step
    #
    #         optics.defocus(float(cur_x * 1e-9))
    #
    #         # Grad descent
    #
    #         previous_step_size = abs(cur_x - prev_x)  # Change in x
    #         iters = iters + 1  # iteration count
    #         prev_y = cur_y

    def divideAndConquer(self, focus_range, optics=None, stem=None):

        # focus_range = 100.0
        precision = 1

        iterations = math.floor(math.log2(focus_range / precision)) + 1

        currentDefocus = optics.defocus()/1e-9 # seed the defocus

        for i in range(0, iterations):

            midPoint = currentDefocus

            startPoint = midPoint - focus_range / 2.0
            endPoint = midPoint + focus_range / 2.0

            foci = np.linspace(start=startPoint, stop=endPoint, num=3)
            vars = []
            #print(foci)

            seedVar = stem.variance()

            for focus in foci:
                optics.defocus(float(focus)*1e-9)
                var = seedVar

                while(seedVar == var):
                    var = stem.variance()
                    continue


                vars.append(var)

            vars = np.array(vars) ** 1
            print(vars)
            vars = (vars) / vars.sum()

            updateDefocus = float((vars * foci).sum())
            optics.defocus(updateDefocus*1e-9)
            focus_range /= 2

            #print(updateDefocus)

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

        # startDefocus = optics.defocus()

        # start stem scanning
        stem.setupFocus(params)
        stem.start()


        self.divideAndConquer(50, optics=optics, stem=stem)
       # self.divideAndConquer(25, optics=optics, stem=stem)
        # prev_x = startDefocus*1e9  # The algorithm starts at x=3
        # prev_y = -stem.variance()
        #
        # cur_x = prev_x + previous_step_size
        # print('got here')


        #plt.show()
        stem.stop()
        print("The local minimum occurs at", optics.defocus()/1e-9)

        return True
