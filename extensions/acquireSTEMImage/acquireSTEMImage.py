import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class AcquireSTEMImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireSTEMImage, self).__init__()
        self.defaultParameters.update()


    def run(self, params, result=None):

        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']

        for i in range(int(params['numFrames'])):
            stem.acquire()

        return result
