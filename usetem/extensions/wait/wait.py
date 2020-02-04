import useTEM.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import time



class AcquireSTEMImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireSTEMImage, self).__init__()
        self.defaultParameters.update({'delay': 1})
        self.parameterTypes = {'delay':float}


    def run(self, params, result=None):
        delayTime = params['delay']
        print(f'Holding for {delayTime} seconds')
        time.sleep(delayTime)


        return result


