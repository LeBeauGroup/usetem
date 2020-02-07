import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class ChangeMagnfication(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'beamBlanked': True})
        self.parameterTypes = {'beamBlanked': bool}

    def ui(self, item, parent=None):
        theUi = super(ChangeMagnfication, self).ui(item, parent)

        def blankBeam():

            widget.item.data['beamBlanked'] = True

        def unblankBeam():

            widget.item.data['beamBlanked'] = False


        widget = theUi.findChild(QtWidgets.QWidget, 'widget')

        blankRadio = widget.findChildren(QtWidgets.QRadioButton, 'blankRadio')[0]
        unblankRadio = widget.findChildren(QtWidgets.QRadioButton, 'unblankRadio')[0]


        if not widget.item.data['beamBlanked']:
            unblankRadio.setChecked(True)

        blankRadio.clicked.connect(blankBeam)
        unblankRadio.clicked.connect(unblankBeam)
        return theUi




    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        optics = tem.techniques['OpticsControl']

        print(params['beamBlanked'])

        optics.isBeamBlanked(params['beamBlanked'])





        return None

