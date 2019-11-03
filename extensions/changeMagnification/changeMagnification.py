import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ChangeMagnfication(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'magnification': '10000'})


    def run(self, input=None):

        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']
        optics.magnification(input['magnification'])

        return None

