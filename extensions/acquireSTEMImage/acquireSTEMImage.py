import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class AcquireSTEMImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireSTEMImage, self).__init__()
        self.defaultParameters.update()

        # self.defaultParameters.update({'rotation': '90', 'dwellTime': '5e-6',
        #                           'binning': '512x512',
        #                           'numFrames': '12', 'detectors': ['HAADF']})

    def run(self, params=None, result=None):
        params = result
        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']

        for i in range(int(params['numFrames'])):
            stem.acquire()

        return result
