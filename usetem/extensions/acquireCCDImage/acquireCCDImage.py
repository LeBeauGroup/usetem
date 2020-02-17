import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class AcquireCCDImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireCCDImage, self).__init__()
        self.defaultParameters.update({'detector':'None'})


    def ui(self, item, parent=None):

        theUi = super(AcquireCCDImage, self).ui(item,parent)

        widget = theUi.findChild(QtWidgets.QWidget, 'widget')

        detectorSelection:QtWidgets.QComboBox = widget.findChildren(QtWidgets.QComboBox, 'detector')[0]

        tia = self.interfaces['tiascript']
        ccd = tia.techniques['CCDImage']

        detectorSelection.addItems(ccd.availableCameras())

        return theUi



    def run(self, params, result=None):


        tia = self.interfaces['tiascript']
        ccd = tia.techniques['CCDImage']

        # for i in range(int(params['numFrames'])):
        ccd.acquire()

        if params['currentFrame'] < params['numFrames']:
            params['currentFrame'] += 1


        return result
