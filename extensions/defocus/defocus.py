import useTEM.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np

class Defocus(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'defocus': 10000, 'useCurrentDefocus':False})
        self.parameterTypes = {'defocus': int, 'useCurrentDefocus': bool}

    def ui(self, item, parent=None):
        theUi = super(Defocus, self).ui(item, parent)

        def textFieldEnableDisable() :
            textBox = theUi.findChild(QtWidgets.QLineEdit,'defocusEdit')
            textBox.setDisabled(checkbox.isChecked())

        checkbox = theUi.findChild(QtWidgets.QCheckBox,'useCurrentDefocusEdit')
        checkbox.stateChanged.connect(textFieldEnableDisable)

        if checkbox.isChecked():

            textFieldEnableDisable()



        return theUi




    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']

        if params['useCurrentDefocus']:
            params['defocus'] = optics.defocus()*1e9
            print(params['defocus'])
        else:
            optics.defocus(params['defocus']*1e-9)



        return None

