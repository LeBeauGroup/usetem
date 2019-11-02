import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class StemImageSettings(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(StemImageSettings, self).__init__()
        self.defaultParameters.update()
        self.acceptsChildren = True

    def run(self, input=None):



        return input
