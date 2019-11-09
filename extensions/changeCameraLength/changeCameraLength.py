import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ChangeCameraLength(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'cameraLength': '100'})


    def run(self, input=None):

        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']
        optics.cameraLength(input['cameraLength'])

        return None

