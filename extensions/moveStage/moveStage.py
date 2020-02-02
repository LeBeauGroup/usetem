import useTEM.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class MoveStage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'magnification': 10000, 'useCurrentMag':False})
        self.parameterTypes = {'magnification': int, 'useCurrentMag': bool}

    def ui(self, item, parent=None):
        # theUi = super(ChangeMagnfication, self).ui(item, parent)
        #
        # def textFieldEnableDisable() :
        #     textBox = theUi.findChild(QtWidgets.QLineEdit,'magnificationEdit')
        #     textBox.setDisabled(checkbox.isChecked())
        #
        # checkbox = theUi.findChild(QtWidgets.QCheckBox,'useCurrentMagEdit')
        # checkbox.stateChanged.connect(textFieldEnableDisable)
        #
        # if checkbox.isChecked():
        #
        #     textFieldEnableDisable()



        return theUi




    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        stage = tem.techniques['StageControl']

        if params['useCurrentMag']:
            params['magnification'] = optics.magnification()
            print(params['magnification'])
        else:
            optics.magnification(params['magnification'])



        return None

