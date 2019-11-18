import pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ChangeMagnfication(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'magnification': '10000'})

    def ui(self, item, parent=None):

        theUi = super(ChangeMagnfication, self).ui(item, parent)
        doubleVal = QtGui.QDoubleValidator()
        intVal = QtGui.QIntValidator()

        theUi.magnificationEdit.setValidator(intVal)
        return theUi




    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']
        optics.magnification(params['magnification'])

        return None

