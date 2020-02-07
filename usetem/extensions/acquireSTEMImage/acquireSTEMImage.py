import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class AcquireSTEMImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireSTEMImage, self).__init__()
        self.defaultParameters.update({'currentFrame':0})


    def run(self, params, result=None):


        tia = self.interfaces['tiascript']
        stem = tia.techniques['STEMImage']

        # for i in range(int(params['numFrames'])):
        stem.acquire()

        if params['currentFrame'] < params['numFrames']:
            params['currentFrame'] += 1


        return result
