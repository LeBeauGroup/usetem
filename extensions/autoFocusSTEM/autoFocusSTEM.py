import pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy.ndimage import gaussian_filter
import matplotlib.pyplot as plt
from skimage.util import noise

import skimage
import sys, os


class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update({'rate':0.01, 'precision':0.000001, 'max_iters':10000})

        self.defaultParameters.update({'dwellTime': '5e-6',
                                  'binning': '100x100',
                                  'numFrames': '1', 'detectors': ['HAADF']})


    def stdevContrast(self,image, x=None):

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
        rate = 0.01  # Learning rate
        precision = 0.0001  # This tells us when to stop the algorithm
        previous_step_size = 1  #
        max_iters = 1000  # maximum number of iterations
        iters = 0  # iteration counter

        df = lambda im, x: self.stdevContrast(im, x) # Gradient of our function
        theImage = stem.acquire(returnsImage=True)

        # plt.ion()
        # self.im = plt.imshow(theImage)
        # plt.show()

        prev_y = df(theImage, 5.0)
        prev_x = 5.0

        cur_x = cur_x
        cur_y = df(theImage,cur_x)

        while previous_step_size > precision and iters < max_iters:

            if iters == 0:
                grad = (cur_y-prev_y)/(cur_x-prev_x)
            else:
                # Store current x value in prev_x
                theImage = stem.acquire(returnsImage=True)

                cur_y = df(theImage, cur_x)
                grad = (cur_y - prev_y) / (cur_x - prev_x)
                prev_x = cur_x

            print(grad, cur_x,cur_y)
            cur_x = cur_x - rate * grad  # Grad descent

            if cur_x <= 1:
                cur_x = 1

            optics.defocus(float(cur_x)*1e-9)

            previous_step_size = abs(cur_x - prev_x)  # Change in x
            iters = iters + 1  # iteration count
            prev_y = cur_y


            # print("Iteration", iters, "\nX value is", cur_x)  # Print iterations

        print("The local minimum occurs at", cur_x)

        return result
