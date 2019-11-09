import pluginTypes as pluginTypes
import numpy as np
from skimage import io
from scipy.ndimage import gaussian_filter

import skimage
import sys, os


class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update()

        # self.defaultParameters.update({'rotation': '90', 'dwellTime': '5e-6',
        #                           'binning': '512x512',
        #                           'numFrames': '12', 'detectors': ['HAADF']})

    def measure(self,image, x=None):

        if x is not None:
            test = gaussian_filter(image, abs(x))

        value = -np.std(test)
        # print(value)
        return value


    def run(self, params=None, result=None):

        filePath = sys.modules[self.__module__].__file__.split(os.extsep)[0]
        imagePath = filePath + '.png'
        theImage = io.imread(imagePath)

        cur_x = 5 # The algorithm starts at x=3
        rate = 0.01  # Learning rate
        precision = 0.0000001  # This tells us when to stop the algorithm
        previous_step_size = 5  #
        max_iters = 10000  # maximum number of iterations
        iters = 0  # iteration counter

        df = lambda x: self.measure(theImage, x) # Gradient of our function

        prev_y = df(4.0)
        prev_x = 4.0

        cur_x = 3.0
        cur_y = df(cur_x)

        while previous_step_size > precision and iters < max_iters:

            if iters == 0:
                grad = (cur_y-prev_y)/(cur_x-prev_x)
            else:
                # Store current x value in prev_x

                cur_y = df(cur_x)
                grad = (cur_y - prev_y) / (cur_x - prev_x)
                prev_x = cur_x

            print(grad, cur_x,cur_y)
            cur_x = cur_x - rate * grad  # Grad descent
            previous_step_size = abs(cur_x - prev_x)  # Change in x
            iters = iters + 1  # iteration count
            prev_y = cur_y


            # print("Iteration", iters, "\nX value is", cur_x)  # Print iterations

        print("The local minimum occurs at", cur_x)

        return result
