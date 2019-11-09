import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class StemImageSettings(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(StemImageSettings, self).__init__()

        self.defaultParameters.update({'rotation': '90', 'dwellTime': '5e-6',
                                  'binning': '512x512',
                                  'numFrames': '1', 'detectors': ['HAADF']})

    def run(self, params, result=None):

        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']

        stem.setupAcquisition(params)

        return params
