import pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy.ndimage import gaussian_filter
import time
import matplotlib.pyplot as plt
from skimage.util import noise

import skimage
import sys, os


class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000})

        self.defaultParameters.update({'dwellTime': '5e-6',
                                  'binning': '256x256',
                                  'numFrames': '1', 'detectors': ['HAADF']})


    def stdevContrast(self,stemInterface, x=None):

        if x is not None:
            test = gaussian_filter(image, abs(x))
        # plt.imshow(test)
        # plt.draw()
        # plt.pause(0.001)
        value = -np.std(test)
        return value


    def run(self, params=None, result=None):
        tem = self.interfaces['temscript']
        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']
        optics = tem.techniques['OpticsControl']

        optics.defocus(6e-9)
        stem.setupFocus(params)

        cur_x = 6 # The algorithm starts at x=3
        rate = params['rate']  # Learning rate
        precision = params['precision']  # This tells us when to stop the algorithm
        previous_step_size = 10  #
        max_iters = params['max_iters']  # maximum number of iterations
        iters = 0  # iteration counter

        def df(im, x):
            return  #self.stdevContrast(im, x)  # Gradient of our function

        # theImage = stem.acquire()

        # plt.ion()
        # self.im = plt.imshow(theImage)
        # plt.show()
        stem.start()
        prev_y = -stem.stdev()
        prev_x = 5.0
        time.sleep(0.06)
        cur_x = cur_x
        cur_y = -stem.stdev()


        while previous_step_size > precision and iters < max_iters:

            if iters == 0:
                grad = (cur_y-prev_y)/(cur_x-prev_x)
            else:
                # Store current x value in prev_x

                if stem.stdev() == cur_y:
                    continue

                cur_y = -stem.stdev()


                print(cur_y)
                grad = (cur_y - prev_y) / (cur_x - prev_x)
                prev_x = cur_x

            # print(grad, cur_x, cur_y)
            cur_x = cur_x - rate * grad  # Grad descent

            # if cur_x <= 1:
            #     cur_x = 1

            optics.defocus(float(cur_x)*1e-9)

            previous_step_size = abs(cur_x - prev_x)  # Change in x
            iters = iters + 1  # iteration count
            prev_y = cur_y

        stem.stop()
        print("The local minimum occurs at", cur_x)

        return True
