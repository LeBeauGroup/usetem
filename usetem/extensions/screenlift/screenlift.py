import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets

class ScreenLift(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super().__init__()
        self.defaultParameters.update({'screenLifted': True})
        self.parameterTypes = {'screenLifted': bool}

    def ui(self, item, parent=None):
        theUi = super(ScreenLift, self).ui(item, parent)

        def raiseScreen():

            widget.item.data['screenLifted'] = True

        def lowerScreen():

            widget.item.data['screenLifted'] = False


        widget = theUi.findChild(QtWidgets.QWidget, 'widget')

        raiseRadio = widget.findChildren(QtWidgets.QRadioButton, 'raiseRadio')[0]
        lowerRadio = widget.findChildren(QtWidgets.QRadioButton, 'lowerRadio')[0]


        if not widget.item.data['screenLifted']:
            lowerRadio.setChecked(True)

        raiseRadio.clicked.connect(raiseScreen)
        lowerRadio.clicked.connect(lowerScreen)

        return theUi


    def run(self, params=None, result=None):

        tem = self.interfaces['temscript']
        flu = tem.techniques['FluControl']

        if params['screenLifted']:
            flu.raiseScreen()
        else:
            flu.lowerScreen()


        return None

