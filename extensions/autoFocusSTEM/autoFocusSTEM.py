import pluginTypes as pluginTypes
import numpy as np



class AutoFocusSTEM(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AutoFocusSTEM, self).__init__()
        self.defaultParameters.update()

        # self.defaultParameters.update({'rotation': '90', 'dwellTime': '5e-6',
        #                           'binning': '512x512',
        #                           'numFrames': '12', 'detectors': ['HAADF']})

    def run(self, params=None, result=None):


        cur_x = 3  # The algorithm starts at x=3
        rate = 0.1  # Learning rate
        precision = 0.01  # This tells us when to stop the algorithm
        previous_step_size = 1  #
        max_iters = 10000  # maximum number of iterations
        iters = 0  # iteration counter


        df = lambda x: 2 * (x + 5)  # Gradient of our function

        while previous_step_size > precision and iters < max_iters:
            prev_x = cur_x  # Store current x value in prev_x
            cur_x = cur_x - rate * df(prev_x)  # Grad descent
            previous_step_size = abs(cur_x - prev_x)  # Change in x
            iters = iters + 1  # iteration count
            print("Iteration", iters, "\nX value is", cur_x)  # Print iterations

        print("The local minimum occurs at", cur_x)

        return result
