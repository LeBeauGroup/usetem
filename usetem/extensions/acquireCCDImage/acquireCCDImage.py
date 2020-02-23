import usetem.pluginTypes as pluginTypes
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np



class AcquireCCDImage(pluginTypes.IExtensionPlugin):

    def __init__(self):

        super(AcquireCCDImage, self).__init__()
        self.defaultParameters.update({'detector':'None', 'integrationTime':0.1, 'binning':1})

        self.parameterTypes = {'detector':str, 'binning':int, 'integrationTime':float}


    def ui(self, item, parent=None):

        theUi = super(AcquireCCDImage, self).ui(item,parent)

        widget = theUi.findChild(QtWidgets.QWidget, 'widget')

        detectorSelection:QtWidgets.QComboBox = widget.findChildren(QtWidgets.QComboBox, 'detectorEdit')[0]
        binningSelection: QtWidgets.QComboBox = widget.findChildren(QtWidgets.QComboBox, 'binningEdit')[0]

        integrationEdit:QtWidgets.QDoubleSpinBox = widget.findChildren(QtWidgets.QDoubleSpinBox, 'integrationTimeEdit')[0]

        tia = self.interfaces['tiascript']
        ccd = tia.techniques['CCDImage']


        intRange = ccd.integrationTimeRange()

        integrationEdit.setMinimum(intRange[0])
        integrationEdit.setMaximum(intRange[1])

        detectorSelection.addItems(ccd.availableCameras())
        binningSelection.addItems(ccd.availableBinnings())


        return theUi



    def run(self, params, result=None):


        tia = self.interfaces['tiascript']
        ccd = tia.techniques['CCDImage']

        if params['detector'] == 'None':
            return

        ccd.setupAcquisition(params)
        # for i in range(int(params['numFrames'])):
        ccd.acquire()



        return result
